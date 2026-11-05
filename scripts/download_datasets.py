"""Download PhysioNet datasets to data/raw/ for offline use.

Datasets are downloaded once and then read locally by the pipeline.
This script is manual: the app itself never pulls data from the network.

Examples:
    python scripts/download_datasets.py bidmc
    python scripts/download_datasets.py bidmc --records bidmc01 bidmc02 bidmc03
    python scripts/download_datasets.py fantasia --records f1y01 f1o01
    python scripts/download_datasets.py mitdb --records 100 119

Pass --all with no --records to pull the whole dataset. BIDMC is ~250 MB,
Fantasia ~800 MB, MIT-BIH ~100 MB — fine on a laptop, slow on metered links.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import wfdb

PN_SLUG = {
    "bidmc": "bidmc",
    "fantasia": "fantasia",
    "mitdb": "mitdb",
    "nstdb": "nstdb",
}

DEFAULT_RECORDS = {
    "bidmc": ["bidmc01", "bidmc02", "bidmc05"],
    "fantasia": ["f1y01", "f1o01"],
    "mitdb": ["100", "119"],
    "nstdb": ["118e24", "118e00"],
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("dataset", choices=sorted(PN_SLUG), help="dataset short name")
    parser.add_argument("--records", nargs="+", help="record ids to download")
    parser.add_argument("--all", action="store_true", help="download the whole dataset")
    parser.add_argument("--out", default="data/raw", help="destination root (default: data/raw)")
    args = parser.parse_args()

    out_dir = Path(args.out) / args.dataset
    out_dir.mkdir(parents=True, exist_ok=True)

    pn_dir = PN_SLUG[args.dataset]

    if args.all and args.records:
        parser.error("choose --all OR --records, not both")

    if args.all:
        print(f"Downloading entire {args.dataset} dataset -> {out_dir}")
        wfdb.dl_database(pn_dir, dl_dir=str(out_dir))
    else:
        records = args.records or DEFAULT_RECORDS[args.dataset]
        print(f"Downloading {len(records)} record(s) from {args.dataset} -> {out_dir}")
        wfdb.dl_database(pn_dir, dl_dir=str(out_dir), records=records)

    print()
    print(f"Done. Loaded files in: {out_dir.resolve()}")
    print("Verify with:")
    print(f'  python -c "from biofeedback.acquisition import load; '
          f'r = load({args.dataset!r}, {(args.records or DEFAULT_RECORDS[args.dataset])[0]!r}, '
          f'data_dir={str(out_dir)!r}); print(r.signal.shape, r.fs)"')
    return 0


if __name__ == "__main__":
    sys.exit(main())
