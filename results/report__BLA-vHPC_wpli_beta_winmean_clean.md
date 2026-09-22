# Statistical report — metric: `BLA-vHPC_wpli_beta_winmean`

## crossover_C1C2

| analysis                   |   n_pairs |    mean_diff |        ci_lo |       ci_hi |          t |   p_paired_t |   wilcoxon_p |        dz |     estimate |      p_lmm |   n_obs |
|:---------------------------|----------:|-------------:|-------------:|------------:|-----------:|-------------:|-------------:|----------:|-------------:|-----------:|--------:|
| C1+C2 crossover psi vs sal |        11 |   0.00331261 |  -0.00783238 |   0.0148326 |   0.546316 |     0.596826 |     0.577148 |   0.16472 | nan          | nan        |     nan |
| LMM drug[T.sal]            |       nan | nan          | nan          | nan         | nan        |   nan        |   nan        | nan       |  -0.00338134 |   0.568792 |      24 |

## crossover_loo

| dropped_mouse   |    mean_diff |   p_paired_t |
|:----------------|-------------:|-------------:|
| C1_F1           | -0.000751301 |     0.883296 |
| C1_F2           |  0.00245461  |     0.720018 |
| C1_F3           |  0.00427016  |     0.534959 |
| C1_M1           |  0.00662164  |     0.268703 |
| C1_M2           |  0.00258762  |     0.706463 |
| C1_M3           |  0.00406123  |     0.556625 |
| C2_F1           |  0.00598849  |     0.345493 |
| C2_F3           |  0.00305232  |     0.659365 |
| C2_M1           |  0.00317152  |     0.647307 |
| C2_M2           |  0.00339714  |     0.624464 |
| C2_M3           |  0.00158524  |     0.810674 |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |   p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|---------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 | -0.0123663  | 0.187681 |        0.309524 | -0.832225  |     0.522398 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |  0.00125743 | 0.917408 |        1        |  0.0722274 |     0.917408 |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 | -0.0111088  | 0.348265 |        0.222222 | -0.587456  |     0.522398 |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |     estimate |             p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------:|--------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan          | nan           |
| OLS Intercept                        | nan                                                                                                                                                                          |   0.281629   |   7.21708e-20 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |   0.00435931 |   0.66234     |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |  -0.0160445  |   0.252076    |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |   0.0157821  |   0.105535    |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   0.0294001  |   0.115471    |
| INTERPRETATION                       | The C(blocker):C(drug) interaction term is the 5-HT2A-dependence test. With n=2-5 per cell it is underpowered -- report the estimate and CI, and do not lean on the p-value. | nan          | nan           |

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