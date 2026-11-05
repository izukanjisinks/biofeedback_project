from __future__ import annotations

from collections.abc import Iterator


def sliding_windows(
    n_samples: int,
    window_size: int,
    step: int | None = None,
) -> Iterator[tuple[int, int]]:
    if window_size <= 0:
        raise ValueError(f"window_size must be positive, got {window_size}")
    step = step if step is not None else window_size
    if step <= 0:
        raise ValueError(f"step must be positive, got {step}")
    start = 0
    while start + window_size <= n_samples:
        yield start, start + window_size
        start += step
