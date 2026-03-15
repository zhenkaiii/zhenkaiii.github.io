"""Level 4 — Audit log + idempotency keys.

Append-only audit log captures every attempted operation (success or failure).
Idempotency keys allow external callers to safely retry without double-applying:
  - Same key + same params  → return cached result, no side-effects.
  - Same key + different params → raise ``IdempotencyConflict``.
  - No key (``None``)       → always execute normally.

Design note on batches:
  During ``apply_batch`` we set a ``_batch_active`` flag so that the
  individual deposit/withdraw/transfer calls skip per-op audit logging.
  The batch is logged as a single audit entry instead, avoiding misleading
  "success" entries for ops that were subsequently rolled back.
"""

from __future__ import annotations

import hashlib
import json

from .core import IdempotencyConflict
from .level3_scheduler_priority import BankLevel3


class BankLevel4(BankLevel3):
    """Extends Level 3 with append-only audit log and idempotency."""

    def __init__(self) -> None:
        super().__init__()
        self._audit_log: list[dict] = []
        self._idem_store: dict[str, dict] = {}
        self._ts: int = 0  # monotonic logical clock
        self._batch_active: bool = False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _next_ts(self) -> int:
        self._ts += 1
        return self._ts

    @staticmethod
    def _request_hash(method: str, **kwargs: object) -> str:
        """Deterministic hash of (method, params) for idempotency checks."""
        canonical = json.dumps({"m": method, **kwargs}, sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()

    def _check_idem(
        self, idem_key: str | None, method: str, **kwargs: object
    ) -> dict | None:
        """Return cached response for *idem_key*, or ``None`` if unseen.

        Raises ``IdempotencyConflict`` if the key was used with different params.
        """
        if idem_key is None:
            return None
        req_hash = self._request_hash(method, **kwargs)
        if idem_key in self._idem_store:
            stored = self._idem_store[idem_key]
            if stored["hash"] != req_hash:
                raise IdempotencyConflict(idem_key)
            return stored["response"]
        return None

    def _store_idem(
        self, idem_key: str | None, method: str, response: dict, **kwargs: object
    ) -> None:
        if idem_key is None:
            return
        req_hash = self._request_hash(method, **kwargs)
        self._idem_store[idem_key] = {"hash": req_hash, "response": response}

    def _log(self, entry: dict) -> None:
        self._audit_log.append(entry)

    # ------------------------------------------------------------------
    # Overridden public API
    # ------------------------------------------------------------------

    def deposit(
        self, account_id: str, amount: int, *, idem_key: str | None = None
    ) -> int:
        # Inside a batch → skip audit/idempotency (batch logged as a unit).
        if self._batch_active:
            return super().deposit(account_id, amount)

        cached = self._check_idem(
            idem_key, "deposit", account_id=account_id, amount=amount
        )
        if cached is not None:
            return cached["balance"]

        ts = self._next_ts()
        try:
            balance = super().deposit(account_id, amount)
        except Exception as exc:
            self._log({
                "ts": ts, "op": "deposit", "account_id": account_id,
                "amount": amount, "success": False, "error": str(exc),
                "idem_key": idem_key,
            })
            raise

        self._log({
            "ts": ts, "op": "deposit", "account_id": account_id,
            "amount": amount, "success": True, "balance": balance,
            "idem_key": idem_key,
        })
        self._store_idem(
            idem_key, "deposit", {"balance": balance},
            account_id=account_id, amount=amount,
        )
        return balance

    def withdraw(
        self, account_id: str, amount: int, *, idem_key: str | None = None
    ) -> int:
        if self._batch_active:
            return super().withdraw(account_id, amount)

        cached = self._check_idem(
            idem_key, "withdraw", account_id=account_id, amount=amount
        )
        if cached is not None:
            return cached["balance"]

        ts = self._next_ts()
        try:
            balance = super().withdraw(account_id, amount)
        except Exception as exc:
            self._log({
                "ts": ts, "op": "withdraw", "account_id": account_id,
                "amount": amount, "success": False, "error": str(exc),
                "idem_key": idem_key,
            })
            raise

        self._log({
            "ts": ts, "op": "withdraw", "account_id": account_id,
            "amount": amount, "success": True, "balance": balance,
            "idem_key": idem_key,
        })
        self._store_idem(
            idem_key, "withdraw", {"balance": balance},
            account_id=account_id, amount=amount,
        )
        return balance

    def transfer(
        self,
        src_id: str,
        dst_id: str,
        amount: int,
        *,
        idem_key: str | None = None,
    ) -> tuple[int, int]:
        if self._batch_active:
            return super().transfer(src_id, dst_id, amount)

        cached = self._check_idem(
            idem_key, "transfer",
            src_id=src_id, dst_id=dst_id, amount=amount,
        )
        if cached is not None:
            return cached["src_balance"], cached["dst_balance"]

        ts = self._next_ts()
        try:
            src_bal, dst_bal = super().transfer(src_id, dst_id, amount)
        except Exception as exc:
            self._log({
                "ts": ts, "op": "transfer", "src_id": src_id,
                "dst_id": dst_id, "amount": amount,
                "success": False, "error": str(exc), "idem_key": idem_key,
            })
            raise

        self._log({
            "ts": ts, "op": "transfer", "src_id": src_id,
            "dst_id": dst_id, "amount": amount,
            "success": True, "src_balance": src_bal, "dst_balance": dst_bal,
            "idem_key": idem_key,
        })
        self._store_idem(
            idem_key, "transfer", {"src_balance": src_bal, "dst_balance": dst_bal},
            src_id=src_id, dst_id=dst_id, amount=amount,
        )
        return src_bal, dst_bal

    def schedule_transfer(
        self,
        tx_id: str,
        when_ts: int,
        src: str,
        dst: str,
        amount: int,
        priority: int = 0,
        *,
        idem_key: str | None = None,
    ) -> None:
        cached = self._check_idem(
            idem_key, "schedule_transfer",
            tx_id=tx_id, when_ts=when_ts, src=src, dst=dst,
            amount=amount, priority=priority,
        )
        if cached is not None:
            return  # idempotent replay — already scheduled

        ts = self._next_ts()
        try:
            super().schedule_transfer(tx_id, when_ts, src, dst, amount, priority)
        except Exception as exc:
            self._log({
                "ts": ts, "op": "schedule_transfer", "tx_id": tx_id,
                "when_ts": when_ts, "src": src, "dst": dst,
                "amount": amount, "priority": priority,
                "success": False, "error": str(exc), "idem_key": idem_key,
            })
            raise

        self._log({
            "ts": ts, "op": "schedule_transfer", "tx_id": tx_id,
            "when_ts": when_ts, "src": src, "dst": dst,
            "amount": amount, "priority": priority,
            "success": True, "idem_key": idem_key,
        })
        self._store_idem(
            idem_key, "schedule_transfer", {},
            tx_id=tx_id, when_ts=when_ts, src=src, dst=dst,
            amount=amount, priority=priority,
        )

    def apply_batch(self, ops: list[dict]) -> list[dict]:
        """Atomic batch — logged as a single audit entry."""
        self._batch_active = True
        try:
            results = super().apply_batch(ops)
        finally:
            self._batch_active = False

        ts = self._next_ts()
        batch_ok = all(r["success"] for r in results)
        self._log({
            "ts": ts, "op": "batch", "num_ops": len(ops),
            "success": batch_ok, "results": results,
        })
        return results

    # ------------------------------------------------------------------
    # Audit query
    # ------------------------------------------------------------------

    def get_audit_log(self, limit: int | None = None) -> list[dict]:
        """Return audit entries.  *limit* returns the last N entries."""
        if limit is None:
            return list(self._audit_log)
        return list(self._audit_log[-limit:])
