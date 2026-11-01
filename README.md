# Psilocybin LFP capstone

Rodent local-field-potential study of psilocybin during an anxiety maze, and of whether a 5-HT2A blocker (ketanserin) prevents any change. Recordings are from basolateral amygdala (BLA), ventral hippocampus (vHPC), and medial prefrontal cortex (mPFC). The unit of analysis is the animal. A recording, a time window, or a single burst is never treated as an independent observation.

This repository holds the pipeline, derived tables, figures, statistical reports, and a manuscript draft. Raw `.mat` files stay outside git (`LFP Only Data/` is ignored).

## Question

Does psilocybin change maze LFP relative to that week's own baseline, and does ketanserin block that change?

The confirmatory test is a within-mouse crossover (cohorts C1 and C2, elevated zero maze). Cohorts C3 and C4 (elevated plus maze) are between-mouse designs used for the ketanserin question. They are underpowered for the effects seen in the crossover.

## Current result

On the C1+C2 maze test, three of eight pre-declared outcomes survive Benjamini–Hochberg FDR:

- Fewer BLA beta bursts on the psilocybin week (about −9 per minute).
- Lower BLA beta power versus that week's own baseline.
- Higher vHPC theta power versus that week's own baseline.

Those first two are largely the same measurement (psi−sal deltas correlate at about r = 0.95). Beta-band BLA–vHPC coupling does not change. Raw maze power, without the baseline reference, does not separate cleanly.

Exploratory follow-ups (their own FDR, not confirmations) show a spectral rotation: slower power versus baseline leans up under psilocybin and faster power leans down. The aperiodic exponent captures that tilt; only vHPC clears correction. Adjusting the vHPC theta hit for the exponent pulls most of that difference into the tilt. Burst rate and BLA beta do not shrink. A high-frequency residual in BLA is a lead, not the prefrontal ~100 Hz oscillation reported elsewhere.

C3 (five mice per arm) points the same way for bursts and BLA beta, and ketanserin animals sit nearer saline for bursts, but none of those primary contrasts survive correction. The pooled C3+C4 blocker × drug interaction does not show that the effect depends on 5-HT2A, and it does not show that it is independent of 5-HT2A. A non-significant blocker test here is an underpowered test.

Numbers, confidence intervals, and the reading of each model are in `PROJECT_SUMMARY.md`. The results-section skeleton is `RESULTS_OUTLINE.md`.

## Pipeline

Run order for the analysis that the reports were built from:

| Step | Script | What it does |
| --- | --- | --- |
| 1–2 | `data_ingestion.ipynb` | Inventory the recordings, clean them, write QC |
| — | `python/exclusions.py` | Drop silent or spike-dominated channels (other regions on the same file stay) |
| 3 | `step3_features.py` | One feature row per recording: band power, bursts, wPLI, aperiodic exponent, high-frequency residual |
| 6 | `step6_windows.py` | Overlapping 10 s windows; session mean and variance of coupling |
| 5 | `step5_stats.py` | Crossover, C3 three-arm, and pooled 2×2, with FDR inside each pre-declared family |
| — | `step5_followup.py` | Exponent direction, tilt adjustment, ketanserin write-up (exploratory) |
| 4 | `step4_figures.py` | Figures from the same tables. Does not decide significance |

`python/lfp_config.py` holds band edges and the three metric lists (`PRIMARY_METRICS`, `EXPLORATORY_METRICS`, `HFO_METRICS`). Adding a metric to the primary list changes what counts as confirmatory.

`step10_timecourse.py` stops on purpose: no file identifies an injection instant (`results/ttl_alignment.md`). `step7_video.py`, `step8_compare.py`, and `step9_band_compare.py` build inspection movies. They are not part of the hypothesis tests. `notebooks/02_lfp_explorer.ipynb` is for looking at one recording.

File-by-file notes are in `CODE_OUTLINE.md`.

```bash
python step3_features.py --derived derived
python step6_windows.py
python step5_stats.py --features derived/features_dynamic.csv --metrics primary --out results
python step5_stats.py --features derived/features_dynamic.csv --metrics exploratory --out results
python step5_followup.py
python step4_figures.py
```

Stage 3 needs the cleaned arrays from the notebook (`derived/clean/*.npz`). Those arrays are gitignored because they are large. A clone of this repo has the tables and reports already written; regenerating features requires the raw recordings and a local run of Stages 1–2.

## Cohorts

| Cohort | Design | Maze | Animals |
| --- | --- | --- | --- |
| C1 | Same mouse, saline week and psilocybin week | EZM | 7 |
| C2 | Same as C1, except one mouse has saline only | EZM | 6 (5 paired) |
| C3 | Different mouse per arm: saline, psilocybin, ketanserin + psilocybin | EPM | 5 per arm |
| C4 | Blocker × drug follow-up that fills out the 2×2 | EPM | 2–4 per cell |

203 recordings across the four cohorts. After channel exclusion, the paired C1+C2 test has 11 mice for outcomes that need a usable BLA and 12 for vHPC. Confirmatory metrics use BLA, vHPC, and the BLA–vHPC pair. mPFC is only in the exploratory exponent family and the high-frequency residual family.

## Where the outputs are

- Feature tables: `derived/features_session.csv`, `derived/features_normalized.csv`, `derived/features_dynamic.csv`
- Confirmatory overview: `results/report__primary_metrics_clean.md`
- Exploratory overview: `results/report__exploratory_metrics_clean.md`
- High-frequency residual: `results/report__hfo_metrics_clean.md`
- One outcome, all three models: `results/report__<metric>_clean.md`
- Figures: `figures_clean/` (PDF) and `figures_png/`
- Manuscript draft: `overleaf/` (see `overleaf/README.md` for the Overleaf import)

## Environment

Python dependencies are pinned in `requirements.txt` (numpy, scipy, pandas, matplotlib, statsmodels, specparam, Jupyter). The aperiodic fit and the high-frequency residual need specparam. `ENABLE_APERIODIC` and `ENABLE_HFO` in `python/lfp_config.py` are on for the delivered pipeline.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
