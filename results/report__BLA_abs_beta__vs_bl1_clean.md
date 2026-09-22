# Statistical report — metric: `BLA_abs_beta__vs_bl1`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |     ci_lo |      ci_hi |         t |   p_paired_t |   wilcoxon_p |         dz |   estimate |        p_lmm |   n_obs |
|:---------------------------|----------:|------------:|----------:|-----------:|----------:|-------------:|-------------:|-----------:|-----------:|-------------:|--------:|
| C1+C2 crossover psi vs sal |        11 |   -0.445595 |  -0.71115 |  -0.199081 |  -3.26255 |   0.00853716 |   0.00976562 |  -0.983697 | nan        | nan          |     nan |
| LMM drug[T.sal]            |       nan |  nan        | nan       | nan        | nan       | nan          | nan          | nan        |   0.408642 |   0.00301241 |      24 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |   -0.493804 |   0.00677289 |
| C1_F2           |   -0.439395 |   0.0172261  |
| C1_F3           |   -0.488176 |   0.00783993 |
| C1_M1           |   -0.404303 |   0.0204077  |
| C1_M2           |   -0.399782 |   0.0203601  |
| C1_M3           |   -0.470402 |   0.0114011  |
| C2_F1           |   -0.358514 |   0.0130955  |
| C2_F3           |   -0.432706 |   0.0182203  |
| C2_M1           |   -0.478793 |   0.00969827 |
| C2_M2           |   -0.435562 |   0.0178128  |
| C2_M3           |   -0.500113 |   0.00563805 |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |    p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|----------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |  -0.536288  | 0.0755924 |       0.222222  |  -1.20954  |     0.185231 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |   0.453744  | 0.123488  |       0.0952381 |   0.968411 |     0.185231 |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |  -0.0825438 | 0.785121  |       0.84127   |  -0.154584 |     0.785121 |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |   estimate |           p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------:|------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan        | nan         |
| OLS Intercept                        | nan                                                                                                                                                                          |   0.134347 |   0.513449  |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |  -0.482634 |   0.0783267 |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |   0.12023  |   0.741736  |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |  -0.10111  |   0.685691  |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   0.283443 |   0.555337  |
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