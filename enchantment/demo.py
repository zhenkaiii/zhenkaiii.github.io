#!/usr/bin/env python3
"""Demo runner — walks through all four levels of the banking system."""

from bank import BankLevel4, IdempotencyConflict


def cents_to_usd(c: int) -> str:
    return f"${c / 100:,.2f}"


def main() -> None:
    bank = BankLevel4()

    # ── Level 1: Basic operations ────────────────────────────────────
    print("═══ Level 1: Basic Operations ═══\n")

    bank.create_account("alice")
    bank.create_account("bob")
    bank.create_account("carol")

    bank.deposit("alice", 100_00)   # $100.00
    bank.deposit("bob",    50_00)   # $50.00
    bank.deposit("carol",  25_00)   # $25.00

    print(f"  Alice : {cents_to_usd(bank.get_balance('alice'))}")
    print(f"  Bob   : {cents_to_usd(bank.get_balance('bob'))}")
    print(f"  Carol : {cents_to_usd(bank.get_balance('carol'))}")

    src_bal, dst_bal = bank.transfer("alice", "bob", 25_00)
    print(f"\n  Transfer $25.00 Alice -> Bob")
    print(f"  Alice : {cents_to_usd(src_bal)}")
    print(f"  Bob   : {cents_to_usd(dst_bal)}")

    # ── Level 2: Batch with rollback ─────────────────────────────────
    print("\n═══ Level 2: Atomic Batch ═══\n")

    print("  Batch: deposit $50 to Alice, then transfer $9,999.99 from Bob (will fail).")
    results = bank.apply_batch([
        {"type": "deposit",  "id": "alice", "amount": 50_00},
        {"type": "transfer", "src": "bob", "dst": "alice", "amount": 999_999},
    ])
    for r in results:
        status = "OK" if r["success"] else f"FAIL — {r['error']}"
        print(f"    op {r['op_index']}: {status}")

    print(f"\n  Balances unchanged after rollback:")
    print(f"  Alice : {cents_to_usd(bank.get_balance('alice'))}")
    print(f"  Bob   : {cents_to_usd(bank.get_balance('bob'))}")

    print("\n  Batch: deposit $10 to Alice + withdraw $5 from Bob (both succeed).")
    results = bank.apply_batch([
        {"type": "deposit",  "id": "alice", "amount": 10_00},
        {"type": "withdraw", "id": "bob",   "amount": 5_00},
    ])
    for r in results:
        print(f"    op {r['op_index']}: OK — balance {cents_to_usd(r.get('balance', 0))}")

    print(f"\n  Alice : {cents_to_usd(bank.get_balance('alice'))}")
    print(f"  Bob   : {cents_to_usd(bank.get_balance('bob'))}")

    # ── Level 3: Scheduled transfers ─────────────────────────────────
    print("\n═══ Level 3: Scheduled Transfers ═══\n")

    bank.schedule_transfer("tx-a", when_ts=100, src="alice", dst="carol", amount=5_00, priority=1)
    bank.schedule_transfer("tx-b", when_ts=100, src="bob",   dst="carol", amount=3_00, priority=5)
    bank.schedule_transfer("tx-c", when_ts=200, src="carol", dst="alice", amount=2_00)
    print("  Scheduled tx-a (ts=100, pri=1): Alice -> Carol $5.00")
    print("  Scheduled tx-b (ts=100, pri=5): Bob   -> Carol $3.00")
    print("  Scheduled tx-c (ts=200, pri=0): Carol -> Alice $2.00")

    print("\n  run_due(now=100):")
    for r in bank.run_due(now_ts=100):
        print(f"    {r['tx_id']}: {r['status']}")

    print("\n  run_due(now=200):")
    for r in bank.run_due(now_ts=200):
        print(f"    {r['tx_id']}: {r['status']}")

    print(f"\n  Alice : {cents_to_usd(bank.get_balance('alice'))}")
    print(f"  Bob   : {cents_to_usd(bank.get_balance('bob'))}")
    print(f"  Carol : {cents_to_usd(bank.get_balance('carol'))}")

    # ── Level 4: Idempotency ─────────────────────────────────────────
    print("\n═══ Level 4: Idempotency ═══\n")

    bal1 = bank.deposit("alice", 10_00, idem_key="dep-once")
    bal2 = bank.deposit("alice", 10_00, idem_key="dep-once")  # replay
    print(f"  deposit $10 (key='dep-once'):  balance = {cents_to_usd(bal1)}")
    print(f"  replay  $10 (key='dep-once'):  balance = {cents_to_usd(bal2)}")
    print(f"  Same result, no double-credit: {bal1 == bal2}")

    print()
    try:
        bank.deposit("alice", 99_99, idem_key="dep-once")  # conflict
    except IdempotencyConflict as exc:
        print(f"  Conflict detected: {exc}")

    # ── Audit log ─────────────────────────────────────────────────────
    print("\n═══ Audit Log (last 10 entries) ═══\n")

    for entry in bank.get_audit_log(limit=10):
        ok = "OK" if entry["success"] else "FAIL"
        key = f"  key={entry['idem_key']}" if entry.get("idem_key") else ""
        print(f"  [{entry['ts']:>3}] {entry['op']:<20} {ok}{key}")

    print()


if __name__ == "__main__":
    main()
