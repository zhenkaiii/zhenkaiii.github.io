"""Tests for Level 4 — Audit Log + Idempotency."""

import unittest

from bank import BankLevel4, IdempotencyConflict


class TestAuditLog(unittest.TestCase):
    def setUp(self) -> None:
        self.bank = BankLevel4()
        self.bank.create_account("alice")
        self.bank.create_account("bob")
        # These deposits are audited.
        self.bank.deposit("alice", 10_000)
        self.bank.deposit("bob", 5_000)

    # -- audit basics --------------------------------------------------

    def test_deposit_is_logged(self) -> None:
        self.bank.deposit("alice", 500)
        entries = [e for e in self.bank.get_audit_log() if e["op"] == "deposit"]
        last = entries[-1]
        self.assertTrue(last["success"])
        self.assertEqual(last["amount"], 500)
        self.assertEqual(last["balance"], 10_500)

    def test_failed_withdraw_is_logged(self) -> None:
        with self.assertRaises(Exception):
            self.bank.withdraw("alice", 999_999)
        failures = [e for e in self.bank.get_audit_log() if not e["success"]]
        self.assertTrue(len(failures) >= 1)
        self.assertEqual(failures[-1]["op"], "withdraw")

    def test_transfer_is_logged(self) -> None:
        self.bank.transfer("alice", "bob", 1_000)
        transfers = [e for e in self.bank.get_audit_log() if e["op"] == "transfer"]
        self.assertEqual(len(transfers), 1)
        self.assertTrue(transfers[0]["success"])
        self.assertEqual(transfers[0]["src_balance"], 9_000)
        self.assertEqual(transfers[0]["dst_balance"], 6_000)

    def test_schedule_transfer_is_logged(self) -> None:
        self.bank.schedule_transfer("tx1", 100, "alice", "bob", 500)
        entries = [e for e in self.bank.get_audit_log() if e["op"] == "schedule_transfer"]
        self.assertEqual(len(entries), 1)
        self.assertTrue(entries[0]["success"])

    def test_batch_is_logged_as_unit(self) -> None:
        self.bank.apply_batch([
            {"type": "deposit", "id": "alice", "amount": 100},
        ])
        batch_entries = [e for e in self.bank.get_audit_log() if e["op"] == "batch"]
        self.assertEqual(len(batch_entries), 1)
        self.assertTrue(batch_entries[0]["success"])

    def test_failed_batch_logged(self) -> None:
        self.bank.apply_batch([
            {"type": "deposit", "id": "alice", "amount": 100},
            {"type": "withdraw", "id": "alice", "amount": 999_999},
        ])
        batch_entries = [e for e in self.bank.get_audit_log() if e["op"] == "batch"]
        self.assertEqual(len(batch_entries), 1)
        self.assertFalse(batch_entries[0]["success"])

    # -- limit ---------------------------------------------------------

    def test_limit_returns_last_n(self) -> None:
        for _ in range(20):
            self.bank.deposit("alice", 1)
        log = self.bank.get_audit_log(limit=5)
        self.assertEqual(len(log), 5)

    def test_limit_none_returns_all(self) -> None:
        log = self.bank.get_audit_log(limit=None)
        self.assertIsInstance(log, list)
        self.assertGreater(len(log), 0)

    # -- timestamps ----------------------------------------------------

    def test_timestamps_monotonically_increase(self) -> None:
        self.bank.deposit("alice", 100)
        self.bank.withdraw("alice", 50)
        self.bank.transfer("alice", "bob", 25)
        ts_list = [e["ts"] for e in self.bank.get_audit_log()]
        self.assertEqual(ts_list, sorted(ts_list))
        self.assertEqual(len(ts_list), len(set(ts_list)), "timestamps must be unique")

    # -- idem_key stored in log ----------------------------------------

    def test_idem_key_in_audit_entry(self) -> None:
        self.bank.deposit("alice", 100, idem_key="d-1")
        entries = [e for e in self.bank.get_audit_log() if e.get("idem_key") == "d-1"]
        self.assertEqual(len(entries), 1)


class TestIdempotency(unittest.TestCase):
    def setUp(self) -> None:
        self.bank = BankLevel4()
        self.bank.create_account("alice")
        self.bank.create_account("bob")
        self.bank.deposit("alice", 10_000)
        self.bank.deposit("bob", 5_000)

    # -- deposit -------------------------------------------------------

    def test_deposit_replay(self) -> None:
        b1 = self.bank.deposit("alice", 500, idem_key="dep-001")
        b2 = self.bank.deposit("alice", 500, idem_key="dep-001")
        self.assertEqual(b1, b2)
        self.assertEqual(self.bank.get_balance("alice"), 10_500)  # applied once

    def test_deposit_conflict(self) -> None:
        self.bank.deposit("alice", 500, idem_key="dep-001")
        with self.assertRaises(IdempotencyConflict):
            self.bank.deposit("alice", 999, idem_key="dep-001")

    # -- withdraw ------------------------------------------------------

    def test_withdraw_replay(self) -> None:
        b1 = self.bank.withdraw("alice", 500, idem_key="wd-001")
        b2 = self.bank.withdraw("alice", 500, idem_key="wd-001")
        self.assertEqual(b1, b2)
        self.assertEqual(self.bank.get_balance("alice"), 9_500)

    def test_withdraw_conflict(self) -> None:
        self.bank.withdraw("alice", 500, idem_key="wd-001")
        with self.assertRaises(IdempotencyConflict):
            self.bank.withdraw("alice", 999, idem_key="wd-001")

    # -- transfer ------------------------------------------------------

    def test_transfer_replay(self) -> None:
        r1 = self.bank.transfer("alice", "bob", 1_000, idem_key="xfer-001")
        r2 = self.bank.transfer("alice", "bob", 1_000, idem_key="xfer-001")
        self.assertEqual(r1, r2)
        self.assertEqual(self.bank.get_balance("alice"), 9_000)

    def test_transfer_conflict(self) -> None:
        self.bank.transfer("alice", "bob", 1_000, idem_key="xfer-001")
        with self.assertRaises(IdempotencyConflict):
            self.bank.transfer("alice", "bob", 2_000, idem_key="xfer-001")

    # -- schedule_transfer ---------------------------------------------

    def test_schedule_replay(self) -> None:
        self.bank.schedule_transfer(
            "tx1", 100, "alice", "bob", 1_000, idem_key="sched-001",
        )
        # Replay must not raise DuplicateTransactionId.
        self.bank.schedule_transfer(
            "tx1", 100, "alice", "bob", 1_000, idem_key="sched-001",
        )

    def test_schedule_conflict(self) -> None:
        self.bank.schedule_transfer(
            "tx1", 100, "alice", "bob", 1_000, idem_key="sched-001",
        )
        with self.assertRaises(IdempotencyConflict):
            self.bank.schedule_transfer(
                "tx1", 100, "alice", "bob", 2_000, idem_key="sched-001",
            )

    # -- no key → always apply -----------------------------------------

    def test_no_idem_key_always_applies(self) -> None:
        self.bank.deposit("alice", 500)
        self.bank.deposit("alice", 500)
        self.assertEqual(self.bank.get_balance("alice"), 11_000)

    # -- different keys → independent ----------------------------------

    def test_different_keys_are_independent(self) -> None:
        self.bank.deposit("alice", 500, idem_key="a")
        self.bank.deposit("alice", 500, idem_key="b")
        self.assertEqual(self.bank.get_balance("alice"), 11_000)


if __name__ == "__main__":
    unittest.main()
