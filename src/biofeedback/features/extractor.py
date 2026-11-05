from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from biofeedback.features import hrv_nonlinear, hrv_time, intervals
from biofeedback.features.beat_detection import detect_ecg_peaks, detect_ppg_peaks
from biofeedback.features.sub_sample import parabolic_refine
from biofeedback.preprocessing.filters import bandpass, notch


@dataclass(frozen=True)
class FeatureSet:
    mean_hr_bpm: float
    rmssd_ms: float
    sdnn_ms: float
    pnn50_pct: float
    sd1_ms: float
    sd2_ms: float
    n_beats: int
    beat_times_s: np.ndarray = field(repr=False)
    ibi_ms: np.ndarray = field(repr=False)
    source: str = ""

    def summary(self) -> dict[str, float | int | str]:
        return {
            "source": self.source,
            "n_beats": self.n_beats,
            "mean_hr_bpm": round(self.mean_hr_bpm, 2),
            "rmssd_ms": round(self.rmssd_ms, 2),
            "sdnn_ms": round(self.sdnn_ms, 2),
            "pnn50_pct": round(self.pnn50_pct, 2),
            "sd1_ms": round(self.sd1_ms, 2),
            "sd2_ms": round(self.sd2_ms, 2),
        }


def _features_from_beat_times(beat_times_s: np.ndarray, source: str) -> FeatureSet:
    ibi = intervals.ibi_ms(beat_times_s)
    sd1, sd2 = hrv_nonlinear.sd1_sd2(ibi)
    return FeatureSet(
        mean_hr_bpm=intervals.mean_hr_bpm(ibi),
        rmssd_ms=hrv_time.rmssd(ibi),
        sdnn_ms=hrv_time.sdnn(ibi),
        pnn50_pct=hrv_time.pnn50(ibi),
        sd1_ms=sd1,
        sd2_ms=sd2,
        n_beats=len(beat_times_s),
        beat_times_s=beat_times_s,
        ibi_ms=ibi,
        source=source,
    )


def extract_from_ppg(
    signal: np.ndarray,
    fs: float,
    *,
    band: tuple[float, float] = (0.5, 8.0),
    mains_hz: float | None = 50.0,
) -> FeatureSet:
    filtered = bandpass(signal, fs, band[0], band[1])
    if mains_hz is not None and mains_hz < 0.5 * fs:
        filtered = notch(filtered, fs, mains_hz)
    peaks = detect_ppg_peaks(filtered, fs)
    beat_times = parabolic_refine(filtered, peaks, fs)
    return _features_from_beat_times(beat_times, source="ppg")


def extract_from_ecg(
    signal: np.ndarray,
    fs: float,
    *,
    mains_hz: float | None = 50.0,
) -> FeatureSet:
    prepared = signal
    if mains_hz is not None and mains_hz < 0.5 * fs:
        prepared = notch(prepared, fs, mains_hz)
    peaks = detect_ecg_peaks(prepared, fs)
    beat_times = parabolic_refine(prepared, peaks, fs)
    return _features_from_beat_times(beat_times, source="ecg")
