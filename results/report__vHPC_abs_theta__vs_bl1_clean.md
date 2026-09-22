# Statistical report — metric: `vHPC_abs_theta__vs_bl1`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |      ci_lo |      ci_hi |         t |   p_paired_t |   wilcoxon_p |         dz |   estimate |        p_lmm |   n_obs |
|:---------------------------|----------:|------------:|-----------:|-----------:|----------:|-------------:|-------------:|-----------:|-----------:|-------------:|--------:|
| C1+C2 crossover psi vs sal |        12 |    0.605694 |   0.184907 |   0.971112 |   2.86709 |    0.0153212 |    0.0341797 |   0.827656 | nan        | nan          |     nan |
| LMM drug[T.sal]            |       nan |  nan        | nan        | nan        | nan       |  nan         |  nan         | nan        |  -0.673731 |   0.00263623 |      25 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |    0.758972 |  0.000761969 |
| C1_F2           |    0.669045 |  0.0126665   |
| C1_F3           |    0.562654 |  0.0323549   |
| C1_M1           |    0.602022 |  0.0264096   |
| C1_M2           |    0.662458 |  0.0140015   |
| C1_M3           |    0.616605 |  0.023574    |
| C1_M4           |    0.56904  |  0.0316219   |
| C2_F1           |    0.555185 |  0.0330665   |
| C2_F3           |    0.520858 |  0.0338177   |
| C2_M1           |    0.544477 |  0.0337791   |
| C2_M2           |    0.62721  |  0.0213974   |
| C2_M3           |    0.579807 |  0.0301569   |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |    p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|----------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |    0.864961 | 0.0570943 |       0.0952381 |   1.24282  |     0.171283 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |   -0.265556 | 0.478952  |       0.547619  |  -0.421585 |     0.478952 |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |    0.599405 | 0.146585  |       0.150794  |   0.89937  |     0.219878 |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |    estimate |             p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------:|--------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan         | nan           |
| OLS Intercept                        | nan                                                                                                                                                                          |   1.89883   |   8.35389e-07 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |  -0.0400329 |   0.90975     |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |  -0.740157  |   0.140595    |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |  -0.576546  |   0.0960468   |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   0.0309963 |   0.961461    |
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