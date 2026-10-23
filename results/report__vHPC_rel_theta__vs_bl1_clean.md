# Statistical report — metric: `vHPC_rel_theta__vs_bl1`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |      ci_lo |     ci_hi |        t |   p_paired_t |   wilcoxon_p |         dz |   estimate |        p_lmm |   n_obs |
|:---------------------------|----------:|------------:|-----------:|----------:|---------:|-------------:|-------------:|-----------:|-----------:|-------------:|--------:|
| C1+C2 crossover psi vs sal |        12 |    0.426584 |   0.148732 |   0.68094 |   2.9723 |    0.0126932 |   0.00927734 |   0.858028 | nan        | nan          |     nan |
| LMM drug[T.sal]            |       nan |  nan        | nan        | nan       | nan      |  nan         | nan          | nan        |  -0.460421 |   0.00157824 |      25 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |    0.525951 |  0.000927168 |
| C1_F2           |    0.450903 |  0.0155625   |
| C1_F3           |    0.395399 |  0.0275802   |
| C1_M1           |    0.364696 |  0.0278431   |
| C1_M2           |    0.401467 |  0.0267845   |
| C1_M3           |    0.460012 |  0.013147    |
| C1_M4           |    0.455765 |  0.014269    |
| C2_F1           |    0.393603 |  0.0277768   |
| C2_F3           |    0.376806 |  0.0286016   |
| C2_M1           |    0.453057 |  0.014989    |
| C2_M2           |    0.432219 |  0.0204331   |
| C2_M3           |    0.409129 |  0.0255205   |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |     p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|-----------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |    0.604809 | 0.00669933 |      0.00793651 |   1.40522  |     0.020098 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |   -0.48708  | 0.0834917  |      0.0952381  |  -1.14078  |     0.125237 |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |    0.117728 | 0.714029   |      1          |   0.214887 |     0.714029 |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |   estimate |           p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------:|------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan        | nan         |
| OLS Intercept                        | nan                                                                                                                                                                          |   0.492255 |   0.0175117 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |   0.115316 |   0.642759  |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |  -0.247702 |   0.473037  |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |  -0.452368 |   0.0651046 |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |  -0.219136 |   0.62761   |
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