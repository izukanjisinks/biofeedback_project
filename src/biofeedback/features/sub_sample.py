from __future__ import annotations

import numpy as np


def parabolic_refine(signal: np.ndarray, peak_indices: np.ndarray, fs: float) -> np.ndarray:
    """Refine integer peak sample indices to sub-sample beat times (seconds).

    Fits a parabola through each peak and its two neighbours and returns
    the vertex's time. Peaks at the first or last sample are returned
    unrefined.
    """
    if signal.ndim != 1:
        raise ValueError(f"signal must be 1-D, got shape {signal.shape}")
    if fs <= 0:
        raise ValueError(f"fs must be positive, got {fs}")

    times = np.empty(len(peak_indices), dtype=float)
    last = len(signal) - 1
    for k, i in enumerate(peak_indices):
        if i <= 0 or i >= last:
            times[k] = i / fs
            continue
        y0, y1, y2 = signal[i - 1], signal[i], signal[i + 1]
        denom = y0 - 2.0 * y1 + y2
        offset = 0.5 * (y0 - y2) / denom if denom != 0 else 0.0
        times[k] = (i + offset) / fs
    return times
