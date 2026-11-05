# Roadmap

Milestones for building the biofeedback prototype. Phase 1 is sensor-free;
Phase 2 adds hardware.

## Phase 1 — Recorded data (no hardware)

### M1 — Foundations
**Goal:** the project runs; recorded data loads.

**Build:**
- Repo scaffolding: `pyproject.toml`, `.pre-commit-config.yaml`, base configs.
- `acquisition/base.py`, `acquisition/wfdb_loader.py`, `acquisition/registry.py`.
- Dataset provenance: `docs/datasets.md` + `notebooks/00_data_provenance.ipynb`.

**Done when:** a WFDB recording from the chosen subset loads into a known
`(signal, fs, meta)` shape from a Python REPL.

### M2 — Signal processing
**Goal:** find heartbeats, compute HR and HRV from a recording.

**Build:**
- `preprocessing/filters.py`, `preprocessing/windows.py`.
- `features/beat_detection.py` (Elgendi / Pan–Tompkins).
- `features/sub_sample.py`, `features/intervals.py`.
- `features/hrv_time.py`, `features/hrv_nonlinear.py`.
- `features/extractor.py`.

**Done when:** on a BIDMC recording with reference beats, HR MAE < 2 bpm
across the chosen subset; RMSSD and SDNN computed and sanity-checked against
NeuroKit2.

### M3 — Quality gate + evaluation
**Goal:** the pipeline refuses to compute on bad signal, and we can prove it.

**Build:**
- `preprocessing/sqi.py`, `preprocessing/quality_gate.py`,
  `preprocessing/artifact.py`.
- `tests/fixtures/synthetic_signals.py` + `tests/unit/test_quality_gate.py`.
- `evaluation/sqi_benchmark.py`, `evaluation/hr_accuracy.py`,
  `evaluation/prv_vs_hrv.py`.

**Done when:** noise-injection benchmark (NSTDB) shows the gate rejects
windows at the configured threshold with expected precision/recall; HR
accuracy and PRV-vs-HRV reports regenerate from a single script.

### M4 — Session layer
**Goal:** a session has structure (baseline → paced → recovery), is saved,
and produces a shareable report.

**Build:**
- `feedback/pacer.py`, `feedback/state.py`, `feedback/renderers/visual.py`.
- `session/baseline.py`, `session/protocol.py`.
- `session/models.py`, `session/store.py`, `session/history.py`,
  `session/export.py`.

**Done when:** running a session on a recording writes a row to SQLite with
before/after HR & HRV, SQI stats, and corrected-beat count; CSV + HTML export
opens and reads cleanly.

### M5 — End-to-end "live-feeling" demo
**Goal:** experience the full biofeedback flow on recorded data.

**Build:**
- `evaluation/rsa_response.py`, `evaluation/timing_accuracy.py`,
  `evaluation/report.py`.
- `feedback/rsa_tracker.py`, `feedback/renderers/audio.py` (optional).
- `app/run_session.py`, `app/run_eval.py`, `app/cli.py`.

**Done when:** `biofeedback run-session --recording <path>` plays the
recording at wall-clock speed, shows the pacer, logs the session, and the
RSA tracker shows visible HR oscillation during the paced segment.

## Phase 2 — Live sensor

### M6 — Sensor decision
**Goal:** pick the hardware.

**Done when:** sensor ordered and `docs/decisions/adr-001-live-sensor.md`
updated with the choice, rationale, and sampling characteristics.

### M7 — Integration
**Goal:** live heartbeat flows into the same pipeline as recorded data.

**Build:**
- Fill in `acquisition/live_source.py`.
- Streaming plumbing (ring buffer, chunk iterator) — deferred from
  structure_gaps.md gap 3, now required.

**Done when:** a session can be driven by the sensor instead of a recording,
with the quality gate pausing feedback on bad signal in real time.

### M8 — Field test
**Goal:** one real user, repeated sessions, exports shared with a health
worker.

**Done when:** at least one user completes an agreed number of sessions
over an agreed period; exports reviewed by a health worker; scope and
limits of the data explicitly stated in the session summary.
