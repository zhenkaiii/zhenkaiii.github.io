"""Tests for Level 3 — Scheduler + Priority."""

import unittest

from bank import (
    AccountNotFound,
    BankLevel3,
    DuplicateTransactionId,
    InvalidAmount,
    SameAccountTransfer,
)


class TestBankLevel3(unittest.TestCase):
    def setUp(self) -> None:
        self.bank = BankLevel3()
        self.bank.create_account("alice")
        self.bank.create_account("bob")
        self.bank.deposit("alice", 10_000)
        self.bank.deposit("bob", 5_000)

    # -- basic scheduling ----------------------------------------------

    def test_schedule_and_run(self) -> None:
        self.bank.schedule_transfer("tx1", when_ts=100, src="alice", dst="bob", amount=1_000)
        results = self.bank.run_due(now_ts=100)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "executed")
        self.assertEqual(results[0]["tx_id"], "tx1")
        self.assertEqual(self.bank.get_balance("alice"), 9_000)
        self.assertEqual(self.bank.get_balance("bob"), 6_000)

    def test_not_due_yet(self) -> None:
        self.bank.schedule_transfer("tx1", when_ts=200, src="alice", dst="bob", amount=1_000)
        results = self.bank.run_due(now_ts=100)
        self.assertEqual(results, [])
        self.assertEqual(self.bank.get_balance("alice"), 10_000)

    def test_run_due_empty_heap(self) -> None:
        self.assertEqual(self.bank.run_due(now_ts=9999), [])

    # -- ordering ------------------------------------------------------

    def test_timestamp_ordering(self) -> None:
        self.bank.schedule_transfer("tx_late", when_ts=200, src="alice", dst="bob", amount=100)
        self.bank.schedule_transfer("tx_early", when_ts=100, src="alice", dst="bob", amount=200)
        results = self.bank.run_due(now_ts=200)
        self.assertEqual(results[0]["tx_id"], "tx_early")
        self.assertEqual(results[1]["tx_id"], "tx_late")

    def test_priority_ordering(self) -> None:
        """Higher priority number → executes first when timestamps tie."""
        self.bank.schedule_transfer(
            "tx_low", when_ts=100, src="alice", dst="bob", amount=100, priority=1,
        )
        self.bank.schedule_transfer(
            "tx_high", when_ts=100, src="alice", dst="bob", amount=100, priority=10,
        )
        results = self.bank.run_due(now_ts=100)
        self.assertEqual(results[0]["tx_id"], "tx_high")
        self.assertEqual(results[1]["tx_id"], "tx_low")

    def test_insertion_order_tiebreak(self) -> None:
        """Same timestamp and priority → first-scheduled wins."""
        self.bank.schedule_transfer(
            "tx_first", when_ts=100, src="alice", dst="bob", amount=100, priority=5,
        )
        self.bank.schedule_transfer(
            "tx_second", when_ts=100, src="alice", dst="bob", amount=100, priority=5,
        )
        results = self.bank.run_due(now_ts=100)
        self.assertEqual(results[0]["tx_id"], "tx_first")
        self.assertEqual(results[1]["tx_id"], "tx_second")

    # -- failure at execution time -------------------------------------

    def test_insufficient_funds_at_execution(self) -> None:
        self.bank.schedule_transfer(
            "tx1", when_ts=100, src="alice", dst="bob", amount=999_999,
        )
        results = self.bank.run_due(now_ts=100)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "failed")
        self.assertIn("error", results[0])
        # Balances unchanged.
        self.assertEqual(self.bank.get_balance("alice"), 10_000)
        self.assertEqual(self.bank.get_balance("bob"), 5_000)

    def test_failed_transfer_does_not_block_others(self) -> None:
        self.bank.schedule_transfer(
            "tx_fail", when_ts=100, src="alice", dst="bob",
            amount=999_999, priority=10,
        )
        self.bank.schedule_transfer(
            "tx_ok", when_ts=100, src="alice", dst="bob",
            amount=100, priority=1,
        )
        results = self.bank.run_due(now_ts=100)
        self.assertEqual(results[0]["tx_id"], "tx_fail")
        self.assertEqual(results[0]["status"], "failed")
        self.assertEqual(results[1]["tx_id"], "tx_ok")
        self.assertEqual(results[1]["status"], "executed")

    # -- validation at schedule time -----------------------------------

    def test_duplicate_tx_id(self) -> None:
        self.bank.schedule_transfer("tx1", when_ts=100, src="alice", dst="bob", amount=100)
        with self.assertRaises(DuplicateTransactionId):
            self.bank.schedule_transfer("tx1", when_ts=200, src="alice", dst="bob", amount=200)

    def test_schedule_validates_accounts(self) -> None:
        with self.assertRaises(AccountNotFound):
            self.bank.schedule_transfer("tx1", when_ts=100, src="ghost", dst="bob", amount=100)

    def test_schedule_validates_amount(self) -> None:
        with self.assertRaises(InvalidAmount):
            self.bank.schedule_transfer("tx1", when_ts=100, src="alice", dst="bob", amount=-1)

    def test_schedule_validates_same_account(self) -> None:
        with self.assertRaises(SameAccountTransfer):
            self.bank.schedule_transfer("tx1", when_ts=100, src="alice", dst="alice", amount=100)

    # -- partial due ---------------------------------------------------

    def test_only_due_transfers_run(self) -> None:
        self.bank.schedule_transfer("tx1", when_ts=50, src="alice", dst="bob", amount=100)
        self.bank.schedule_transfer("tx2", when_ts=150, src="alice", dst="bob", amount=200)
        results = self.bank.run_due(now_ts=100)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["tx_id"], "tx1")
        # tx2 still pending — run again later.
        results2 = self.bank.run_due(now_ts=200)
        self.assertEqual(len(results2), 1)
        self.assertEqual(results2[0]["tx_id"], "tx2")


if __name__ == "__main__":
    unittest.main()
