# Statistical report — metric: `BLA_abs_hgamma__vs_bl1`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |      ci_lo |      ci_hi |         t |   p_paired_t |   wilcoxon_p |         dz |   estimate |        p_lmm |   n_obs |
|:---------------------------|----------:|------------:|-----------:|-----------:|----------:|-------------:|-------------:|-----------:|-----------:|-------------:|--------:|
| C1+C2 crossover psi vs sal |        11 |     -0.3694 |  -0.609566 |  -0.117757 |  -2.80298 |    0.0186987 |    0.0322266 |  -0.845131 | nan        | nan          |     nan |
| LMM drug[T.sal]            |       nan |    nan      | nan        | nan        | nan       |  nan         |  nan         | nan        |   0.340002 |   0.00782754 |      24 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |   -0.388127 |   0.0247465  |
| C1_F2           |   -0.320105 |   0.0419762  |
| C1_F3           |   -0.335973 |   0.0409635  |
| C1_M1           |   -0.434988 |   0.00736602 |
| C1_M2           |   -0.431385 |   0.00845483 |
| C1_M3           |   -0.344018 |   0.0394923  |
| C2_F1           |   -0.351666 |   0.0376212  |
| C2_F3           |   -0.403365 |   0.0186187  |
| C2_M1           |   -0.308189 |   0.0406548  |
| C2_M2           |   -0.397092 |   0.0211335  |
| C2_M3           |   -0.348494 |   0.0384478  |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |   p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|---------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |   -0.405903 | 0.251575 |        0.420635 |  -0.744385 |     0.582642 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |    0.208515 | 0.582642 |        0.690476 |   0.342302 |     0.582642 |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |   -0.197388 | 0.510549 |        0.420635 |  -0.366624 |     0.582642 |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |    estimate |             p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------:|--------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan         | nan           |
| OLS Intercept                        | nan                                                                                                                                                                          |  -0.975832  |   2.14069e-05 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |  -0.183174  |   0.431237    |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |  -0.0482933 |   0.879843    |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |   0.373096  |   0.099294    |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   0.436592  |   0.304452    |
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