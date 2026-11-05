from __future__ import annotations

import numpy as np


def _require_neurokit2():
    try:
        import neurokit2 as nk
    except ImportError as exc:
        raise ImportError(
            "neurokit2 is required for beat detection. "
            'Install it with: pip install -e ".[features]"'
        ) from exc
    return nk


def detect_ppg_peaks(signal: np.ndarray, fs: float) -> np.ndarray:
    """Return sample indices of systolic peaks in a cleaned PPG signal.

    Uses the Elgendi detector via NeuroKit2. The input should already be
    band-pass filtered; no cleaning is performed here.
    """
    nk = _require_neurokit2()
    info = nk.ppg_findpeaks(signal, sampling_rate=fs, method="elgendi")
    return np.asarray(info["PPG_Peaks"], dtype=int)


def detect_ecg_peaks(signal: np.ndarray, fs: float, method: str = "pantompkins1985") -> np.ndarray:
    """Return sample indices of R-peaks.

    NeuroKit2 handles cleaning and detection internally.
    """
    nk = _require_neurokit2()
    cleaned = nk.ecg_clean(signal, sampling_rate=fs, method="pantompkins1985")
    _, info = nk.ecg_peaks(cleaned, sampling_rate=fs, method=method)
    return np.asarray(info["ECG_R_Peaks"], dtype=int)
