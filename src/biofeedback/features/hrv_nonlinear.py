from __future__ import annotations

import numpy as np


def sd1_sd2(ibi_ms: np.ndarray) -> tuple[float, float]:
    """Return Poincaré plot SD1 and SD2 (ms).

    Uses the rotated Poincaré formulation (std along the ellipse axes),
    matching NeuroKit2 and Kubios.
    """
    ibi = np.asarray(ibi_ms, dtype=float)
    if len(ibi) < 3:
        return float("nan"), float("nan")
    x = ibi[:-1]
    y = ibi[1:]
    sd1 = float(np.std((x - y) / np.sqrt(2.0), ddof=1))
    sd2 = float(np.std((x + y) / np.sqrt(2.0), ddof=1))
    return sd1, sd2
