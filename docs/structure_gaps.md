# Project Structure — Gap List

Working list of gaps between `project_structure.txt` and `project_summary.md`.
Scope: **Phase 1 only** (recorded datasets, no live sensor, simple batch route).

## Resolved

### 1. Naming collision ✅
Inner `src/biofeedback/biofeedback/` package shared the project name, causing
`biofeedback.biofeedback.pacer` import stutter.

**Fix applied:** renamed to `src/biofeedback/feedback/` and
`feedback_state.py` → `state.py`.

### 2. Respiration slot ✅
`adr-002-respiration.md` referenced an open decision (measure respiration vs.
pace only).

**Resolution:** removed from the structure. Current direction is **pace only**;
no code or ADR slot reserved. Revisit if the decision changes.

### 3. Real-time / streaming module ✅
No ring buffer, chunk iterator, or wall-clock replay path.

**Resolution:** deferred. The **simple Phase 1 route** (load recording →
batch-compute HR/HRV → plot before/during/after) does not require streaming.
Streaming only becomes relevant if a live sensor is added (Phase 2) or if the
pacer needs to run live over a replayed recording.

### 4. `SignalSource.stream()` signature ✅
ABC originally defined as `stream() -> (signal, fs, meta)` — a one-shot tuple
that reads oddly for live use.

**Resolution:** no change needed for Phase 1. The ABC can expose
`load() -> (signal, fs, meta)` and recorded loaders implement that directly.
Revisit if streaming is added later.

### 5. `session/export.py` — PDF dependency ✅
Structure originally listed CSV/PDF export. PDF generation adds a heavy dep
(ReportLab / WeasyPrint) that conflicts with the "offline-first,
resource-constrained" framing.

**Fix applied:** structure updated to **CSV + HTML**. CSV holds raw numbers;
HTML holds a human-readable summary with inline plots. If PDF is ever needed,
a user can "Print to PDF" from the HTML in any browser.

### 6. No baseline / calibration module ✅
Session store promised "before/after HR & HRV" but the baseline-window
protocol (duration, acceptance criteria, session flow) was implicit.

**Fix applied:** added `session/baseline.py` (baseline window protocol +
acceptance rule) and `session/protocol.py` (session flow: baseline → paced →
recovery). Kept under `session/` since both are tightly coupled to session
flow rather than being standalone concepts.

### 7. No dataset provenance doc ✅
A feasibility study needs the exact subset of each dataset used, licensing,
and preprocessing choices to be reviewable.

**Fix applied:** added both — `notebooks/00_data_provenance.ipynb` (workshop:
generates subset stats and plots live from the data) and `docs/datasets.md`
(shop window: the readable record of subsets, licenses, selection rationale).

## Open

### Delivery platform (deferred)
Project is being built as a local Python desktop/laptop app. Whether it
eventually needs to run on a phone, a Raspberry Pi, or stay on a laptop is
explicitly **deferred** — revisit when Phase 2 (live sensor) is scoped. No
code change yet; noted here so the question is not forgotten.

### 8. Quality-gate test (reduced scope)
`tests/unit/test_quality_gate.py` is listed but the behavior is not pinned
down. With the simple Phase 1 route this is a plain unit test (does the gate
correctly flag a bad window?), not an integration test.

**Options:** define the test's expected inputs/outputs; add a synthetic
noisy-window fixture.

### 9. `Makefile` on Windows
Project lives on Windows 11 (OneDrive path). `make` is not native. Either
expect WSL, or swap to a cross-platform alternative.

**Options:** keep Makefile + WSL, or replace with `tasks.py` (Invoke) /
`justfile`.
