# Statistical report — metric: `BLA-vHPC_wpli_beta`

## crossover_C1C2

| analysis                   |   n_pairs |    mean_diff |       ci_lo |       ci_hi |          t |   p_paired_t |   wilcoxon_p |        dz |     estimate |      p_lmm |   n_obs |
|:---------------------------|----------:|-------------:|------------:|------------:|-----------:|-------------:|-------------:|----------:|-------------:|-----------:|--------:|
| C1+C2 crossover psi vs sal |        11 |   0.00924982 |  -0.0212372 |   0.0381695 |   0.583326 |     0.572594 |     0.464844 |   0.17588 | nan          | nan        |     nan |
| LMM drug[T.sal]            |       nan | nan          | nan         | nan         | nan        |   nan        |   nan        | nan       |  -0.00967691 |   0.533729 |      24 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           | 0.000614832 |     0.967559 |
| C1_F2           | 0.00786667  |     0.663037 |
| C1_F3           | 0.0141153   |     0.419483 |
| C1_M1           | 0.0183164   |     0.234734 |
| C1_M2           | 0.00331977  |     0.842751 |
| C1_M3           | 0.00800947  |     0.65761  |
| C2_F1           | 0.0155773   |     0.35783  |
| C2_F3           | 0.00941159  |     0.604357 |
| C2_M1           | 0.0098549   |     0.587469 |
| C2_M2           | 0.00953772  |     0.599557 |
| C2_M3           | 0.00512409  |     0.768983 |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |   p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|---------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 | -0.00845432 | 0.749425 |        1        |  -0.220484 |     0.845615 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 | -0.00599165 | 0.845615 |        0.84127  |  -0.125146 |     0.845615 |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 | -0.014446   | 0.661034 |        0.690476 |  -0.261489 |     0.845615 |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |    estimate |             p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------:|--------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan         | nan           |
| OLS Intercept                        | nan                                                                                                                                                                          |   0.0920135 |   0.000384314 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |   0.0226779 |   0.424779    |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |  -0.0163605 |   0.675399    |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |   0.0105148 |   0.694039    |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   0.0427579 |   0.407729    |
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