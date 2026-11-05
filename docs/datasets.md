# Datasets

Record of the exact dataset subsets, licensing and selection rationale.
Numbers in this file are filled in from `notebooks/00_data_provenance.ipynb`
after the data is downloaded.

## BIDMC PPG and Respiration Dataset

- Source: PhysioNet, https://physionet.org/content/bidmc/1.0.0/
- License: Open Data Commons Attribution License v1.0
- Citation: Pimentel et al. (2017). *Toward a robust estimation of respiratory
  rate from pulse oximeters.* IEEE TBME 64(8), 1914–1923.
- Signals used: PPG (`PLETH`), ECG (`II`), respiration (`RESP`)
- Sampling rate: 125 Hz
- Total records: 53 (8 min each)
- Subset used: _TBD — fill after provenance notebook_
- Selection criteria: _TBD_

## Fantasia Database

- Source: PhysioNet, https://physionet.org/content/fantasia/1.0.0/
- License: ODC-By
- Citation: Iyengar et al. (1996). *Age-related alterations in the fractal
  scaling of cardiac interbeat interval dynamics.* Am J Physiol 271(4).
- Signals used: ECG, respiration
- Sampling rate: 250 Hz
- Subset used: _TBD_
- Selection criteria: _TBD_

## MIT-BIH Arrhythmia Database

- Source: PhysioNet, https://physionet.org/content/mitdb/1.0.0/
- License: ODC-By
- Citation: Moody & Mark (2001). *The impact of the MIT-BIH Arrhythmia
  Database.* IEEE EMB Mag 20(3), 45–50.
- Use: ectopic-beat handling and quality-gate stress tests, not for primary
  HR/HRV evaluation.
- Subset used: _TBD_
- Selection criteria: _TBD_

## Preprocessing applied before the pipeline

None. All filtering, beat detection and quality assessment happens inside
`src/biofeedback/` so the data on disk stays identical to the download.
