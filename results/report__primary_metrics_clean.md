# Statistical report — metrics: `burst_rate_per_min`, `BLA_abs_beta`, `BLA_abs_beta__vs_bl1`, `vHPC_abs_theta`, `vHPC_abs_theta__vs_bl1`, `BLA-vHPC_wpli_beta`, `BLA-vHPC_wpli_beta_winmean`, `BLA-vHPC_wpli_beta_winvar`

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

| metric                     |   p_crossover |   n_pairs |       mean_diff |   p_crossover_fdr | reject_fdr   |
|:---------------------------|--------------:|----------:|----------------:|------------------:|:-------------|
| burst_rate_per_min         |    0.00970956 |        11 |    -8.77738     |         0.0388382 | True         |
| BLA_abs_beta               |    0.204987   |        11 |  -771.776       |         0.32798   | False        |
| BLA_abs_beta__vs_bl1       |    0.00853716 |        11 |    -0.445595    |         0.0388382 | True         |
| vHPC_abs_theta             |    0.0902203  |        12 | 49252           |         0.180441  | False        |
| vHPC_abs_theta__vs_bl1     |    0.0153212  |        12 |     0.605694    |         0.0408565 | True         |
| BLA-vHPC_wpli_beta         |    0.572594   |        11 |     0.00924982  |         0.596826  | False        |
| BLA-vHPC_wpli_beta_winmean |    0.596826   |        11 |     0.00331261  |         0.596826  | False        |
| BLA-vHPC_wpli_beta_winvar  |    0.496619   |        11 |     0.000303093 |         0.596826  | False        |

## Reporting checklist
- [ ] Unit of analysis is the animal, not the burst or the time window
- [ ] Effect sizes with bootstrap CIs reported alongside every p-value
- [ ] FDR correction applied across the primary metric family
- [ ] Primary hypothesis was declared before looking; everything else labelled exploratory
- [ ] Artifact-rejection rates compared across groups
- [ ] Sensitivity analysis reported for any null result
- [ ] Dead-channel exclusions reported with per-group counts