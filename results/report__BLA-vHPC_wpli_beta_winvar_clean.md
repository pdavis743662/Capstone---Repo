# Statistical report — metric: `BLA-vHPC_wpli_beta_winvar`

## crossover_C1C2

| analysis                   |   n_pairs |     mean_diff |         ci_lo |        ci_hi |          t |   p_paired_t |   wilcoxon_p |         dz |      estimate |      p_lmm |   n_obs |
|:---------------------------|----------:|--------------:|--------------:|-------------:|-----------:|-------------:|-------------:|-----------:|--------------:|-----------:|--------:|
| C1+C2 crossover psi vs sal |        11 |   0.000303093 |  -0.000467852 |   0.00113334 |   0.705476 |     0.496619 |     0.700195 |   0.212709 | nan           | nan        |     nan |
| LMM drug[T.sal]            |       nan | nan           | nan           | nan          | nan        |   nan        |   nan        | nan        |  -0.000258469 |   0.534844 |      24 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           | 4.92552e-06 |     0.988822 |
| C1_F2           | 0.000353195 |     0.473139 |
| C1_F3           | 0.000361043 |     0.462644 |
| C1_M1           | 0.000457837 |     0.328441 |
| C1_M2           | 0.000168207 |     0.717781 |
| C1_M3           | 0.000500297 |     0.26614  |
| C2_F1           | 0.000399948 |     0.40987  |
| C2_F3           | 0.000287606 |     0.55954  |
| C2_M1           | 0.000208101 |     0.663874 |
| C2_M2           | 0.000361638 |     0.461847 |
| C2_M3           | 0.000231221 |     0.633296 |

## threearm_C3

| analysis                                          |   n1 |   n2 |    mean_diff |    p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|-------------:|----------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 | -0.000737891 | 0.0318968 |        0.031746 | -1.54277   |    0.0488951 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |  1.29882e-05 | 0.957004  |        1        |  0.0273468 |    0.957004  |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 | -0.000724903 | 0.0325967 |        0.031746 | -1.64451   |    0.0488951 |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |      estimate |             p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------:|--------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan           | nan           |
| OLS Intercept                        | nan                                                                                                                                                                          |   0.00302382  |   4.17675e-11 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |   6.36816e-05 |   0.836071    |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |  -0.000764497 |   0.0838484   |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |   0.00101979  |   0.00202418  |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   0.00151548  |   0.0124468   |
| INTERPRETATION                       | The C(blocker):C(drug) interaction term is the 5-HT2A-dependence test. With n=2-5 per cell it is underpowered -- report the estimate and CI, and do not lean on the p-value. | nan           | nan           |

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