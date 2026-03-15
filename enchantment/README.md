# Banking System — Interview Warmup

A 4-level progressive banking system in pure Python (no external deps).
Each level builds on the previous, adding complexity while keeping code
interview-friendly: short functions, explicit errors, simple data structures.

## Levels

| Level | Module | Key idea | Data structure |
|-------|--------|----------|----------------|
| 1 | `level1_basic.py` | Create, deposit, withdraw, transfer, get_balance | `dict[str, int]` |
| 2 | `level2_batch_atomic.py` | Atomic batch ops — all-or-nothing with snapshot rollback | dict + snapshot copy |
| 3 | `level3_scheduler_priority.py` | Scheduled transfers ordered by (time, priority, insertion) | `heapq` min-heap |
| 4 | `level4_audit_idempotency.py` | Append-only audit log + idempotency keys | list + dict |

All balances are **integer cents** (no floats). Account IDs are strings.

## Run tests

```bash
cd enchantment
python -m unittest discover -s tests -v
```

Or a single level:

```bash
python -m unittest tests.test_level3 -v
```

## Run the demo

```bash
python demo.py
```

## Quick usage

```python
from bank import BankLevel4

bank = BankLevel4()
bank.create_account("alice")
bank.create_account("bob")

bank.deposit("alice", 100_00)                              # $100.00
bank.transfer("alice", "bob", 25_00, idem_key="xfer-001")  # safe retry

# Schedule a future transfer
bank.schedule_transfer("tx1", when_ts=1000, src="alice", dst="bob",
                       amount=5_00, priority=1)
results = bank.run_due(now_ts=1000)

# Inspect audit trail
for entry in bank.get_audit_log(limit=5):
    print(entry)
```

## Project structure

```
enchantment/
  demo.py
  bank/
    __init__.py
    core.py                         # Exceptions
    level1_basic.py                 # dict-based bank
    level2_batch_atomic.py          # atomic batches
    level3_scheduler_priority.py    # heap-based scheduler
    level4_audit_idempotency.py     # audit + idempotency
  tests/
    test_level1.py
    test_level2.py
    test_level3.py
    test_level4.py
```
