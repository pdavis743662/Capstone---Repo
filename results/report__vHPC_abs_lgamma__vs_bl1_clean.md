# Statistical report — metric: `vHPC_abs_lgamma__vs_bl1`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |     ci_lo |      ci_hi |         t |   p_paired_t |    wilcoxon_p |        dz |   estimate |         p_lmm |   n_obs |
|:---------------------------|----------:|------------:|----------:|-----------:|----------:|-------------:|--------------:|----------:|-----------:|--------------:|--------:|
| C1+C2 crossover psi vs sal |        12 |    -1.14629 |  -1.72273 |  -0.659226 |  -4.02553 |   0.00199717 |   0.000976562 |  -1.16207 |   nan      | nan           |     nan |
| LMM drug[T.sal]            |       nan |   nan       | nan       | nan        | nan       | nan          | nan           | nan       |     1.0794 |   0.000191445 |      25 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |   -1.20463  |  0.00275015  |
| C1_F2           |   -1.1237   |  0.00473848  |
| C1_F3           |   -1.16478  |  0.0038342   |
| C1_M1           |   -0.919416 |  0.00064455  |
| C1_M2           |   -1.16367  |  0.00386253  |
| C1_M3           |   -1.29147  |  0.000709962 |
| C1_M4           |   -1.12214  |  0.00476519  |
| C2_F1           |   -1.07297  |  0.00518325  |
| C2_F3           |   -1.17994  |  0.00343297  |
| C2_M1           |   -1.14074  |  0.0044059   |
| C2_M2           |   -1.20914  |  0.00262508  |
| C2_M3           |   -1.16291  |  0.00388204  |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |    p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|----------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |   -0.974145 | 0.0149985 |        0.031746 |  -1.23103  |    0.0449955 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |    0.428906 | 0.236676  |        0.420635 |   0.819265 |    0.263174  |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |   -0.54524  | 0.263174  |        0.420635 |  -0.703143 |    0.263174  |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |   estimate |           p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------:|------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan        | nan         |
| OLS Intercept                        | nan                                                                                                                                                                          |  -0.593107 |   0.0315596 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |  -0.579647 |   0.0947385 |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |   0.302593 |   0.515549  |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |   0.55309  |   0.092292  |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   0.635965 |   0.302058  |
| INTERPRETATION                       | The C(blocker):C(drug) interaction term is the 5-HT2A-dependence test. With n=2-5 per cell it is underpowered -- report the estimate and CI, and do not lean on the p-value. | nan        | nan         |

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