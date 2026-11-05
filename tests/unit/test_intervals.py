import numpy as np

from biofeedback.features.intervals import ibi_ms, mean_hr_bpm, tachogram


def test_ibi_ms_basic():
    beats = np.array([0.0, 0.8, 1.6, 2.4])
    assert np.allclose(ibi_ms(beats), [800.0, 800.0, 800.0])


def test_ibi_ms_short_input():
    assert len(ibi_ms(np.array([1.0]))) == 0


def test_mean_hr_bpm():
    # 800 ms IBI -> 75 bpm
    assert abs(mean_hr_bpm(np.array([800.0, 800.0, 800.0])) - 75.0) < 1e-9


def test_tachogram_midpoints():
    beats = np.array([0.0, 1.0, 2.0])
    mids, intervals = tachogram(beats)
    assert np.allclose(mids, [0.5, 1.5])
    assert np.allclose(intervals, [1000.0, 1000.0])
