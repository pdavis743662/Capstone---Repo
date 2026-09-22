# Statistical report — metric: `vHPC_abs_theta`

## crossover_C1C2

| analysis                   |   n_pairs |   mean_diff |    ci_lo |   ci_hi |         t |   p_paired_t |   wilcoxon_p |         dz |   estimate |       p_lmm |   n_obs |
|:---------------------------|----------:|------------:|---------:|--------:|----------:|-------------:|-------------:|-----------:|-----------:|------------:|--------:|
| C1+C2 crossover psi vs sal |        12 |       49252 | -1064.85 | 98944.4 |   1.85732 |    0.0902203 |    0.0922852 |   0.536162 |      nan   | nan         |     nan |
| LMM drug[T.sal]            |       nan |         nan |   nan    |   nan   | nan       |  nan         |  nan         | nan        |   -50867.1 |   0.0545759 |      25 |

## crossover_loo

| dropped_mouse   |   mean_diff |   p_paired_t |
|:----------------|------------:|-------------:|
| C1_F1           |     57751.8 |    0.0621988 |
| C1_F2           |     53889   |    0.0889147 |
| C1_F3           |     51911.4 |    0.102703  |
| C1_M1           |     36846.6 |    0.181769  |
| C1_M2           |     53292.6 |    0.0930836 |
| C1_M3           |     64563.2 |    0.0214793 |
| C1_M4           |     46919.8 |    0.135979  |
| C2_F1           |     46245.5 |    0.140166  |
| C2_F3           |     41008.3 |    0.168292  |
| C2_M1           |     47753.8 |    0.130673  |
| C2_M2           |     36830   |    0.181799  |
| C2_M3           |     54012.1 |    0.0880533 |

## threearm_C3

| analysis                                          |   n1 |   n2 |   mean_diff |   p_perm |   p_mannwhitney |   hedges_g |   p_perm_fdr |
|:--------------------------------------------------|-----:|-----:|------------:|---------:|----------------:|-----------:|-------------:|
| C3 psi vs sal (is there an effect?)               |    5 |    5 |    -87346.4 | 0.844916 |        0.84127  | -0.224857  |     0.915708 |
| C3 ket vs psi (is it 5-HT2A dependent?)           |    5 |    5 |     49974.1 | 0.684832 |        0.84127  |  0.226006  |     0.915708 |
| C3 ket vs sal (did the blocker restore baseline?) |    5 |    5 |    -37372.3 | 0.915708 |        0.690476 | -0.0940987 |     0.915708 |

## pooled_2x2_C3C4

| analysis                             | note                                                                                                                                                                         |   estimate |             p |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------:|--------------:|
| cell counts                          | {('ket', 'psi'): 7, ('ket', 'sal'): 4, ('sal', 'psi'): 8, ('sal', 'sal'): 6}                                                                                                 |      nan   | nan           |
| OLS Intercept                        | nan                                                                                                                                                                          |   445147   |   0.000697835 |
| OLS C(blocker)[T.sal]                | nan                                                                                                                                                                          |   -72451.8 |   0.618493    |
| OLS C(drug)[T.sal]                   | nan                                                                                                                                                                          |  -149920   |   0.458038    |
| OLS C(cohort)[T.C4]                  | nan                                                                                                                                                                          |     1533.6 |   0.991087    |
| OLS C(blocker)[T.sal]:C(drug)[T.sal] | nan                                                                                                                                                                          |   218825   |   0.410274    |
| INTERPRETATION                       | The C(blocker):C(drug) interaction term is the 5-HT2A-dependence test. With n=2-5 per cell it is underpowered -- report the estimate and CI, and do not lean on the p-value. |      nan   | nan           |

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