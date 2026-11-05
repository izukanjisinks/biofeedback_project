import numpy as np
import pytest

from biofeedback.preprocessing.filters import bandpass, notch


def test_bandpass_removes_dc():
    fs = 250.0
    t = np.arange(0, 10, 1 / fs)
    sig = np.ones_like(t) * 5.0 + 0.1 * np.sin(2 * np.pi * 2.0 * t)
    out = bandpass(sig, fs, 0.5, 8.0)
    # DC input mean was 5.0; after band-pass the mean should be hugely
    # attenuated (allow small edge-effect residual from filtfilt).
    assert abs(out.mean()) < 0.01
    # And the 2 Hz in-band component should survive (RMS close to 0.1/sqrt(2)).
    rms = float(np.sqrt(np.mean(out**2)))
    assert 0.05 < rms < 0.1


def test_bandpass_rejects_bad_band():
    with pytest.raises(ValueError):
        bandpass(np.zeros(100), fs=100.0, low_hz=5.0, high_hz=4.0)
    with pytest.raises(ValueError):
        bandpass(np.zeros(100), fs=100.0, low_hz=0.0, high_hz=10.0)


def test_notch_attenuates_mains():
    fs = 500.0
    t = np.arange(0, 5, 1 / fs)
    sig = np.sin(2 * np.pi * 50.0 * t) + 0.5 * np.sin(2 * np.pi * 5.0 * t)
    out = notch(sig, fs, freq_hz=50.0, q=30.0)
    # 50 Hz component should be strongly attenuated vs the 5 Hz component.
    fft_in = np.abs(np.fft.rfft(sig))
    fft_out = np.abs(np.fft.rfft(out))
    freqs = np.fft.rfftfreq(len(sig), 1 / fs)
    idx_50 = np.argmin(np.abs(freqs - 50.0))
    idx_5 = np.argmin(np.abs(freqs - 5.0))
    assert fft_out[idx_50] < 0.1 * fft_in[idx_50]
    assert fft_out[idx_5] > 0.9 * fft_in[idx_5]
