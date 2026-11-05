from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass(frozen=True)
class SignalRecord:
    signal: np.ndarray
    fs: float
    meta: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.signal.ndim not in (1, 2):
            raise ValueError(f"signal must be 1-D or 2-D, got shape {self.signal.shape}")
        if self.fs <= 0:
            raise ValueError(f"fs must be positive, got {self.fs}")


class SignalSource(ABC):
    name: str

    @abstractmethod
    def load(self, record_id: str, **kwargs: Any) -> SignalRecord:
        """Return the recording identified by `record_id`."""
