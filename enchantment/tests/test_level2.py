"""Tests for Level 2 — Batch + Atomicity."""

import unittest

from bank import BankLevel2


class TestBankLevel2(unittest.TestCase):
    def setUp(self) -> None:
        self.bank = BankLevel2()
        self.bank.create_account("alice")
        self.bank.create_account("bob")
        self.bank.deposit("alice", 10_000)
        self.bank.deposit("bob", 5_000)

    # -- happy path ----------------------------------------------------

    def test_batch_all_succeed(self) -> None:
        results = self.bank.apply_batch([
            {"type": "deposit", "id": "alice", "amount": 500},
            {"type": "withdraw", "id": "bob", "amount": 200},
            {"type": "transfer", "src": "alice", "dst": "bob", "amount": 1000},
        ])
        self.assertTrue(all(r["success"] for r in results))
        self.assertEqual(self.bank.get_balance("alice"), 10_000 + 500 - 1000)
        self.assertEqual(self.bank.get_balance("bob"), 5_000 - 200 + 1000)

    def test_batch_single_op(self) -> None:
        results = self.bank.apply_batch([
            {"type": "deposit", "id": "alice", "amount": 100},
        ])
        self.assertTrue(results[0]["success"])
        self.assertEqual(results[0]["balance"], 10_100)

    def test_batch_empty(self) -> None:
        self.assertEqual(self.bank.apply_batch([]), [])

    # -- rollback ------------------------------------------------------

    def test_batch_atomic_rollback(self) -> None:
        alice_before = self.bank.get_balance("alice")
        bob_before = self.bank.get_balance("bob")

        results = self.bank.apply_batch([
            {"type": "deposit", "id": "alice", "amount": 5_000},
            {"type": "transfer", "src": "bob", "dst": "alice", "amount": 999_999},
        ])

        # First op "succeeded" but batch rolled back.
        self.assertTrue(results[0]["success"])
        self.assertFalse(results[1]["success"])

        # State is exactly as before.
        self.assertEqual(self.bank.get_balance("alice"), alice_before)
        self.assertEqual(self.bank.get_balance("bob"), bob_before)

    def test_remaining_ops_marked_not_executed(self) -> None:
        results = self.bank.apply_batch([
            {"type": "deposit", "id": "alice", "amount": 100},
            {"type": "withdraw", "id": "alice", "amount": 999_999},
            {"type": "deposit", "id": "bob", "amount": 100},
        ])
        self.assertTrue(results[0]["success"])
        self.assertFalse(results[1]["success"])
        self.assertFalse(results[2]["success"])
        self.assertIn("rolled back", results[2]["error"])

    def test_rollback_preserves_all_accounts(self) -> None:
        """Accounts *not* touched by the batch must also be unchanged."""
        self.bank.create_account("carol")
        self.bank.deposit("carol", 1_000)

        self.bank.apply_batch([
            {"type": "deposit", "id": "alice", "amount": 100},
            {"type": "deposit", "id": "carol", "amount": 100},
            {"type": "withdraw", "id": "bob", "amount": 999_999},
        ])

        self.assertEqual(self.bank.get_balance("alice"), 10_000)
        self.assertEqual(self.bank.get_balance("bob"), 5_000)
        self.assertEqual(self.bank.get_balance("carol"), 1_000)

    # -- error types ---------------------------------------------------

    def test_batch_unknown_op_type(self) -> None:
        results = self.bank.apply_batch([
            {"type": "explode", "id": "alice"},
        ])
        self.assertFalse(results[0]["success"])

    def test_batch_first_op_fails(self) -> None:
        """If the very first op fails, every op is marked failed."""
        results = self.bank.apply_batch([
            {"type": "withdraw", "id": "alice", "amount": 999_999},
            {"type": "deposit", "id": "alice", "amount": 100},
        ])
        self.assertFalse(results[0]["success"])
        self.assertFalse(results[1]["success"])
        self.assertEqual(self.bank.get_balance("alice"), 10_000)


if __name__ == "__main__":
    unittest.main()
