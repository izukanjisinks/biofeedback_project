import pytest

from biofeedback.preprocessing.windows import sliding_windows


def test_non_overlapping():
    wins = list(sliding_windows(n_samples=10, window_size=3))
    assert wins == [(0, 3), (3, 6), (6, 9)]


def test_with_step():
    wins = list(sliding_windows(n_samples=10, window_size=4, step=2))
    assert wins == [(0, 4), (2, 6), (4, 8), (6, 10)]


def test_window_larger_than_signal_yields_nothing():
    wins = list(sliding_windows(n_samples=5, window_size=10))
    assert wins == []


def test_bad_args():
    with pytest.raises(ValueError):
        list(sliding_windows(n_samples=10, window_size=0))
    with pytest.raises(ValueError):
        list(sliding_windows(n_samples=10, window_size=4, step=0))
