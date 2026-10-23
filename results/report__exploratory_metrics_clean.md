# Statistical report — metrics: `BLA_abs_delta__vs_bl1`, `BLA_abs_theta__vs_bl1`, `BLA_abs_beta__vs_bl1`, `BLA_abs_lgamma__vs_bl1`, `BLA_abs_hgamma__vs_bl1`, `vHPC_abs_delta__vs_bl1`, `vHPC_abs_theta__vs_bl1`, `vHPC_abs_beta__vs_bl1`, `vHPC_abs_lgamma__vs_bl1`, `vHPC_abs_hgamma__vs_bl1`, `BLA_rel_beta__vs_bl1`, `vHPC_rel_theta__vs_bl1`, `BLA-vHPC_wpli_theta_winmean`, `BLA-vHPC_wpli_theta_winvar`

_Exploratory family. FDR is within this list only. `BLA_abs_beta__vs_bl1` and `vHPC_abs_theta__vs_bl1` also appear in `PRIMARY_METRICS`; they are included here so band-specificity is tested under one correction. Do not treat new rejections as confirmatory._

_Dead channels excluded. Filenames use the `_clean` suffix._

## Channel exclusions

Policy (applied before every test): a region's metrics are set to NaN when `log10(RMS) < 2.0` (dead channel; main clouds sit near 2.6–2.9, a distinct cluster sits near 1.05), when excess kurtosis > 20, or when the channel is missing. Burst columns require a live BLA; phase-lag columns require live BLA and vHPC. Other regions on the same recording are kept.

- Files in the features table: **203**
- Files with ≥1 excluded channel: **33**

### By criterion (unique files)

| reason        |   n_files |
|:--------------|----------:|
| dead_channel  |        16 |
| high_kurtosis |        17 |

### Per (cohort, group, region)

| cohort   | group   | region   |   n_excluded |   n_files_in_group |   pct_of_group_files |
|:---------|:--------|:---------|-------------:|-------------------:|---------------------:|
| C1       | psi     | BLA      |            4 |                 28 |             14.2857  |
| C1       | psi     | mPFC     |            4 |                 28 |             14.2857  |
| C1       | psi     | vHPC     |            1 |                 28 |              3.57143 |
| C1       | sal     | BLA      |            5 |                 28 |             17.8571  |
| C2       | psi     | mPFC     |            4 |                 20 |             20       |
| C2       | sal     | BLA      |            1 |                 24 |              4.16667 |
| C2       | sal     | mPFC     |            8 |                 24 |             33.3333  |
| C3       | ket     | BLA      |            2 |                 20 |             10       |
| C3       | ket     | mPFC     |            2 |                 20 |             10       |
| C3       | psi     | BLA      |            1 |                 20 |              5       |
| C3       | sal     | BLA      |            3 |                 20 |             15       |
| C3       | sal     | mPFC     |            3 |                 20 |             15       |
| C4       | ket_sal | mPFC     |            1 |                 16 |              6.25    |

## C1/C2 crossover FDR across metrics

| metric                      |   p_crossover |   n_pairs |   mean_diff |   p_crossover_fdr | reject_fdr   |
|:----------------------------|--------------:|----------:|------------:|------------------:|:-------------|
| BLA_abs_delta__vs_bl1       |   0.160983    |        11 |  0.866274   |       0.187814    | False        |
| BLA_abs_theta__vs_bl1       |   0.0554248   |        11 |  0.657073   |       0.0775947   | False        |
| BLA_abs_beta__vs_bl1        |   0.00853716  |        11 | -0.445595   |       0.02988     | True         |
| BLA_abs_lgamma__vs_bl1      |   2.65586e-05 |        11 | -0.961229   |       0.000371821 | True         |
| BLA_abs_hgamma__vs_bl1      |   0.0186987   |        11 | -0.3694     |       0.0373974   | True         |
| vHPC_abs_delta__vs_bl1      |   0.108529    |        12 |  0.421838   |       0.138127    | False        |
| vHPC_abs_theta__vs_bl1      |   0.0153212   |        12 |  0.605694   |       0.0357495   | True         |
| vHPC_abs_beta__vs_bl1       |   0.568874    |        12 | -0.180594   |       0.568874    | False        |
| vHPC_abs_lgamma__vs_bl1     |   0.00199717  |        12 | -1.14629    |       0.00932012  | True         |
| vHPC_abs_hgamma__vs_bl1     |   9.19706e-05 |        12 | -0.6679     |       0.000643794 | True         |
| BLA_rel_beta__vs_bl1        |   0.0423284   |        11 | -0.694808   |       0.0658442   | False        |
| vHPC_rel_theta__vs_bl1      |   0.0126932   |        12 |  0.426584   |       0.0355408   | True         |
| BLA-vHPC_wpli_theta_winmean |   0.0389386   |        11 | -0.0393326  |       0.0658442   | False        |
| BLA-vHPC_wpli_theta_winvar  |   0.251303    |        11 |  0.00146796 |       0.270634    | False        |

## Reporting checklist
- [ ] Unit of analysis is the animal, not the burst or the time window
- [ ] Effect sizes with bootstrap CIs reported alongside every p-value
- [ ] FDR correction applied across the primary metric family
- [ ] Primary hypothesis was declared before looking; everything else labelled exploratory
- [ ] Artifact-rejection rates compared across groups
- [ ] Sensitivity analysis reported for any null result
- [ ] Dead-channel exclusions reported with per-group counts