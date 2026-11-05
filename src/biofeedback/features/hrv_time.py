from __future__ import annotations

import numpy as np


def rmssd(ibi_ms: np.ndarray) -> float:
    ibi = np.asarray(ibi_ms, dtype=float)
    if len(ibi) < 2:
        return float("nan")
    return float(np.sqrt(np.mean(np.diff(ibi) ** 2)))


def sdnn(ibi_ms: np.ndarray) -> float:
    ibi = np.asarray(ibi_ms, dtype=float)
    if len(ibi) < 2:
        return float("nan")
    return float(np.std(ibi, ddof=1))


def pnn50(ibi_ms: np.ndarray) -> float:
    ibi = np.asarray(ibi_ms, dtype=float)
    if len(ibi) < 2:
        return float("nan")
    diffs = np.abs(np.diff(ibi))
    return float(100.0 * np.sum(diffs > 50.0) / len(diffs))
