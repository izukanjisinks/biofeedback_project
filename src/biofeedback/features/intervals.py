from __future__ import annotations

import numpy as np


def ibi_ms(beat_times_s: np.ndarray) -> np.ndarray:
    if len(beat_times_s) < 2:
        return np.array([], dtype=float)
    return np.diff(np.asarray(beat_times_s, dtype=float)) * 1000.0


def tachogram(beat_times_s: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return (midpoint_times_s, ibi_ms) for plotting IBIs against time."""
    beats = np.asarray(beat_times_s, dtype=float)
    if len(beats) < 2:
        return np.array([]), np.array([])
    midpoints = 0.5 * (beats[:-1] + beats[1:])
    return midpoints, ibi_ms(beats)


def mean_hr_bpm(ibi_ms: np.ndarray) -> float:
    if len(ibi_ms) == 0:
        return float("nan")
    return float(60000.0 / np.mean(ibi_ms))
