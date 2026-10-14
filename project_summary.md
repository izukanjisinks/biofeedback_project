# Low-Cost Biofeedback System for Hypertension Self-Management

## Project Build Summary

A low-cost, offline-first biofeedback prototype that uses heart rate (from PPG or ECG) to
guide paced-breathing exercises for hypertension self-management, aimed at resource-constrained
settings. Framed as a biomedical signal-processing and software study: it proves **technical
feasibility and physiological response**, not clinical effectiveness.

| Component | What we're building | Key details / tools | Scope boundary |
|---|---|---|---|
| **Overall system** | Low-cost, offline-first biofeedback prototype for hypertension self-management via paced breathing | Python stack, runs locally; honest "feasibility not clinical proof" framing | Proves technical feasibility + physiological response, **not** clinical effectiveness |
| **1. Signal acquisition** | Dataset loader + (later) a live input | WFDB for BIDMC, Fantasia, MIT-BIH; file readers for PPG-DaLiA/WESAD. Live input = *to be decided* | Development uses recorded datasets; real sensor is later-phase |
| **2. Preprocessing + signal quality** | Filtering and a quality gate that decides if a segment is trustworthy | Band-pass (0.5–8 Hz PPG), 50 Hz notch; windowed signal-quality index (skewness/template); 5%-bad-interval discard rule | The "honest" core — refuses to show confident numbers on bad signals |
| **3. Feature extraction** | Beat detection → intervals → heart rate + HRV | NeuroKit2 Elgendi (PPG) / Pan–Tompkins (ECG); parabolic sub-sample timing; IBI/tachogram; RMSSD, SDNN, pNN50, SD1/SD2; LF/HF (secondary); ectopic flagging | HRV only when data quality/length supports it; else HR only |
| **4. Biofeedback engine** | Paced-breathing pacer + real-time feedback | Expanding/contracting visual at ~6 breaths/min (configurable) + optional audio; shows HR oscillation (RSA), pauses/marks uncertain on poor signal | Target physiological response is HRV/RSA change, not BP |
| **5. Session management** | Local storage + history + optional export | SQLite (duration, pacing rate, before/after HR & HRV, SQI stats, corrected-beat count); Matplotlib history graphs; exportable summary for a health worker | Fully offline; no mandatory connectivity |
| **6. Evaluation harness** | Measure what the system can actually demonstrate | HR accuracy vs reference (MAE, Bland–Altman); PRV-vs-HRV agreement (BIDMC); SQI performance via noise injection (Noise Stress Test DB); feedback-timing accuracy; HR/RSA response during paced breathing | Clinical / blood-pressure effectiveness stays out |

## Open decisions

- **Live sensor** (row 1): not yet chosen.
- **Respiration** (rows 3–4): whether to measure it or just pace it.
