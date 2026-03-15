"""Core exceptions for the banking system.

All balances and amounts are in integer cents (no floats).
"""


class BankError(Exception):
    """Base exception for all banking errors."""


class AccountNotFound(BankError):
    """Raised when an operation references a non-existent account."""

    def __init__(self, account_id: str) -> None:
        super().__init__(f"Account not found: {account_id!r}")
        self.account_id = account_id


class DuplicateAccount(BankError):
    """Raised when creating an account that already exists."""

    def __init__(self, account_id: str) -> None:
        super().__init__(f"Account already exists: {account_id!r}")
        self.account_id = account_id


class InvalidAmount(BankError):
    """Raised when an amount is not a positive integer."""

    def __init__(self, amount: object) -> None:
        super().__init__(f"Amount must be a positive integer, got {amount!r}")
        self.amount = amount


class InsufficientFunds(BankError):
    """Raised when a withdrawal or transfer exceeds available balance."""

    def __init__(self, account_id: str, balance: int, amount: int) -> None:
        super().__init__(
            f"Insufficient funds in {account_id!r}: "
            f"balance={balance}, requested={amount}"
        )
        self.account_id = account_id
        self.balance = balance
        self.amount = amount


class SameAccountTransfer(BankError):
    """Raised when source and destination of a transfer are the same."""

    def __init__(self, account_id: str) -> None:
        super().__init__(f"Cannot transfer to the same account: {account_id!r}")
        self.account_id = account_id


class DuplicateTransactionId(BankError):
    """Raised when a scheduled transaction ID is reused."""

    def __init__(self, tx_id: str) -> None:
        super().__init__(f"Duplicate transaction ID: {tx_id!r}")
        self.tx_id = tx_id


class IdempotencyConflict(BankError):
    """Raised when an idempotency key is reused with different parameters."""

    def __init__(self, idem_key: str) -> None:
        super().__init__(
            f"Idempotency key {idem_key!r} already used with different parameters"
        )
        self.idem_key = idem_key
