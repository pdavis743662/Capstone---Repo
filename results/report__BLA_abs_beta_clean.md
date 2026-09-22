# Statistical report — metric: `BLA_abs_beta`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |    ci_lo |   ci_hi |        t |   p_paired_t |   wilcoxon_p |        dz |   estimate |      p_lmm |   n_obs |
|:---------------------------|----------:|------------:|---------:|--------:|---------:|-------------:|-------------:|----------:|-----------:|-----------:|--------:|
| C1+C2 crossover psi vs sal |        11 |    -771.776 | -1829.85 | 283.492 |  -1.3558 |     0.204987 |     0.240234 |  -0.40879 |    nan     | nan        |     nan |
| LMM drug[T.sal]            |       nan |     nan     |   nan    | nan     | nan      |   nan        |   nan        | nan       |    768.639 |   0.174167 |      24 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |    -812.823 |     0.227564 |
| C1_F2           |   -1018.86  |     0.105876 |
| C1_F3           |    -849.272 |     0.206251 |
| C1_M1           |    -718.865 |     0.280857 |
| C1_M2           |    -610.508 |     0.338172 |
| C1_M3           |    -433.046 |     0.414097 |
| C2_F1           |    -716.916 |     0.281931 |
| C2_F3           |    -672.734 |     0.305899 |
| C2_M1           |   -1016.09  |     0.107476 |
| C2_M2           |    -637.248 |     0.324538 |
| C2_M3           |   -1003.18  |     0.114992 |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |   p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|---------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |    1510.08  | 0.792321 |         1       |   0.227323 |     0.886111 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |    -775.228 | 0.886111 |         0.84127 |  -0.114617 |     0.886111 |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |     734.854 | 0.709729 |         1       |   0.215628 |     0.886111 |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |   estimate |             p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------:|--------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 |     nan    | nan           |
| OLS Intercept                        | nan                                                                                                                                                                          |   20648.2  |   1.04297e-09 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |    1180.63 |   0.640736    |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |    3892.63 |   0.27206     |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |   -2678.93 |   0.269429    |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   -6261.7  |   0.181773    |
| INTERPRETATION                       | The C(blocker):C(drug) interaction term is the 5-HT2A-dependence test. With n=2-5 per cell it is underpowered -- report the estimate and CI, and do not lean on the p-value. |     nan    | nan           |

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