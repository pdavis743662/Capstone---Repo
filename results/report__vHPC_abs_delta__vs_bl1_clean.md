# Statistical report — metric: `vHPC_abs_delta__vs_bl1`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |       ci_lo |      ci_hi |         t |   p_paired_t |   wilcoxon_p |         dz |   estimate |       p_lmm |   n_obs |
|:---------------------------|----------:|------------:|------------:|-----------:|----------:|-------------:|-------------:|-----------:|-----------:|------------:|--------:|
| C1+C2 crossover psi vs sal |        12 |    0.421838 |  -0.0172096 |   0.880203 |   1.74662 |     0.108529 |    0.0771484 |   0.504205 | nan        | nan         |     nan |
| LMM drug[T.sal]            |       nan |  nan        | nan         | nan        | nan       |   nan        |  nan         | nan        |  -0.431109 |   0.0708948 |      25 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |    0.423698 |    0.140346  |
| C1_F2           |    0.453367 |    0.114611  |
| C1_F3           |    0.473875 |    0.0965105 |
| C1_M1           |    0.393471 |    0.165124  |
| C1_M2           |    0.565669 |    0.0238373 |
| C1_M3           |    0.429086 |    0.135748  |
| C1_M4           |    0.318507 |    0.212442  |
| C2_F1           |    0.36242  |    0.187934  |
| C2_F3           |    0.441037 |    0.125415  |
| C2_M1           |    0.28097  |    0.220332  |
| C2_M2           |    0.43702  |    0.128906  |
| C2_M3           |    0.482936 |    0.0885358 |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |    p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|----------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |   0.0368051 | 0.952205  |       1         |  0.0491582 |     0.952205 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |   0.939918  | 0.0986901 |       0.150794  |  1.05384   |     0.160934 |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |   0.976723  | 0.107289  |       0.0555556 |  0.972956  |     0.160934 |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |   estimate |            p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------:|-------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan        | nan          |
| OLS Intercept                        | nan                                                                                                                                                                          |   2.05255  |   2.0771e-05 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |  -0.24871  |   0.608897   |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |  -0.858725 |   0.209217   |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |   0.183892 |   0.689026   |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   0.688765 |   0.437398   |
| INTERPRETATION                       | The C(blocker):C(drug) interaction term is the 5-HT2A-dependence test. With n=2-5 per cell it is underpowered -- report the estimate and CI, and do not lean on the p-value. | nan        | nan          |

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