"""Level 1 — Basic Bank.

Single dict mapping account_id -> balance (integer cents).
All operations validate inputs and raise explicit exceptions.
"""

from .core import (
    AccountNotFound,
    DuplicateAccount,
    InsufficientFunds,
    InvalidAmount,
    SameAccountTransfer,
)


class BankLevel1:
    """Simple bank backed by a ``dict[str, int]`` of balances in cents."""

    def __init__(self) -> None:
        self._accounts: dict[str, int] = {}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate_amount(self, amount: int) -> None:
        if not isinstance(amount, int) or amount <= 0:
            raise InvalidAmount(amount)

    def _require_account(self, account_id: str) -> None:
        if account_id not in self._accounts:
            raise AccountNotFound(account_id)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create_account(self, account_id: str) -> None:
        """Create an account with zero balance.  Raises on duplicate."""
        if account_id in self._accounts:
            raise DuplicateAccount(account_id)
        self._accounts[account_id] = 0

    def deposit(self, account_id: str, amount: int) -> int:
        """Deposit *amount* cents.  Returns the new balance."""
        self._require_account(account_id)
        self._validate_amount(amount)
        self._accounts[account_id] += amount
        return self._accounts[account_id]

    def withdraw(self, account_id: str, amount: int) -> int:
        """Withdraw *amount* cents.  Returns the new balance."""
        self._require_account(account_id)
        self._validate_amount(amount)
        balance = self._accounts[account_id]
        if balance < amount:
            raise InsufficientFunds(account_id, balance, amount)
        self._accounts[account_id] -= amount
        return self._accounts[account_id]

    def transfer(self, src_id: str, dst_id: str, amount: int) -> tuple[int, int]:
        """Transfer *amount* cents from *src_id* to *dst_id*.

        Returns ``(src_balance, dst_balance)`` after the transfer.
        """
        if src_id == dst_id:
            raise SameAccountTransfer(src_id)
        self._require_account(src_id)
        self._require_account(dst_id)
        self._validate_amount(amount)
        if self._accounts[src_id] < amount:
            raise InsufficientFunds(src_id, self._accounts[src_id], amount)
        self._accounts[src_id] -= amount
        self._accounts[dst_id] += amount
        return self._accounts[src_id], self._accounts[dst_id]

    def get_balance(self, account_id: str) -> int:
        """Return the current balance in cents."""
        self._require_account(account_id)
        return self._accounts[account_id]
