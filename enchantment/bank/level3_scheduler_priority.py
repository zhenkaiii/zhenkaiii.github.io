"""Level 3 — Scheduled transfers with priority ordering.

Transfers are stored in a min-heap keyed by ``(when_ts, -priority, seq)``.
Lower *when_ts* runs first; among ties, higher *priority* (larger int) runs
first; among ties in both, the transfer that was scheduled first wins.

Failed transfers at execution time are recorded but do **not** block remaining
due transfers.
"""

from __future__ import annotations

import heapq

from .core import (
    DuplicateTransactionId,
    SameAccountTransfer,
)
from .level2_batch_atomic import BankLevel2


class BankLevel3(BankLevel2):
    """Extends Level 2 with heap-based scheduled transfers."""

    def __init__(self) -> None:
        super().__init__()
        # Heap entries: (when_ts, -priority, seq, tx_id, src, dst, amount)
        self._heap: list[tuple[int, int, int, str, str, str, int]] = []
        self._scheduled_ids: set[str] = set()
        self._seq: int = 0

    def schedule_transfer(
        self,
        tx_id: str,
        when_ts: int,
        src: str,
        dst: str,
        amount: int,
        priority: int = 0,
    ) -> None:
        """Enqueue a transfer for future execution.

        Validates accounts and amount eagerly so callers get immediate
        feedback, but the actual balance check happens at execution time.
        """
        if tx_id in self._scheduled_ids:
            raise DuplicateTransactionId(tx_id)

        # Eager validation (balance is checked later at execution time).
        self._validate_amount(amount)
        self._require_account(src)
        self._require_account(dst)
        if src == dst:
            raise SameAccountTransfer(src)

        self._scheduled_ids.add(tx_id)
        entry = (when_ts, -priority, self._seq, tx_id, src, dst, amount)
        self._seq += 1
        heapq.heappush(self._heap, entry)

    def run_due(self, now_ts: int) -> list[dict]:
        """Pop and execute every transfer whose *when_ts* <= *now_ts*.

        Returns a result dict per executed transfer.
        """
        results: list[dict] = []

        while self._heap and self._heap[0][0] <= now_ts:
            _when, _neg_pri, _seq, tx_id, src, dst, amount = heapq.heappop(
                self._heap
            )
            try:
                src_bal, dst_bal = self.transfer(src, dst, amount)
                results.append({
                    "tx_id": tx_id,
                    "status": "executed",
                    "src": src,
                    "dst": dst,
                    "amount": amount,
                    "src_balance": src_bal,
                    "dst_balance": dst_bal,
                })
            except Exception as exc:
                results.append({
                    "tx_id": tx_id,
                    "status": "failed",
                    "src": src,
                    "dst": dst,
                    "amount": amount,
                    "error": str(exc),
                })

        return results
