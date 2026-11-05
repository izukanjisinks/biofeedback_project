# Biofeedback

Low-cost, offline-first biofeedback prototype that uses heart rate (PPG or ECG)
to guide paced-breathing exercises for hypertension self-management.

Scope: **technical feasibility and physiological response**, not clinical
effectiveness.

## Status

Phase 1, Milestone 1: foundations. Package installs; a WFDB recording loads
into a known shape.

## Install

```bash
python -m venv .venv
. .venv/Scripts/activate      # Windows
pip install -e ".[dev]"
```

## Load a recording

```python
from biofeedback.acquisition import load

record = load("bidmc", "bidmc01", data_dir="data/raw/bidmc")
print(record.signal.shape, record.fs, record.meta)
```

## Documentation

- [Project summary](project_summary.md)
- [Roadmap](docs/roadmap.md)
- [Datasets](docs/datasets.md)
- [Structure](docs/project_structure.txt)
- [Gap list](docs/structure_gaps.md)
