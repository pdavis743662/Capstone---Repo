# Statistical report — metric: `BLA-vHPC_wpli_theta_winvar`

## crossover_C1C2

| analysis                   |   n_pairs |    mean_diff |         ci_lo |        ci_hi |         t |   p_paired_t |   wilcoxon_p |        dz |     estimate |      p_lmm |   n_obs |
|:---------------------------|----------:|-------------:|--------------:|-------------:|----------:|-------------:|-------------:|----------:|-------------:|-----------:|--------:|
| C1+C2 crossover psi vs sal |        11 |   0.00146796 |  -0.000849381 |   0.00367821 |   1.21767 |     0.251303 |      0.27832 |   0.36714 | nan          | nan        |     nan |
| LMM drug[T.sal]            |       nan | nan          | nan           | nan          | nan       |   nan        |    nan       | nan       |  -0.00181476 |   0.123038 |      24 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           | 0.00105648  |    0.420891  |
| C1_F2           | 0.000950141 |    0.450157  |
| C1_F3           | 0.00109854  |    0.409036  |
| C1_M1           | 0.00147328  |    0.297648  |
| C1_M2           | 0.00153756  |    0.277613  |
| C1_M3           | 0.00204952  |    0.113053  |
| C2_F1           | 0.00144955  |    0.304982  |
| C2_F3           | 0.00218926  |    0.0706098 |
| C2_M1           | 0.00123111  |    0.370754  |
| C2_M2           | 0.00134457  |    0.33699   |
| C2_M3           | 0.00176755  |    0.204145  |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |   p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|---------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |  0.00190896 | 0.533247 |        0.420635 |   0.365819 |     0.533247 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |  0.00274742 | 0.30437  |        0.309524 |   0.619133 |     0.456554 |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |  0.00465638 | 0.106389 |        0.150794 |   1.05469  |     0.319168 |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |     estimate |             p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------:|--------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan          | nan           |
| OLS Intercept                        | nan                                                                                                                                                                          |   0.0181694  |   2.18361e-09 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |  -0.00329394 |   0.165713    |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |  -0.0113504  |   0.00185632  |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |   0.0034631  |   0.125742    |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   0.00767408 |   0.0798889   |
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