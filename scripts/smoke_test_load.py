"""Fetch one BIDMC record from PhysioNet and print what came back.

Usage:
    python scripts/smoke_test_load.py              # defaults to bidmc01, first 10 s
    python scripts/smoke_test_load.py bidmc05 30   # record_id, seconds to load
"""
from __future__ import annotations

import sys

from biofeedback.acquisition import load


def main(record_id: str = "bidmc01", seconds: float = 10.0) -> int:
    fs_hint = 125  # BIDMC
    sampto = int(seconds * fs_hint)

    print(f"Fetching {record_id!r} from PhysioNet (first {seconds:g} s)...")
    rec = load("bidmc", record_id, pn_dir="bidmc", sampto=sampto)

    print()
    print(f"signal shape   : {rec.signal.shape}")
    print(f"sampling rate  : {rec.fs} Hz")
    print(f"channels       : {rec.meta['sig_name']}")
    print(f"units          : {rec.meta['units']}")
    print(f"total record   : {rec.meta['sig_len']} samples")
    print()
    print("OK — loader works end-to-end against PhysioNet.")
    return 0


if __name__ == "__main__":
    record_id = sys.argv[1] if len(sys.argv) > 1 else "bidmc01"
    seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
    sys.exit(main(record_id, seconds))
