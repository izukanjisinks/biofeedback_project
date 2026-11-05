import math

import numpy as np

from biofeedback.features.hrv_nonlinear import sd1_sd2
from biofeedback.features.hrv_time import pnn50, rmssd, sdnn


def test_rmssd_known_value():
    # successive diffs: [100, 100, 100] -> RMSSD = 100
    ibi = np.array([700.0, 800.0, 900.0, 1000.0])
    assert abs(rmssd(ibi) - 100.0) < 1e-9


def test_sdnn_known_value():
    ibi = np.array([800.0, 900.0, 1000.0])
    # sample std with ddof=1 of [800, 900, 1000] = 100
    assert abs(sdnn(ibi) - 100.0) < 1e-9


def test_pnn50_all_above():
    ibi = np.array([700.0, 800.0, 900.0, 1000.0])  # diffs all 100 ms
    assert pnn50(ibi) == 100.0


def test_pnn50_none_above():
    ibi = np.array([800.0, 810.0, 820.0, 830.0])  # diffs all 10 ms
    assert pnn50(ibi) == 0.0


def test_sd1_sd2_match_poincare_formula():
    rng = np.random.default_rng(0)
    ibi = 800.0 + 40.0 * rng.standard_normal(500)
    sd1, sd2 = sd1_sd2(ibi)
    # Independently compute via rotation of the Poincaré plot.
    x = ibi[:-1]
    y = ibi[1:]
    sd1_ref = float(np.std((x - y) / math.sqrt(2.0), ddof=1))
    sd2_ref = float(np.std((x + y) / math.sqrt(2.0), ddof=1))
    assert abs(sd1 - sd1_ref) < 1e-6
    assert abs(sd2 - sd2_ref) < 1e-6
