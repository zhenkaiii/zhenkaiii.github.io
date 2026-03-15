"""Tests for Level 1 — Basic Bank."""

import unittest

from bank import (
    AccountNotFound,
    BankLevel1,
    DuplicateAccount,
    InsufficientFunds,
    InvalidAmount,
    SameAccountTransfer,
)


class TestBankLevel1(unittest.TestCase):
    def setUp(self) -> None:
        self.bank = BankLevel1()

    # -- create_account ------------------------------------------------

    def test_create_account(self) -> None:
        self.bank.create_account("alice")
        self.assertEqual(self.bank.get_balance("alice"), 0)

    def test_create_duplicate_raises(self) -> None:
        self.bank.create_account("alice")
        with self.assertRaises(DuplicateAccount):
            self.bank.create_account("alice")

    # -- deposit -------------------------------------------------------

    def test_deposit_returns_new_balance(self) -> None:
        self.bank.create_account("alice")
        self.assertEqual(self.bank.deposit("alice", 1000), 1000)

    def test_deposit_accumulates(self) -> None:
        self.bank.create_account("alice")
        self.bank.deposit("alice", 1000)
        self.assertEqual(self.bank.deposit("alice", 500), 1500)

    def test_deposit_unknown_account(self) -> None:
        with self.assertRaises(AccountNotFound):
            self.bank.deposit("ghost", 100)

    def test_deposit_zero_amount(self) -> None:
        self.bank.create_account("alice")
        with self.assertRaises(InvalidAmount):
            self.bank.deposit("alice", 0)

    def test_deposit_negative_amount(self) -> None:
        self.bank.create_account("alice")
        with self.assertRaises(InvalidAmount):
            self.bank.deposit("alice", -100)

    def test_deposit_float_amount(self) -> None:
        self.bank.create_account("alice")
        with self.assertRaises(InvalidAmount):
            self.bank.deposit("alice", 10.5)  # type: ignore[arg-type]

    # -- withdraw ------------------------------------------------------

    def test_withdraw_returns_new_balance(self) -> None:
        self.bank.create_account("alice")
        self.bank.deposit("alice", 1000)
        self.assertEqual(self.bank.withdraw("alice", 400), 600)

    def test_withdraw_exact_balance(self) -> None:
        self.bank.create_account("alice")
        self.bank.deposit("alice", 1000)
        self.assertEqual(self.bank.withdraw("alice", 1000), 0)

    def test_withdraw_insufficient_funds(self) -> None:
        self.bank.create_account("alice")
        self.bank.deposit("alice", 100)
        with self.assertRaises(InsufficientFunds):
            self.bank.withdraw("alice", 200)

    def test_withdraw_from_empty_account(self) -> None:
        self.bank.create_account("alice")
        with self.assertRaises(InsufficientFunds):
            self.bank.withdraw("alice", 1)

    def test_withdraw_unknown_account(self) -> None:
        with self.assertRaises(AccountNotFound):
            self.bank.withdraw("ghost", 100)

    def test_withdraw_invalid_amount(self) -> None:
        self.bank.create_account("alice")
        with self.assertRaises(InvalidAmount):
            self.bank.withdraw("alice", -50)

    # -- transfer ------------------------------------------------------

    def test_transfer_returns_both_balances(self) -> None:
        self.bank.create_account("alice")
        self.bank.create_account("bob")
        self.bank.deposit("alice", 1000)
        src, dst = self.bank.transfer("alice", "bob", 400)
        self.assertEqual(src, 600)
        self.assertEqual(dst, 400)

    def test_transfer_to_self_raises(self) -> None:
        self.bank.create_account("alice")
        self.bank.deposit("alice", 1000)
        with self.assertRaises(SameAccountTransfer):
            self.bank.transfer("alice", "alice", 100)

    def test_transfer_insufficient_funds(self) -> None:
        self.bank.create_account("alice")
        self.bank.create_account("bob")
        self.bank.deposit("alice", 100)
        with self.assertRaises(InsufficientFunds):
            self.bank.transfer("alice", "bob", 200)

    def test_transfer_unknown_src(self) -> None:
        self.bank.create_account("bob")
        with self.assertRaises(AccountNotFound):
            self.bank.transfer("ghost", "bob", 100)

    def test_transfer_unknown_dst(self) -> None:
        self.bank.create_account("alice")
        with self.assertRaises(AccountNotFound):
            self.bank.transfer("alice", "ghost", 100)

    def test_transfer_invalid_amount(self) -> None:
        self.bank.create_account("alice")
        self.bank.create_account("bob")
        with self.assertRaises(InvalidAmount):
            self.bank.transfer("alice", "bob", 0)

    def test_transfer_does_not_mutate_on_insufficient(self) -> None:
        """Source balance must be unchanged after a failed transfer."""
        self.bank.create_account("alice")
        self.bank.create_account("bob")
        self.bank.deposit("alice", 100)
        with self.assertRaises(InsufficientFunds):
            self.bank.transfer("alice", "bob", 200)
        self.assertEqual(self.bank.get_balance("alice"), 100)
        self.assertEqual(self.bank.get_balance("bob"), 0)

    # -- get_balance ---------------------------------------------------

    def test_get_balance_unknown_account(self) -> None:
        with self.assertRaises(AccountNotFound):
            self.bank.get_balance("ghost")


if __name__ == "__main__":
    unittest.main()
