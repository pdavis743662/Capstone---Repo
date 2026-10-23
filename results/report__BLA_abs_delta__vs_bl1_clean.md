# Statistical report — metric: `BLA_abs_delta__vs_bl1`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |     ci_lo |     ci_hi |         t |   p_paired_t |   wilcoxon_p |         dz |   estimate |      p_lmm |   n_obs |
|:---------------------------|----------:|------------:|----------:|----------:|----------:|-------------:|-------------:|-----------:|-----------:|-----------:|--------:|
| C1+C2 crossover psi vs sal |        11 |    0.866274 |  -0.28318 |   1.87142 |   1.51396 |     0.160983 |     0.101562 |   0.456475 | nan        | nan        |     nan |
| LMM drug[T.sal]            |       nan |  nan        | nan       | nan       | nan       |   nan        |   nan        | nan        |  -0.844318 |   0.114411 |      24 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |    0.738479 |    0.26164   |
| C1_F2           |    0.887447 |    0.193914  |
| C1_F3           |    0.788011 |    0.240214  |
| C1_M1           |    0.761151 |    0.251998  |
| C1_M2           |    1.30128  |    0.0114289 |
| C1_M3           |    0.569616 |    0.31977   |
| C2_F1           |    0.809249 |    0.230649  |
| C2_F3           |    0.94555  |    0.1655    |
| C2_M1           |    0.761987 |    0.251637  |
| C2_M2           |    1.00793  |    0.134472  |
| C2_M3           |    0.958307 |    0.159181  |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |    p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|----------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |   0.745508  | 0.0986901 |        0.150794 |  1.03912   |    0.148035  |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |   0.0305887 | 0.952305  |        1        |  0.0477874 |    0.952305  |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |   0.776096  | 0.0251975 |        0.031746 |  1.46195   |    0.0755924 |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |    estimate |           p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------:|------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan         | nan         |
| OLS Intercept                        | nan                                                                                                                                                                          |   0.0157986 |   0.946652  |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |   0.36452   |   0.239016  |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |  -1.08177   |   0.0169852 |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |   0.245743  |   0.39763   |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   0.406804  |   0.464585  |
| INTERPRETATION                       | The C(blocker):C(drug) interaction term is the 5-HT2A-dependence test. With n=2-5 per cell it is underpowered -- report the estimate and CI, and do not lean on the p-value. | nan         | nan         |

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