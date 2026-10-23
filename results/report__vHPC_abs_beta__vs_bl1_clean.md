# Statistical report — metric: `vHPC_abs_beta__vs_bl1`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |      ci_lo |      ci_hi |         t |   p_paired_t |   wilcoxon_p |         dz |    estimate |      p_lmm |   n_obs |
|:---------------------------|----------:|------------:|-----------:|-----------:|----------:|-------------:|-------------:|-----------:|------------:|-----------:|--------:|
| C1+C2 crossover psi vs sal |        12 |   -0.180594 |  -0.775607 |   0.386251 |  -0.58728 |     0.568874 |     0.677246 |  -0.169533 | nan         | nan        |     nan |
| LMM drug[T.sal]            |       nan |  nan        | nan        | nan        | nan       |   nan        |   nan        | nan        |   0.0873167 |   0.782244 |      25 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |  -0.19168   |     0.581655 |
| C1_F2           |  -0.157258  |     0.64969  |
| C1_F3           |  -0.21368   |     0.537786 |
| C1_M1           |   0.0105478 |     0.968902 |
| C1_M2           |  -0.079149  |     0.808479 |
| C1_M3           |  -0.239618  |     0.485184 |
| C1_M4           |  -0.350073  |     0.241357 |
| C2_F1           |  -0.0943593 |     0.776385 |
| C2_F3           |  -0.202154  |     0.560834 |
| C2_M1           |  -0.277408  |     0.405934 |
| C2_M2           |  -0.136013  |     0.691817 |
| C2_M3           |  -0.236283  |     0.492017 |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |   p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|---------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |  -0.0211026 | 0.943706 |        0.84127  |  -0.043202 |     0.943706 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |   0.140576  | 0.632337 |        0.690476 |   0.247479 |     0.943706 |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |   0.119473  | 0.635236 |        0.547619 |   0.242303 |     0.943706 |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |     estimate |             p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------:|--------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan          | nan           |
| OLS Intercept                        | nan                                                                                                                                                                          |   0.862112   |   0.000180304 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |  -0.00849587 |   0.972378    |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |  -0.223825   |   0.511896    |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |  -0.0111301  |   0.961778    |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   0.143188   |   0.748333    |
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