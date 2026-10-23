# Statistical report — metric: `vHPC_abs_hgamma__vs_bl1`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |     ci_lo |      ci_hi |        t |    p_paired_t |    wilcoxon_p |        dz |   estimate |         p_lmm |   n_obs |
|:---------------------------|----------:|------------:|----------:|-----------:|---------:|--------------:|--------------:|----------:|-----------:|--------------:|--------:|
| C1+C2 crossover psi vs sal |        12 |     -0.6679 |  -0.89782 |  -0.487128 |  -5.9792 |   9.19706e-05 |   0.000488281 |  -1.72605 | nan        | nan           |     nan |
| LMM drug[T.sal]            |       nan |    nan      | nan       | nan        | nan      | nan           | nan           | nan       |   0.657952 |   3.22457e-09 |      25 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |   -0.693585 |  0.000167362 |
| C1_F2           |   -0.680852 |  0.000227102 |
| C1_F3           |   -0.686744 |  0.000199998 |
| C1_M1           |   -0.646538 |  0.000308768 |
| C1_M2           |   -0.708576 |  9.91597e-05 |
| C1_M3           |   -0.678552 |  0.000237168 |
| C1_M4           |   -0.659592 |  0.000299161 |
| C2_F1           |   -0.573589 |  5.34068e-06 |
| C2_F3           |   -0.645668 |  0.000308218 |
| C2_M1           |   -0.666693 |  0.000281377 |
| C2_M2           |   -0.687011 |  0.000198739 |
| C2_M3           |   -0.687407 |  0.000196863 |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |    p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|----------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |   -0.944691 | 0.0161984 |       0.015873  |  -2.21255  |    0.0485951 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |    0.691512 | 0.0391961 |       0.0555556 |   1.42143  |    0.0587941 |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |   -0.253179 | 0.350365  |       0.420635  |  -0.547775 |    0.350365  |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |    estimate |            p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------:|-------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan         | nan          |
| OLS Intercept                        | nan                                                                                                                                                                          |  -0.0155844 |   0.929042   |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |  -0.773451  |   0.00239245 |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |   0.179476  |   0.566502   |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |   0.324277  |   0.139496   |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   0.725092  |   0.0881049  |
| INTERPRETATION                       | The C(blocker):C(drug) interaction term is the 5-HT2A-dependence test. With n=2-5 per cell it is underpowered -- report the estimate and CI, and do not lean on the p-value. | nan         | nan          |

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