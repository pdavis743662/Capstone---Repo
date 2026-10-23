# Statistical report — metric: `BLA_abs_theta__vs_bl1`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |       ci_lo |     ci_hi |         t |   p_paired_t |   wilcoxon_p |         dz |   estimate |       p_lmm |   n_obs |
|:---------------------------|----------:|------------:|------------:|----------:|----------:|-------------:|-------------:|-----------:|-----------:|------------:|--------:|
| C1+C2 crossover psi vs sal |        11 |    0.657073 |   0.0777097 |   1.21157 |   2.16727 |    0.0554248 |    0.0673828 |   0.653457 |  nan       | nan         |     nan |
| LMM drug[T.sal]            |       nan |  nan        | nan         | nan       | nan       |  nan         |  nan         | nan        |   -0.70849 |   0.0136772 |      24 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |    0.742456 |    0.0463466 |
| C1_F2           |    0.597961 |    0.102279  |
| C1_F3           |    0.578905 |    0.107479  |
| C1_M1           |    0.629971 |    0.0917651 |
| C1_M2           |    0.829759 |    0.0146709 |
| C1_M3           |    0.682904 |    0.071202  |
| C2_F1           |    0.490111 |    0.113719  |
| C2_F3           |    0.622239 |    0.0944761 |
| C2_M1           |    0.585582 |    0.105763  |
| C2_M2           |    0.674927 |    0.0744653 |
| C2_M3           |    0.792991 |    0.0266175 |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |     p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|-----------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |    1.03376  | 0.00729927 |      0.00793651 |   2.64236  |    0.0128987 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |   -0.38765  | 0.206079   |      0.222222   |  -0.791154 |    0.206079  |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |    0.646106 | 0.00859914 |      0.015873   |   1.72741  |    0.0128987 |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |   estimate |             p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------:|--------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan        | nan           |
| OLS Intercept                        | nan                                                                                                                                                                          |   1.31911  |   5.60126e-09 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |   0.325277 |   0.079142    |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |  -0.410562 |   0.106919    |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |  -0.35644  |   0.0447131   |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |  -0.459185 |   0.165996    |
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