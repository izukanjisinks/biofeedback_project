from __future__ import annotations

from pathlib import Path
from typing import Any

from biofeedback.acquisition.base import SignalRecord, SignalSource
from biofeedback.acquisition.wfdb_loader import (
    BIDMCSource,
    FantasiaSource,
    MITBIHSource,
)

_SOURCES: dict[str, type[SignalSource]] = {
    "bidmc": BIDMCSource,
    "fantasia": FantasiaSource,
    "mitdb": MITBIHSource,
}


def available() -> list[str]:
    return sorted(_SOURCES)


def get_source(
    name: str,
    data_dir: str | Path | None = None,
    pn_dir: str | None = None,
) -> SignalSource:
    try:
        cls = _SOURCES[name]
    except KeyError as exc:
        raise KeyError(f"unknown source {name!r}; available: {available()}") from exc
    return cls(data_dir=data_dir, pn_dir=pn_dir)


def load(
    source: str,
    record_id: str,
    data_dir: str | Path | None = None,
    pn_dir: str | None = None,
    **kwargs: Any,
) -> SignalRecord:
    return get_source(source, data_dir=data_dir, pn_dir=pn_dir).load(record_id, **kwargs)
