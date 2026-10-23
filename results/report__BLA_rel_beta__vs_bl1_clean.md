# Statistical report — metric: `BLA_rel_beta__vs_bl1`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |    ci_lo |      ci_hi |         t |   p_paired_t |   wilcoxon_p |         dz |   estimate |       p_lmm |   n_obs |
|:---------------------------|----------:|------------:|---------:|-----------:|----------:|-------------:|-------------:|-----------:|-----------:|------------:|--------:|
| C1+C2 crossover psi vs sal |        11 |   -0.694808 |  -1.2372 |  -0.126212 |  -2.32613 |    0.0423284 |    0.0673828 |  -0.701355 |  nan       | nan         |     nan |
| LMM drug[T.sal]            |       nan |  nan        | nan      | nan        | nan       |  nan         |  nan         | nan        |    0.68274 |   0.0155144 |      24 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |   -0.728969 |   0.0533814  |
| C1_F2           |   -0.68725  |   0.0670645  |
| C1_F3           |   -0.662867 |   0.074252   |
| C1_M1           |   -0.603756 |   0.0870984  |
| C1_M2           |   -0.893411 |   0.00555336 |
| C1_M3           |   -0.643793 |   0.0792318  |
| C2_F1           |   -0.52782  |   0.0859781  |
| C2_F3           |   -0.6869   |   0.0671729  |
| C2_M1           |   -0.657221 |   0.0757926  |
| C2_M2           |   -0.735484 |   0.0511547  |
| C2_M3           |   -0.815416 |   0.0244291  |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |    p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|----------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |   -0.814866 | 0.0276972 |       0.031746  |  -1.55741  |    0.0830917 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |    0.36392  | 0.157184  |       0.0952381 |   0.841916 |    0.157184  |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |   -0.450946 | 0.126087  |       0.150794  |  -0.977159 |    0.157184  |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |    estimate |           p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------:|------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan         | nan         |
| OLS Intercept                        | nan                                                                                                                                                                          |  -0.0243744 |   0.896274  |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |  -0.507939  |   0.0452229 |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |   0.504691  |   0.140605  |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |  -0.188715  |   0.41171   |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   0.202185  |   0.644808  |
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