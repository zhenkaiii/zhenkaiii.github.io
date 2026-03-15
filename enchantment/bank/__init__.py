"""Banking system with 4 levels of increasing complexity."""

from .core import (
    AccountNotFound,
    BankError,
    DuplicateAccount,
    DuplicateTransactionId,
    IdempotencyConflict,
    InsufficientFunds,
    InvalidAmount,
    SameAccountTransfer,
)
from .level1_basic import BankLevel1
from .level2_batch_atomic import BankLevel2
from .level3_scheduler_priority import BankLevel3
from .level4_audit_idempotency import BankLevel4

__all__ = [
    "BankError",
    "AccountNotFound",
    "DuplicateAccount",
    "InsufficientFunds",
    "InvalidAmount",
    "SameAccountTransfer",
    "DuplicateTransactionId",
    "IdempotencyConflict",
    "BankLevel1",
    "BankLevel2",
    "BankLevel3",
    "BankLevel4",
]
