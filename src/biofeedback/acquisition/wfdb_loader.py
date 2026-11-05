from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import wfdb

from biofeedback.acquisition.base import SignalRecord, SignalSource


class WFDBSource(SignalSource):
    name = "wfdb"

    def __init__(self, data_dir: str | Path | None = None, pn_dir: str | None = None):
        if (data_dir is None) == (pn_dir is None):
            raise ValueError("Provide exactly one of data_dir or pn_dir")
        self.data_dir = Path(data_dir) if data_dir is not None else None
        self.pn_dir = pn_dir

    def load(
        self,
        record_id: str,
        channel: str | int | None = None,
        sampto: int | None = None,
        **_: Any,
    ) -> SignalRecord:
        if self.data_dir is not None:
            record = wfdb.rdrecord(str(self.data_dir / record_id), sampto=sampto)
        else:
            record = wfdb.rdrecord(record_id, pn_dir=self.pn_dir, sampto=sampto)

        signal = np.asarray(record.p_signal)
        channel_idx = self._resolve_channel(channel, record.sig_name)
        if channel_idx is not None:
            signal = signal[:, channel_idx]

        meta: dict[str, Any] = {
            "record_id": record_id,
            "sig_name": list(record.sig_name),
            "units": list(record.units),
            "n_sig": record.n_sig,
            "sig_len": record.sig_len,
            "comments": list(record.comments or []),
        }
        if channel_idx is not None:
            meta["channel"] = record.sig_name[channel_idx]

        return SignalRecord(signal=signal, fs=float(record.fs), meta=meta)

    @staticmethod
    def _resolve_channel(
        channel: str | int | None, sig_names: list[str]
    ) -> int | None:
        if channel is None:
            return None
        if isinstance(channel, int):
            return channel
        try:
            return sig_names.index(channel)
        except ValueError as exc:
            raise ValueError(
                f"channel {channel!r} not found; available: {sig_names}"
            ) from exc


class BIDMCSource(WFDBSource):
    name = "bidmc"


class FantasiaSource(WFDBSource):
    name = "fantasia"


class MITBIHSource(WFDBSource):
    name = "mitdb"
