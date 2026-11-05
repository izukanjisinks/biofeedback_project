import numpy as np
import pytest

from biofeedback.acquisition import SignalRecord
from biofeedback.acquisition.registry import available, get_source


def test_signal_record_accepts_1d():
    rec = SignalRecord(signal=np.zeros(100), fs=125.0)
    assert rec.signal.shape == (100,)
    assert rec.fs == 125.0
    assert rec.meta == {}


def test_signal_record_accepts_2d():
    rec = SignalRecord(signal=np.zeros((100, 2)), fs=250.0, meta={"a": 1})
    assert rec.signal.shape == (100, 2)
    assert rec.meta == {"a": 1}


def test_signal_record_rejects_bad_shape():
    with pytest.raises(ValueError):
        SignalRecord(signal=np.zeros((2, 2, 2)), fs=100.0)


def test_signal_record_rejects_bad_fs():
    with pytest.raises(ValueError):
        SignalRecord(signal=np.zeros(10), fs=0.0)


def test_registry_lists_known_sources():
    names = available()
    assert "bidmc" in names
    assert "fantasia" in names
    assert "mitdb" in names


def test_registry_rejects_unknown_source():
    with pytest.raises(KeyError):
        get_source("nope", data_dir=".")


def test_wfdb_source_requires_exactly_one_location():
    with pytest.raises(ValueError):
        get_source("bidmc")  # neither data_dir nor pn_dir
    with pytest.raises(ValueError):
        get_source("bidmc", data_dir=".", pn_dir="bidmc")
