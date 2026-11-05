"""Run the full M2 pipeline on a local BIDMC record and compare to NeuroKit2.

Usage:
    python scripts/smoke_test_features.py                      # bidmc01
    python scripts/smoke_test_features.py bidmc02

The record must already be downloaded to data/raw/bidmc/.
"""
from __future__ import annotations

import sys

import numpy as np

from biofeedback.acquisition import load
from biofeedback.features import extract_from_ecg, extract_from_ppg


def _nk_reference(signal: np.ndarray, fs: float, kind: str) -> dict:
    import neurokit2 as nk

    if kind == "ppg":
        clean = nk.ppg_clean(signal, sampling_rate=fs)
        info = nk.ppg_findpeaks(clean, sampling_rate=fs, method="elgendi")
        peaks = info["PPG_Peaks"]
    else:
        _, info = nk.ecg_peaks(nk.ecg_clean(signal, sampling_rate=fs), sampling_rate=fs)
        peaks = info["ECG_R_Peaks"]
    hrv = nk.hrv_time(peaks, sampling_rate=fs, show=False)
    return {
        "mean_hr_bpm": 60000.0 / np.mean(np.diff(peaks) / fs * 1000.0),
        "rmssd_ms": float(hrv["HRV_RMSSD"].iloc[0]),
        "sdnn_ms": float(hrv["HRV_SDNN"].iloc[0]),
        "pnn50_pct": float(hrv["HRV_pNN50"].iloc[0]),
        "n_beats": len(peaks),
    }


def run(record_id: str) -> int:
    for channel, kind, extract in (
        ("PLETH", "ppg", extract_from_ppg),
        ("II", "ecg", extract_from_ecg),
    ):
        print(f"\n=== {record_id} · channel {channel} ({kind.upper()}) ===")
        rec = load("bidmc", record_id, data_dir="data/raw/bidmc", channel=channel)
        fs = rec.fs

        ours = extract(rec.signal, fs)
        theirs = _nk_reference(rec.signal, fs, kind)

        print(f"{'':16} {'ours':>12} {'nk ref':>12} {'delta':>12}")
        for key in ("n_beats", "mean_hr_bpm", "rmssd_ms", "sdnn_ms", "pnn50_pct"):
            a = getattr(ours, key) if hasattr(ours, key) else ours.summary()[key]
            b = theirs[key]
            delta = (a - b) if isinstance(a, int | float) and isinstance(b, int | float) else "n/a"
            print(f"{key:16} {a:>12.3f} {b:>12.3f} {delta:>12.3f}")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    record_id = sys.argv[1] if len(sys.argv) > 1 else "bidmc01"
    sys.exit(run(record_id))
