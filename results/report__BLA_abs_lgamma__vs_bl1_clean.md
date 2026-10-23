# Statistical report — metric: `BLA_abs_lgamma__vs_bl1`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |     ci_lo |      ci_hi |         t |    p_paired_t |    wilcoxon_p |        dz |   estimate |         p_lmm |   n_obs |
|:---------------------------|----------:|------------:|----------:|-----------:|----------:|--------------:|--------------:|----------:|-----------:|--------------:|--------:|
| C1+C2 crossover psi vs sal |        11 |   -0.961229 |  -1.21139 |  -0.719924 |  -7.28228 |   2.65586e-05 |   0.000976562 |  -2.19569 | nan        | nan           |     nan |
| LMM drug[T.sal]            |       nan |  nan        | nan       | nan        | nan       | nan           | nan           | nan       |   0.914381 |   1.78421e-11 |      24 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |   -0.939544 |  0.000107991 |
| C1_F2           |   -0.950328 |  0.000107052 |
| C1_F3           |   -1.04549  |  6.47798e-06 |
| C1_M1           |   -0.974001 |  8.79282e-05 |
| C1_M2           |   -0.986617 |  7.14881e-05 |
| C1_M3           |   -0.86663  |  1.33925e-05 |
| C2_F1           |   -0.962355 |  9.98451e-05 |
| C2_F3           |   -0.990023 |  6.67126e-05 |
| C2_M1           |   -0.947591 |  0.000107816 |
| C2_M2           |   -0.937637 |  0.000107565 |
| C2_M3           |   -0.973304 |  8.87487e-05 |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |    p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|----------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |   -0.822129 | 0.0124988 |        0.015873 |  -1.85103  |    0.0374963 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |    0.6017   | 0.216278  |        0.309524 |   0.768742 |    0.324418  |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |   -0.220429 | 0.639436  |        0.420635 |  -0.298714 |    0.639436  |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |    estimate |             p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------:|--------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan         | nan           |
| OLS Intercept                        | nan                                                                                                                                                                          |  -1.65671   |   4.66787e-07 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |  -0.555182  |   0.0721202   |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |  -0.0481098 |   0.9065      |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |   0.562943  |   0.055435    |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   0.642084  |   0.240822    |
| INTERPRETATION                       | The C(blocker):C(drug) interaction term is the 5-HT2A-dependence test. With n=2-5 per cell it is underpowered -- report the estimate and CI, and do not lean on the p-value. | nan         | nan           |

## sensitivity

| analysis                                  |   n_per_group |         d | note                                                                                                                                                                      |
|:------------------------------------------|--------------:|----------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| minimum detectable Cohen's d at 80% power |             5 |   1.77188 | nan                                                                                                                                                                       |
| minimum detectable Cohen's d at 90% power |             5 |   2.05011 | nan                                                                                                                                                                       |
| INTERPRETATION                            |           nan | nan       | If that d is larger than effects typical in this literature, a null result here is uninformative -- say so explicitly in the discussion rather than claiming 'no effect'. |

## Reporting checklist
- [ ] Unit of analysis is the animal, not the burst or the time window
- [ ] Effect sizes with bootstrap CIs reported alongside every p-value
- [ ] FDR correction applied across the primary metric family
- [ ] Primary hypothesis was declared before looking; everything else labelled exploratory
- [ ] Artifact-rejection rates compared across groups
- [ ] Sensitivity analysis reported for any null result
- [ ] Dead-channel exclusions reported with per-group counts