# Statistical report — metric: `burst_rate_per_min`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |    ci_lo |     ci_hi |         t |   p_paired_t |   wilcoxon_p |         dz |   estimate |        p_lmm |   n_obs |
|:---------------------------|----------:|------------:|---------:|----------:|----------:|-------------:|-------------:|-----------:|-----------:|-------------:|--------:|
| C1+C2 crossover psi vs sal |        11 |    -8.77738 | -14.1773 |  -3.99783 |  -3.18663 |   0.00970956 |   0.00976562 |  -0.960805 |  nan       | nan          |     nan |
| LMM drug[T.sal]            |       nan |   nan       | nan      | nan       | nan       | nan          | nan          | nan        |    7.94523 |   0.00425744 |      24 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |    -9.60163 |   0.00916375 |
| C1_F2           |    -8.76783 |   0.0181989  |
| C1_F3           |    -9.81254 |   0.0069687  |
| C1_M1           |    -8.07742 |   0.0227511  |
| C1_M2           |    -8.07275 |   0.022763   |
| C1_M3           |    -9.4449  |   0.010885   |
| C2_F1           |    -6.77014 |   0.0100524  |
| C2_F3           |    -8.49932 |   0.0205296  |
| C2_M1           |    -8.80013 |   0.0178848  |
| C2_M2           |    -8.908   |   0.0167951  |
| C2_M3           |    -9.79653 |   0.00712868 |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |    p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|----------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |   -9.08535  | 0.0655934 |       0.150794  | -1.25534   |     0.130037 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |    9.58071  | 0.0866913 |       0.0555556 |  0.98145   |     0.130037 |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |    0.495355 | 0.917408  |       1         |  0.0459518 |     0.917408 |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |   estimate |             p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------:|--------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan        | nan           |
| OLS Intercept                        | nan                                                                                                                                                                          |  33.5577   |   3.57541e-08 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |  -8.68501  |   0.098495    |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |   2.31585  |   0.741806    |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |  -0.908332 |   0.850085    |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   3.51694  |   0.703352    |
| INTERPRETATION                       | The C(blocker):C(drug) interaction term is the 5-HT2A-dependence test. With n=2-5 per cell it is underpowered -- report the estimate and CI, and do not lean on the p-value. | nan        | nan           |

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