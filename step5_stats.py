"""
Stage 5 -- Statistics that respect the design.

Three model families, matching the three designs in this dataset:
    1. C1/C2 crossover      -> mixed model with random intercept per mouse
    2. C3 three-arm         -> planned contrasts (psi vs sal; ket vs psi)
    3. C3+C4 pooled 2x2     -> blocker * drug interaction = the 5-HT2A test

Everything aggregates to ONE VALUE PER ANIMAL first. Read Aarts et al. (2014,
Nat Neurosci) before changing that.

Run:
    python step5_stats.py --features ../derived/features_session.csv \
                          --metric burst_rate_per_min --out ../results
    python step5_stats.py --features ../derived/features_dynamic.csv \
                          --metrics primary --out ../results
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "python"))
from lfp_config import PRIMARY_METRICS  # noqa: E402
from exclusions import (  # noqa: E402
    apply_exclusions,
    bad_channel_map,
    exclusion_report,
    find_bad_channels,
)

try:
    import statsmodels.formula.api as smf
    HAVE_SM = True
except ImportError:
    HAVE_SM = False

CHECKLIST = [
    "## Reporting checklist",
    "- [ ] Unit of analysis is the animal, not the burst or the time window",
    "- [ ] Effect sizes with bootstrap CIs reported alongside every p-value",
    "- [ ] FDR correction applied across the primary metric family",
    "- [ ] Primary hypothesis was declared before looking; everything else "
    "labelled exploratory",
    "- [ ] Artifact-rejection rates compared across groups",
    "- [ ] Sensitivity analysis reported for any null result",
    "- [ ] Dead-channel exclusions reported with per-group counts",
]


def _formula_frame(df: pd.DataFrame, metric: str) -> tuple[pd.DataFrame, str]:
    """Rename hyphenated metrics so patsy formulas parse."""
    safe = metric.replace("-", "_")
    if safe == metric:
        return df, metric
    return df.rename(columns={metric: safe}), safe


def parse_metrics(metric: str | None, metrics: str | None) -> list[str]:
    """``--metrics primary`` or a comma list; else a single ``--metric``."""
    if metrics:
        raw = metrics.strip()
        if raw.lower() == "primary":
            return list(PRIMARY_METRICS)
        return [m.strip() for m in raw.split(",") if m.strip()]
    return [metric or "burst_rate_per_min"]


# ------------------------------------------------------------------
def to_animal_level(df: pd.DataFrame, metric: str, rectypes) -> pd.DataFrame:
    """One row per animal per condition. Do this before any test."""
    sub = df[df.rectype.isin(rectypes)].dropna(subset=[metric])
    return (sub.groupby(["cohort", "group", "blocker", "drug", "mouse",
                         "sex", "subject_uid"], as_index=False)[metric]
               .mean())


def bootstrap_ci(x, n=10000, stat=np.mean, alpha=.05, seed=0):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) < 2:
        return (np.nan, np.nan)
    b = [stat(rng.choice(x, len(x), replace=True)) for _ in range(n)]
    return tuple(np.percentile(b, [100 * alpha / 2, 100 * (1 - alpha / 2)]))


def hedges_g(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return np.nan
    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    d = (a.mean() - b.mean()) / sp if sp > 0 else np.nan
    J = 1 - 3 / (4 * (na + nb) - 9)
    return d * J


def perm_test_2group(a, b, n=10000, seed=0):
    """Label-shuffling test on the difference in means. No distributional
    assumptions -- the right default at n=5."""
    rng = np.random.default_rng(seed)
    a, b = np.asarray(a, float), np.asarray(b, float)
    obs = a.mean() - b.mean()
    pool = np.concatenate([a, b])
    cnt = 0
    for _ in range(n):
        rng.shuffle(pool)
        if abs(pool[:len(a)].mean() - pool[len(a):].mean()) >= abs(obs):
            cnt += 1
    return obs, (cnt + 1) / (n + 1)


def fdr(pvals, q=.05):
    """Benjamini-Hochberg. Returns (rejected, adjusted p)."""
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    ranked = p[order]
    m = len(p)
    adj = ranked * m / (np.arange(m) + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    out = np.empty(m); out[order] = np.minimum(adj, 1)
    return out < q, out


# ------------------------------------------------------------------
def analysis_crossover(df, metric, rectypes=("EZM",)) -> tuple[pd.DataFrame, pd.DataFrame]:
    a = to_animal_level(df[df.cohort.isin(["C1", "C2"])], metric, rectypes)
    empty_loo = pd.DataFrame(columns=["dropped_mouse", "mean_diff", "p_paired_t"])
    if a.empty or not {"sal", "psi"}.issubset(set(a.drug.unique())):
        return pd.DataFrame([{
            "analysis": "C1+C2 crossover skipped",
            "note": "Need EZM rows for both sal and psi.",
        }]), empty_loo
    piv = a.pivot_table(index=["cohort", "mouse"], columns="drug", values=metric)
    missing = [c for c in ("sal", "psi") if c not in piv.columns]
    if missing:
        return pd.DataFrame([{
            "analysis": "C1+C2 crossover skipped",
            "note": f"pivot missing columns {missing}",
        }]), empty_loo
    piv = piv.dropna(subset=["sal", "psi"])
    d = piv["psi"] - piv["sal"]

    rows = []
    if len(d) >= 3:
        t, pt = stats.ttest_rel(piv["psi"], piv["sal"])
        try:
            w, pw = stats.wilcoxon(piv["psi"], piv["sal"])
        except ValueError:
            w, pw = np.nan, np.nan
        lo, hi = bootstrap_ci(d.values)
        rows.append(dict(analysis="C1+C2 crossover psi vs sal", n_pairs=len(d),
                         mean_diff=float(d.mean()), ci_lo=lo, ci_hi=hi,
                         t=float(t), p_paired_t=float(pt),
                         wilcoxon_p=float(pw) if np.isfinite(pw) else np.nan,
                         dz=float(d.mean() / d.std(ddof=1)) if d.std(ddof=1) > 0 else np.nan))

    if HAVE_SM and len(a) >= 6:
        try:
            a_m, mname = _formula_frame(a, metric)
            m = smf.mixedlm(f"{mname} ~ drug + cohort", a_m,
                            groups=a_m["mouse"] + "_" + a_m["cohort"]).fit()
            for name in m.params.index:
                if name.startswith("drug"):
                    rows.append(dict(analysis=f"LMM {name}",
                                     estimate=float(m.params[name]),
                                     p_lmm=float(m.pvalues[name]),
                                     n_obs=len(a)))
        except Exception as e:                          # noqa: BLE001
            rows.append(dict(analysis="LMM failed", note=repr(e)))

    loo_rows = []
    if len(piv) >= 3:
        for idx in piv.index:
            rest = piv.drop(idx)
            t_loo, p_loo = stats.ttest_rel(rest["psi"], rest["sal"])
            d_loo = rest["psi"] - rest["sal"]
            cohort, mouse = idx
            loo_rows.append(dict(
                dropped_mouse=f"{cohort}_{mouse}",
                mean_diff=float(d_loo.mean()),
                p_paired_t=float(p_loo),
            ))
    loo = pd.DataFrame(loo_rows, columns=["dropped_mouse", "mean_diff", "p_paired_t"])
    return pd.DataFrame(rows), loo


def analysis_c3(df, metric, rectypes=("EPM",)) -> pd.DataFrame:
    a = to_animal_level(df[df.cohort == "C3"], metric, rectypes)
    g = {k: v[metric].values for k, v in a.groupby("group")}
    rows = []
    for lbl, (x, y) in {
        "C3 psi vs sal (is there an effect?)": ("psi", "sal"),
        "C3 ket vs psi (is it 5-HT2A dependent?)": ("ket", "psi"),
        "C3 ket vs sal (did the blocker restore baseline?)": ("ket", "sal"),
    }.items():
        if x in g and y in g:
            obs, p = perm_test_2group(g[x], g[y])
            u, pu = stats.mannwhitneyu(g[x], g[y], alternative="two-sided")
            rows.append(dict(analysis=lbl, n1=len(g[x]), n2=len(g[y]),
                             mean_diff=float(obs), p_perm=p,
                             p_mannwhitney=float(pu),
                             hedges_g=hedges_g(g[x], g[y])))
    if rows:
        rej, padj = fdr([r["p_perm"] for r in rows])
        for r, pa in zip(rows, padj):
            r["p_perm_fdr"] = float(pa)
    return pd.DataFrame(rows)


def analysis_pooled_2x2(df, metric, rectypes=("EPM",)) -> pd.DataFrame:
    a = to_animal_level(df[df.cohort.isin(["C3", "C4"])], metric, rectypes)
    rows = [dict(analysis="cell counts",
                 note=str(a.groupby(["blocker", "drug"]).size().to_dict()))]
    if HAVE_SM and len(a) >= 8:
        try:
            a_m, mname = _formula_frame(a, metric)
            m = smf.ols(f"{mname} ~ C(blocker) * C(drug) + C(cohort)", a_m).fit()
            for name in m.params.index:
                rows.append(dict(analysis=f"OLS {name}",
                                 estimate=float(m.params[name]),
                                 p=float(m.pvalues[name])))
            rows.append(dict(analysis="INTERPRETATION",
                             note="The C(blocker):C(drug) interaction term is the "
                                  "5-HT2A-dependence test. With n=2-5 per cell it is "
                                  "underpowered -- report the estimate and CI, and do "
                                  "not lean on the p-value."))
        except Exception as e:                          # noqa: BLE001
            rows.append(dict(analysis="OLS failed", note=repr(e)))
    return pd.DataFrame(rows)


def sensitivity(df, metric, rectypes=("EPM",)) -> pd.DataFrame:
    """What effect size could you actually have detected? Report this."""
    a = to_animal_level(df[df.cohort == "C3"], metric, rectypes)
    n = int(a.groupby("group").size().min()) if len(a) else 0
    rows = []
    for power in (.8, .9):
        za = stats.norm.ppf(1 - .025)
        zb = stats.norm.ppf(power)
        d = (za + zb) * np.sqrt(2 / n) if n else np.nan
        rows.append(dict(analysis=f"minimum detectable Cohen's d at {power:.0%} power",
                         n_per_group=n, d=float(d)))
    rows.append(dict(analysis="INTERPRETATION",
                     note="If that d is larger than effects typical in this "
                          "literature, a null result here is uninformative -- say so "
                          "explicitly in the discussion rather than claiming 'no effect'."))
    return pd.DataFrame(rows)


def _exclusion_markdown(bad: pd.DataFrame, summary: pd.DataFrame,
                        n_files: int) -> list[str]:
    n_flagged = 0 if bad.empty else int(bad.stem.nunique())
    reason = (
        bad.groupby("reason").stem.nunique().rename("n_files").reset_index()
        if not bad.empty else pd.DataFrame(columns=["reason", "n_files"])
    )
    lines = [
        "## Channel exclusions",
        "",
        "Policy (applied before every test): a region's metrics are set to NaN "
        "when `log10(RMS) < 2.0` (dead channel; main clouds sit near 2.6–2.9, "
        "a distinct cluster sits near 1.05), when excess kurtosis > 20, or when "
        "the channel is missing. Burst columns require a live BLA; phase-lag "
        "columns require live BLA and vHPC. Other regions on the same recording "
        "are kept.",
        "",
        f"- Files in the features table: **{n_files}**",
        f"- Files with ≥1 excluded channel: **{n_flagged}**",
        "",
        "### By criterion (unique files)",
        "",
        reason.to_markdown(index=False) if len(reason) else "_none_",
        "",
        "### Per (cohort, group, region)",
        "",
        summary.to_markdown(index=False) if len(summary) else "_none_",
        "",
    ]
    return lines


def _crossover_row(xtab: pd.DataFrame) -> pd.Series | None:
    if xtab is None or xtab.empty:
        return None
    if "analysis" in xtab.columns:
        hit = xtab[xtab["analysis"] == "C1+C2 crossover psi vs sal"]
        if not hit.empty:
            return hit.iloc[0]
    return xtab.iloc[0]


def _crossover_p(xtab: pd.DataFrame) -> float:
    row = _crossover_row(xtab)
    if row is None or "p_paired_t" not in row.index:
        return float("nan")
    val = row["p_paired_t"]
    return float(val) if pd.notna(val) else float("nan")


def _run_one(df: pd.DataFrame, metric: str, out: Path, suffix: str) -> dict:
    xtab, loo = analysis_crossover(df, metric)
    blocks = {
        "crossover_C1C2": xtab,
        "crossover_loo": loo,
        "threearm_C3": analysis_c3(df, metric),
        "pooled_2x2_C3C4": analysis_pooled_2x2(df, metric),
        "sensitivity": sensitivity(df, metric),
    }
    safe_file = metric.replace("/", "_")
    lines = [f"# Statistical report — metric: `{metric}`", ""]
    for name, tbl in blocks.items():
        dest = out / f"{name}__{safe_file}{suffix}.csv"
        tbl.to_csv(dest, index=False)
        lines += [f"## {name}", "", tbl.to_markdown(index=False), ""]
        print(f"\n=== {metric} / {name} ===")
        print(tbl.to_string(index=False) if len(tbl) else "(empty)")
    lines += CHECKLIST
    report = out / f"report__{safe_file}{suffix}.md"
    report.write_text("\n".join(lines))
    print(f"Wrote {report}")
    row = _crossover_row(xtab)
    return {
        "metric": metric,
        "p_crossover": _crossover_p(xtab),
        "n_pairs": float(row["n_pairs"]) if row is not None and "n_pairs" in row.index else float("nan"),
        "mean_diff": float(row["mean_diff"]) if row is not None and "mean_diff" in row.index else float("nan"),
    }


def run(*, features: Path, out: Path, metric: str = "burst_rate_per_min",
        metrics: str | None = None, qc_path: Path | None = None,
        exclude: bool = True) -> None:
    out.mkdir(parents=True, exist_ok=True)
    suffix = "_clean" if exclude else ""
    wanted = parse_metrics(metric, metrics)

    df = pd.read_csv(features)
    missing = [m for m in wanted if m not in df.columns]
    keep = [m for m in wanted if m in df.columns]
    if missing:
        print("Skipping metrics not in the features table:\n  " + "\n  ".join(missing))
    if not keep:
        raise SystemExit("None of the requested metrics are in the features table.")

    n_files = len(df)
    excl_md = [
        "## Channel exclusions",
        "",
        "_Exclusions off (`--no-exclude`)._",
        "",
    ]
    if exclude:
        qc_p = Path(qc_path) if qc_path is not None else features.parent / "qc.csv"
        if not qc_p.exists():
            raise SystemExit(f"--exclude requires a QC table: {qc_p} not found")
        qc = pd.read_csv(qc_p)
        bad = find_bad_channels(qc)
        df, audit = apply_exclusions(df, bad_channel_map(bad))
        summary = exclusion_report(audit if not audit.empty else bad, qc)
        excl_md = _exclusion_markdown(bad, summary, n_files)

    summaries = [_run_one(df, m, out, suffix) for m in keep]
    fdr_tbl = pd.DataFrame(summaries)
    if len(fdr_tbl) >= 2 and fdr_tbl["p_crossover"].notna().sum() >= 2:
        p = fdr_tbl["p_crossover"].to_numpy(float)
        finite = np.isfinite(p)
        padj = np.full_like(p, np.nan, dtype=float)
        rej = np.zeros(len(p), dtype=bool)
        if finite.any():
            r, a = fdr(p[finite])
            padj[finite] = a
            rej[finite] = r
        fdr_tbl["p_crossover_fdr"] = padj
        fdr_tbl["reject_fdr"] = rej
    dest = out / f"primary_metrics_fdr{suffix}.csv"
    fdr_tbl.to_csv(dest, index=False)

    header = keep[0] if len(keep) == 1 else "primary_metrics"
    lines = [f"# Statistical report — metrics: {', '.join(f'`{m}`' for m in keep)}", ""]
    if exclude:
        lines += ["_Dead channels excluded. Filenames use the `_clean` suffix._", ""]
    lines += excl_md
    lines += ["## C1/C2 crossover FDR across metrics", "",
              fdr_tbl.to_markdown(index=False), ""]
    lines += CHECKLIST
    summary_report = out / f"report__{header}{suffix}.md"
    if len(keep) > 1:
        summary_report = out / f"report__primary_metrics{suffix}.md"
    summary_report.write_text("\n".join(lines))
    print(f"\nWrote {summary_report}")
    print(f"Wrote {dest}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", required=True, type=Path)
    ap.add_argument("--metric", default="burst_rate_per_min")
    ap.add_argument("--metrics", default=None,
                    help="comma-separated list, or 'primary' for the declared set")
    ap.add_argument("--out", default=Path("../results"), type=Path)
    ap.add_argument("--qc", default=None, type=Path,
                    help="QC table (default: <features-dir>/qc.csv)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--exclude", dest="exclude", action="store_true")
    g.add_argument("--no-exclude", dest="exclude", action="store_false")
    ap.set_defaults(exclude=True)
    args = ap.parse_args()
    run(features=args.features, out=args.out, metric=args.metric,
        metrics=args.metrics, qc_path=args.qc, exclude=args.exclude)


if __name__ == "__main__":
    main()
