# Statistical report — metric: `BLA-vHPC_wpli_theta_winmean`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |       ci_lo |        ci_hi |         t |   p_paired_t |   wilcoxon_p |         dz |    estimate |       p_lmm |   n_obs |
|:---------------------------|----------:|------------:|------------:|-------------:|----------:|-------------:|-------------:|-----------:|------------:|------------:|--------:|
| C1+C2 crossover psi vs sal |        11 |  -0.0393326 |  -0.0679291 |  -0.00624174 |  -2.37507 |    0.0389386 |    0.0673828 |  -0.716111 | nan         | nan         |     nan |
| LMM drug[T.sal]            |       nan | nan         | nan         | nan          | nan       |  nan         |  nan         | nan        |   0.0399163 |   0.0147824 |      24 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |  -0.0510721 |   0.00332957 |
| C1_F2           |  -0.0339019 |   0.0816313  |
| C1_F3           |  -0.0379126 |   0.0674367  |
| C1_M1           |  -0.03629   |   0.0745451  |
| C1_M2           |  -0.0427701 |   0.0406839  |
| C1_M3           |  -0.0458122 |   0.0236459  |
| C2_F1           |  -0.0366072 |   0.0732754  |
| C2_F3           |  -0.0360734 |   0.0753743  |
| C2_M1           |  -0.0329321 |   0.082928   |
| C2_M2           |  -0.041889  |   0.0458054  |
| C2_M3           |  -0.0373978 |   0.0698475  |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |     p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|-----------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |  -0.143631  | 0.00079992 |      0.00793651 |  -2.41861  |   0.00239976 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |   0.0658672 | 0.146385   |      0.222222   |   0.847073 |   0.146385   |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |  -0.0777639 | 0.0554945  |      0.0952381  |  -1.37481  |   0.0832417  |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |    estimate |             p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------:|--------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 | nan         | nan           |
| OLS Intercept                        | nan                                                                                                                                                                          |   0.477439  |   1.81473e-14 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |  -0.0585014 |   0.0789387   |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |   0.0650265 |   0.152419    |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |  -0.0206447 |   0.497992    |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   0.0370845 |   0.525592    |
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