"""Level 2 — Batch operations with atomic rollback.

Operations are executed in queue order.  If any single operation fails the
entire batch is rolled back (snapshot-restore) so the bank state is unchanged.

Why snapshot instead of inverse operations?
  Snapshot is O(number-of-accounts) for the copy but dead simple — no risk of
  getting the inverse wrong for an edge-case.  For an interview-sized system
  with a modest number of accounts this is the right trade-off.
"""

from .level1_basic import BankLevel1


class BankLevel2(BankLevel1):
    """Extends Level 1 with atomic batch operations."""

    def apply_batch(self, ops: list[dict]) -> list[dict]:
        """Execute *ops* atomically — all-or-nothing.

        Each op is a dict:
          deposit:  ``{"type": "deposit",  "id": ..., "amount": ...}``
          withdraw: ``{"type": "withdraw", "id": ..., "amount": ...}``
          transfer: ``{"type": "transfer", "src": ..., "dst": ..., "amount": ...}``

        Returns one result dict per op, always in the same order.
        """
        snapshot = self._accounts.copy()
        results: list[dict] = []

        for i, op in enumerate(ops):
            try:
                result = self._execute_op(op)
                results.append({"op_index": i, "success": True, **result})
            except Exception as exc:
                results.append({
                    "op_index": i,
                    "success": False,
                    "error": str(exc),
                })
                # Roll back the entire batch.
                self._accounts = snapshot
                # Mark remaining ops as not-executed.
                for j in range(i + 1, len(ops)):
                    results.append({
                        "op_index": j,
                        "success": False,
                        "error": "not executed (batch rolled back)",
                    })
                return results

        return results

    def _execute_op(self, op: dict) -> dict:
        """Dispatch a single operation dict to the matching method."""
        op_type = op.get("type")
        if op_type == "deposit":
            balance = self.deposit(op["id"], op["amount"])
            return {"type": "deposit", "id": op["id"], "balance": balance}
        if op_type == "withdraw":
            balance = self.withdraw(op["id"], op["amount"])
            return {"type": "withdraw", "id": op["id"], "balance": balance}
        if op_type == "transfer":
            src_bal, dst_bal = self.transfer(op["src"], op["dst"], op["amount"])
            return {
                "type": "transfer",
                "src": op["src"],
                "dst": op["dst"],
                "src_balance": src_bal,
                "dst_balance": dst_bal,
            }
        raise ValueError(f"Unknown operation type: {op_type!r}")
