from __future__ import annotations

import numpy as np
from scipy.signal import butter, filtfilt, iirnotch


def bandpass(
    signal: np.ndarray,
    fs: float,
    low_hz: float,
    high_hz: float,
    order: int = 4,
) -> np.ndarray:
    nyq = 0.5 * fs
    if not 0 < low_hz < high_hz < nyq:
        raise ValueError(
            f"require 0 < low_hz < high_hz < {nyq} (Nyquist); got {low_hz}, {high_hz}"
        )
    b, a = butter(order, [low_hz / nyq, high_hz / nyq], btype="band")
    return filtfilt(b, a, signal)


def notch(
    signal: np.ndarray,
    fs: float,
    freq_hz: float = 50.0,
    q: float = 30.0,
) -> np.ndarray:
    nyq = 0.5 * fs
    if not 0 < freq_hz < nyq:
        raise ValueError(f"freq_hz must be between 0 and {nyq}, got {freq_hz}")
    b, a = iirnotch(freq_hz / nyq, q)
    return filtfilt(b, a, signal)
