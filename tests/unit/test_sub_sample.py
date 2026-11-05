import numpy as np

from biofeedback.features.sub_sample import parabolic_refine


def test_parabolic_refine_on_exact_parabola():
    # f(x) = -(x - 5.3)^2 + 10 sampled at integer x; vertex at 5.3
    x = np.arange(0, 11, 1.0)
    y = -((x - 5.3) ** 2) + 10.0
    fs = 1.0
    # nearest integer peak is x=5
    times = parabolic_refine(y, np.array([5]), fs)
    assert abs(times[0] - 5.3) < 1e-6


def test_parabolic_refine_boundary_peaks():
    y = np.array([1.0, 2.0, 3.0])
    # peak at index 0 or last -> returned unrefined
    times = parabolic_refine(y, np.array([0, 2]), fs=10.0)
    assert np.allclose(times, [0.0, 0.2])
