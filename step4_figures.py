"""
Stage 4 -- The figure catalog.

Builds F0 (QC dashboard) through F10 from the CSVs/parquet written by later
stages. F7 needs the window table (Stage 6); F8–F10 need ``*_winmean`` / ``*_winvar``.

Run:
    python step4_figures.py --derived ../derived --out ../figures_clean
    python step4_figures.py --derived ../derived --no-exclude --out ../figures
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "python"))
from exclusions import (  # noqa: E402
    apply_exclusions,
    bad_channel_map,
    find_bad_channels,
)
from lfp_video import paint_wpli_triangle, triangle_edge_vals  # noqa: E402

plt.rcParams.update({
    "figure.dpi": 120, "savefig.dpi": 300, "savefig.bbox": "tight",
    "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
})

REGIONS = ("BLA", "vHPC", "mPFC")
BANDS = ("delta", "theta", "beta", "lgamma", "hgamma")
RECORDER = ["BL1", "inj", "EZM", "EPM", "BL2"]

TITLE_SUFFIX = ""


def _t(text: str) -> str:
    return f"{text}{TITLE_SUFFIX}"


def _boxplot(ax, data, labels, **kw):
    """matplotlib renamed labels -> tick_labels in 3.9; support both."""
    try:
        return ax.boxplot(data, tick_labels=labels, **kw)
    except TypeError:
        return ax.boxplot(data, labels=labels, **kw)


# ----------------------------------------------------------------- F0
def fig0_qc(qc: pd.DataFrame, out: Path) -> None:
    """QC dashboard. Build this FIRST and actually look at it."""
    fig, axes = plt.subplots(2, 3, figsize=(13, 7))

    ax = axes[0, 0]
    for ct, g in qc.groupby("cohort"):
        ax.scatter(g.duration_s / 60, np.random.normal(0, .06, len(g)) +
                   list(qc.cohort.unique()).index(ct), s=14, label=ct, alpha=.7)
    ax.set_yticks(range(qc.cohort.nunique()))
    ax.set_yticklabels(sorted(qc.cohort.unique()))
    ax.set_xlabel("recording duration (min)")
    ax.set_title(_t("F0a  Durations — look for outliers"))

    ax = axes[0, 1]
    if "pct_artifact_union" in qc:
        order = sorted(qc.group.unique())
        data = [qc.loc[qc.group == g, "pct_artifact_union"].dropna() for g in order]
        _boxplot(ax, data, order, showfliers=False)
        for i, d in enumerate(data, 1):
            ax.scatter(np.random.normal(i, .06, len(d)), d, s=10, alpha=.6)
        ax.set_ylabel("% samples flagged")
        ax.tick_params(axis="x", rotation=60)
    ax.set_title(_t("F0b  Artifact rate by group\n(imbalance here = confound)"))

    ax = axes[0, 2]
    rms = [c for c in qc.columns if c.endswith("_rms")]
    for c in rms:
        ax.scatter(np.random.normal(rms.index(c), .08, len(qc)),
                   np.log10(qc[c].replace(0, np.nan)), s=8, alpha=.5)
    ax.set_xticks(range(len(rms)))
    ax.set_xticklabels([c.replace("_rms", "") for c in rms])
    ax.set_ylabel("log10 RMS amplitude")
    ax.set_title(_t("F0c  Signal amplitude by region\n(flat = dead channel)"))

    ax = axes[1, 0]
    ct = pd.crosstab(qc.cohort, qc.rectype)
    im = ax.imshow(ct.values, cmap="Blues")
    ax.set_xticks(range(ct.shape[1])); ax.set_xticklabels(ct.columns)
    ax.set_yticks(range(ct.shape[0])); ax.set_yticklabels(ct.index)
    for i in range(ct.shape[0]):
        for j in range(ct.shape[1]):
            ax.text(j, i, ct.values[i, j], ha="center", va="center", fontsize=8)
    ax.set_title(_t("F0d  File inventory"))
    plt.colorbar(im, ax=ax, fraction=.04)

    ax = axes[1, 1]
    k = [c for c in qc.columns if c.endswith("_kurtosis")]
    if k:
        _boxplot(ax, [qc[c].dropna() for c in k],
                 [c.replace("_kurtosis", "") for c in k], showfliers=True)
        ax.axhline(0, ls=":", c="k", lw=.8)
        ax.set_ylabel("excess kurtosis")
    ax.set_title(_t("F0e  Kurtosis\n(very high = transient artifacts remain)"))

    ax = axes[1, 2]
    n = (qc.groupby(["cohort", "group"]).subject_uid.nunique()
           .rename("n_mice").reset_index())
    ax.axis("off")
    ax.table(cellText=n.values, colLabels=n.columns, loc="center", cellLoc="center")
    ax.set_title(_t("F0f  ANIMALS per group — your real n"))

    fig.suptitle(_t("F0 — Quality control dashboard"), fontweight="bold")
    fig.tight_layout()
    fig.savefig(out / "F0_qc_dashboard.pdf")
    plt.close(fig)


def fig0g_exclusions(audit: pd.DataFrame, qc: pd.DataFrame, out: Path) -> None:
    """Bar chart of excluded-file count per (cohort, group)."""
    fig, ax = plt.subplots(figsize=(8, 3.6))
    keys = (
        qc.groupby(["cohort", "group"]).size()
        .reset_index()[["cohort", "group"]]
        .drop_duplicates()
        .sort_values(["cohort", "group"])
    )
    labels = [f"{c} {g}" for c, g in keys.itertuples(index=False)]
    if audit is None or audit.empty:
        counts = np.zeros(len(keys), dtype=int)
    else:
        n = (
            audit.groupby(["cohort", "group"])
            .stem.nunique()
            .reindex(pd.MultiIndex.from_frame(keys), fill_value=0)
        )
        counts = n.to_numpy()
    ax.bar(range(len(labels)), counts, color="0.35")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=60, ha="right")
    ax.set_ylabel("files with ≥1 excluded channel")
    ax.set_title(_t("F0g  Dead / high-kurtosis channel exclusions"))
    fig.tight_layout()
    fig.savefig(out / "F0g_exclusions.pdf")
    plt.close(fig)


# ----------------------------------------------------------------- F3
def fig3_band_heatmap(norm: pd.DataFrame, out: Path) -> None:
    """Band power change vs that animal's own BL1, region x band, per group."""
    beh = norm[norm.rectype.isin(["EZM", "EPM", "inj"])]
    groups = sorted(beh.group.unique())
    if not groups:
        print("F3 skipped: no behavior rows after exclusions")
        return
    fig, axes = plt.subplots(1, len(groups), figsize=(2.4 * len(groups), 3.2),
                             squeeze=False, sharey=True)
    vmax = 0
    mats = {}
    for g in groups:
        sub = beh[beh.group == g]
        M = np.full((len(REGIONS), len(BANDS)), np.nan)
        for i, r in enumerate(REGIONS):
            for j, b in enumerate(BANDS):
                col = f"{r}_abs_{b}__vs_bl1"
                if col in sub:
                    per_animal = sub.groupby("subject_uid")[col].mean()
                    M[i, j] = per_animal.mean()
        mats[g] = M
        vmax = max(vmax, np.nanmax(np.abs(M)) if np.isfinite(M).any() else 0)

    if not np.isfinite(vmax) or vmax == 0:
        vmax = 1.0
    for k, g in enumerate(groups):
        ax = axes[0, k]
        im = ax.imshow(mats[g], cmap="RdBu_r", vmin=-vmax, vmax=vmax)
        ax.set_xticks(range(len(BANDS))); ax.set_xticklabels(BANDS, rotation=60)
        if k == 0:
            ax.set_yticks(range(len(REGIONS))); ax.set_yticklabels(REGIONS)
        ax.set_title(_t(g), fontsize=9)
    fig.colorbar(im, ax=axes.ravel().tolist(), fraction=.02, label="dB vs BL1")
    fig.suptitle(_t("F3 — Band power change from each animal's own baseline"),
                 fontweight="bold")
    fig.savefig(out / "F3_band_heatmap.pdf")
    plt.close(fig)


# ----------------------------------------------------------------- F4
def fig4_bursts(feat: pd.DataFrame, out: Path, metric="burst_rate_per_min") -> None:
    beh = feat[feat.rectype.isin(["EZM", "EPM"])]
    per_animal = (beh.groupby(["cohort", "group", "subject_uid"])[metric]
                    .mean().reset_index())
    cohorts = sorted(per_animal.cohort.unique())
    if not cohorts:
        print("F4 skipped: no behavior rows after exclusions")
        return
    fig, axes = plt.subplots(1, len(cohorts), figsize=(3 * len(cohorts), 3.4),
                             squeeze=False, sharey=True)
    for k, c in enumerate(cohorts):
        ax = axes[0, k]
        sub = per_animal[per_animal.cohort == c]
        order = sorted(sub.group.unique())
        for i, g in enumerate(order, 1):
            v = sub.loc[sub.group == g, metric].dropna()
            ax.scatter(np.random.normal(i, .07, len(v)), v, s=26,
                       alpha=.85, zorder=3)
            if len(v):
                ax.hlines(v.mean(), i - .25, i + .25, lw=2, color="k", zorder=4)
                se = v.std(ddof=1) / np.sqrt(len(v)) if len(v) > 1 else 0
                ax.vlines(i, v.mean() - se, v.mean() + se, lw=1.4, color="k", zorder=4)
        ax.set_xticks(range(1, len(order) + 1))
        ax.set_xticklabels(order, rotation=60)
        ax.set_title(_t(c))
        if k == 0:
            ax.set_ylabel(metric.replace("_", " "))
    fig.suptitle(_t("F4 — Beta burst rate during behavior (one point = one animal)"),
                 fontweight="bold")
    fig.tight_layout()
    fig.savefig(out / "F4_burst_rate.pdf")
    plt.close(fig)


# ----------------------------------------------------------------- F5
def fig5_slopegraph(feat: pd.DataFrame, out: Path, metric="burst_rate_per_min") -> None:
    """The crossover cohorts' superpower: each mouse is its own control."""
    sub = feat[(feat.cohort.isin(["C1", "C2"])) & (feat.rectype == "EZM")]
    if sub.empty or not {"sal", "psi"}.issubset(set(sub.drug.unique())):
        print("F5 skipped: need C1/C2 EZM rows for both sal and psi.")
        return
    piv = sub.pivot_table(index=["cohort", "mouse"], columns="drug", values=metric)
    missing = [c for c in ("sal", "psi") if c not in piv.columns]
    if missing:
        print(f"F5 skipped: pivot missing {missing}")
        return
    piv = piv.dropna(subset=["sal", "psi"], how="any")
    if piv.empty:
        print("F5 skipped: no mouse has both a saline and a psilocybin EZM.")
        return

    fig, ax = plt.subplots(figsize=(3.4, 4))
    for (c, m), r in piv.iterrows():
        ax.plot([0, 1], [r["sal"], r["psi"]], "-o", ms=5, lw=1.2, alpha=.75,
                color="tab:blue" if c == "C1" else "tab:orange")
    ax.hlines([piv["sal"].mean(), piv["psi"].mean()], [-.15, .85], [.15, 1.15],
              color="k", lw=2.5)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["saline", "psilocybin"])
    ax.set_xlim(-.35, 1.35)
    ax.set_ylabel(metric.replace("_", " "))
    ax.set_title(_t(f"F5 — Within-mouse crossover (n={len(piv)} paired)"),
                 fontweight="bold", fontsize=10)
    fig.savefig(out / "F5_crossover_slopegraph.pdf")
    plt.close(fig)


# ----------------------------------------------------------------- F6
def fig6_phase_polar(feat: pd.DataFrame, out: Path) -> None:
    """Circular data on circular axes. Arrow length = consistency."""
    beh = feat[feat.rectype.isin(["EZM", "EPM"])].dropna(
        subset=["phase_lag_circmean_rad"])
    if beh.empty:
        print("F6 skipped: no phase-lag rows after exclusions")
        return
    groups = sorted(beh.group.unique())
    ncol = min(4, len(groups))
    nrow = int(np.ceil(len(groups) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(3 * ncol, 3 * nrow),
                             subplot_kw={"projection": "polar"}, squeeze=False)
    for k, g in enumerate(groups):
        ax = axes[k // ncol][k % ncol]
        sub = beh[beh.group == g]
        a = sub.phase_lag_circmean_rad.values
        w = sub.phase_lag_resultant.fillna(1).values
        ax.hist(a, bins=18, range=(-np.pi, np.pi), alpha=.45)
        for ai, wi in zip(a, w):
            ax.annotate("", xy=(ai, wi * ax.get_ylim()[1]), xytext=(0, 0),
                        arrowprops=dict(arrowstyle="->", alpha=.55, lw=1))
        z = np.sum(w * np.exp(1j * a)) / np.sum(w) if len(a) else 0
        ax.annotate("", xy=(np.angle(z), np.abs(z) * ax.get_ylim()[1]),
                    xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", lw=2.6, color="crimson"))
        ax.set_title(_t(f"{g}  (n={len(a)})"), fontsize=9)
    for k in range(len(groups), nrow * ncol):
        axes[k // ncol][k % ncol].axis("off")
    fig.suptitle(_t("F6 — BLA−vHPC beta phase lag (positive = BLA leads)"),
                 fontweight="bold")
    fig.tight_layout()
    fig.savefig(out / "F6_phase_polar.pdf")
    plt.close(fig)


def _load_windows(derived: Path) -> pd.DataFrame | None:
    parquet = derived / "windows.parquet"
    csv_path = derived / "windows.csv"
    if parquet.exists():
        return pd.read_parquet(parquet)
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return None


def _example_c1_ezm_stems(feat: pd.DataFrame) -> tuple[str | None, str | None]:
    """One C1 psi EZM stem and one C1 sal EZM stem."""
    ezm = feat[(feat.cohort == "C1") & (feat.rectype == "EZM")]
    col = "BLA-vHPC_wpli_beta"
    if col in ezm.columns:
        ezm = ezm.dropna(subset=[col])
    if not {"psi", "sal"}.issubset(set(ezm.drug.unique())):
        return None, None
    psi = str(ezm.loc[ezm.drug == "psi", "stem"].iloc[0])
    sal = str(ezm.loc[ezm.drug == "sal", "stem"].iloc[0])
    return psi, sal


# ----------------------------------------------------------------- F7
def fig7_wpli_trace(windows: pd.DataFrame, feat: pd.DataFrame, out: Path) -> None:
    """Time-resolved BLA-vHPC beta wPLI for one psi vs one sal EZM."""
    col = "BLA-vHPC_wpli_beta"
    if windows is None or windows.empty or col not in windows.columns:
        print("F7 skipped: window table missing BLA-vHPC_wpli_beta")
        return
    psi, sal = _example_c1_ezm_stems(feat)
    if not psi or not sal:
        print("F7 skipped: need C1 EZM psi and sal stems")
        return
    fig, ax = plt.subplots(figsize=(8.5, 3.2))
    for stem, label, color in ((psi, "psi", "tab:blue"), (sal, "sal", "0.35")):
        sub = windows[windows.stem == stem].sort_values("t_start")
        if sub.empty:
            print(f"F7 skipped: {stem} not in window table")
            plt.close(fig)
            return
        tc = 0.5 * (sub.t_start + sub.t_end)
        ax.plot(tc, sub[col], lw=1.4, color=color, label=f"{label}  {stem}")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("BLA–vHPC β wPLI")
    ax.set_ylim(0, 1)
    ax.legend(fontsize=7)
    ax.set_title(_t("F7 — 10 s BLA–vHPC beta wPLI (example C1 EZM pair)"),
                 fontweight="bold")
    fig.savefig(out / "F7_wpli_trace.pdf")
    plt.close(fig)


# ----------------------------------------------------------------- F8
def fig8_wpli_var_slopegraph(feat: pd.DataFrame, out: Path) -> None:
    """C1/C2 crossover: variance of 10 s BLA-vHPC beta wPLI (Kirkby analog)."""
    metric = "BLA-vHPC_wpli_beta_winvar"
    if metric not in feat.columns:
        print("F8 skipped: BLA-vHPC_wpli_beta_winvar not in features")
        return
    sub = feat[(feat.cohort.isin(["C1", "C2"])) & (feat.rectype == "EZM")]
    if sub.empty or not {"sal", "psi"}.issubset(set(sub.drug.unique())):
        print("F8 skipped: need C1/C2 EZM rows for both sal and psi.")
        return
    piv = sub.pivot_table(index=["cohort", "mouse"], columns="drug", values=metric)
    missing = [c for c in ("sal", "psi") if c not in piv.columns]
    if missing:
        print(f"F8 skipped: pivot missing {missing}")
        return
    piv = piv.dropna(subset=["sal", "psi"], how="any")
    if piv.empty:
        print("F8 skipped: no mouse has both a saline and a psilocybin EZM.")
        return

    fig, ax = plt.subplots(figsize=(3.4, 4))
    for (c, _m), r in piv.iterrows():
        ax.plot([0, 1], [r["sal"], r["psi"]], "-o", ms=5, lw=1.2, alpha=.75,
                color="tab:blue" if c == "C1" else "tab:orange")
    ax.hlines([piv["sal"].mean(), piv["psi"].mean()], [-.15, .85], [.15, 1.15],
              color="k", lw=2.5)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["saline", "psilocybin"])
    ax.set_xlim(-.35, 1.35)
    ax.set_ylabel(metric.replace("_", " "))
    ax.set_title(_t(f"F8 — BLA–vHPC β wPLI variance (n={len(piv)} paired)"),
                 fontweight="bold", fontsize=10)
    fig.savefig(out / "F8_wpli_var_slopegraph.pdf")
    plt.close(fig)


def _ezm_minus_bl1(feat: pd.DataFrame, metric: str) -> pd.DataFrame:
    """One row per mouse-week: Δ = behavior (EZM/EPM) − BL1."""
    sub = feat[feat.cohort.isin(["C1", "C2"])]
    if metric not in sub.columns:
        return pd.DataFrame()
    beh = sub[sub.rectype.isin(["EZM", "EPM"])][
        ["cohort", "mouse", "drug", "session_uid", metric]
    ].rename(columns={metric: "beh"})
    bl1 = sub[sub.rectype == "BL1"][["session_uid", metric]].rename(columns={metric: "bl1"})
    m = beh.merge(bl1, on="session_uid", how="inner")
    m["delta"] = m["beh"] - m["bl1"]
    return m.dropna(subset=["delta"])


# ----------------------------------------------------------------- F9
def fig9_wpli_triangles(feat: pd.DataFrame, out: Path) -> None:
    """Per-mouse 2x2 β wPLI triangles: saline/psi × BL1/EZM."""
    sub = feat[feat.cohort.isin(["C1", "C2"])]
    uids = []
    for uid, g in sub.groupby("subject_uid"):
        drugs = set(g.drug)
        recs = set(g.rectype)
        if {"sal", "psi"} <= drugs and "BL1" in recs and ({"EZM", "EPM"} & recs):
            uids.append(uid)
    uids = sorted(uids)
    if not uids:
        print("F9 skipped: no C1/C2 mouse with sal+psi BL1 and EZM/EPM")
        return
    ncol_mice = 3
    nrow_mice = int(np.ceil(len(uids) / ncol_mice))
    fig = plt.figure(figsize=(11.5, 3.3 * nrow_mice))
    outer = fig.add_gridspec(nrow_mice, ncol_mice, hspace=0.55, wspace=0.35,
                             left=0.04, right=0.98, top=0.93, bottom=0.04)
    corners = [("sal", "BL1"), ("psi", "BL1"), ("sal", "EZM"), ("psi", "EZM")]
    for i, uid in enumerate(uids):
        r, c = divmod(i, ncol_mice)
        inner = outer[r, c].subgridspec(2, 2, wspace=0.15, hspace=0.35)
        g = sub[sub.subject_uid == uid]
        mouse = str(g.mouse.iloc[0])
        coh = str(g.cohort.iloc[0])
        for k, (drug, rec) in enumerate(corners):
            ax = fig.add_subplot(inner[k // 2, k % 2])
            recs = (rec,) if rec == "BL1" else ("EZM", "EPM")
            hit = g[(g.drug == drug) & (g.rectype.isin(recs))]
            row = None if hit.empty else hit.iloc[0]
            vals = triangle_edge_vals(row, suffix="_winmean") if row is not None else triangle_edge_vals(None)
            head = f"{coh} {mouse}\n" if k == 0 else ""
            paint_wpli_triangle(ax, vals, title=f"{head}{drug} {rec}", fontsize=6)
    fig.suptitle(_t("F9 — Same mouse, two weeks: mean β wPLI (BL1 vs maze)"),
                 fontweight="bold", fontsize=12)
    fig.savefig(out / "F9_wpli_triangles.pdf")
    plt.close(fig)


# ----------------------------------------------------------------- F10
def fig10_delta_slopegraphs(feat: pd.DataFrame, out: Path) -> None:
    """C1/C2: Δ(EZM−BL1) for three β wPLI edges (and burst rate). Exploratory."""
    metrics = [
        ("burst_rate_per_min", "burst rate / min"),
        ("BLA-vHPC_wpli_beta_winmean", "BLA–vHPC β wPLI"),
        ("BLA-mPFC_wpli_beta_winmean", "BLA–mPFC β wPLI"),
        ("vHPC-mPFC_wpli_beta_winmean", "vHPC–mPFC β wPLI"),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(11.2, 3.6))
    any_ok = False
    for ax, (metric, ylab) in zip(axes, metrics):
        d = _ezm_minus_bl1(feat, metric)
        if d.empty:
            ax.set_visible(False)
            continue
        piv = d.pivot_table(index=["cohort", "mouse"], columns="drug", values="delta")
        if not {"sal", "psi"}.issubset(piv.columns):
            ax.set_visible(False)
            continue
        piv = piv.dropna(subset=["sal", "psi"], how="any")
        if piv.empty:
            ax.set_visible(False)
            continue
        any_ok = True
        for (c, _m), r in piv.iterrows():
            ax.plot([0, 1], [r["sal"], r["psi"]], "-o", ms=5, lw=1.2, alpha=.75,
                    color="tab:blue" if c == "C1" else "tab:orange")
        ax.hlines([piv["sal"].mean(), piv["psi"].mean()], [-.15, .85], [.15, 1.15],
                  color="k", lw=2.2)
        ax.axhline(0, color="0.7", lw=0.8, ls="--")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["saline\nΔ", "psi\nΔ"])
        ax.set_xlim(-.35, 1.35)
        ax.set_ylabel(f"Δ {ylab}")
        ax.set_title(f"n={len(piv)}", fontsize=9)
    if not any_ok:
        plt.close(fig)
        print("F10 skipped: need winmean/burst Δ for C1/C2")
        return
    fig.suptitle(_t("F10 — Exploratory: EZM − BL1, then psi vs saline (C1/C2)"),
                 fontweight="bold")
    fig.tight_layout()
    fig.savefig(out / "F10_delta_slopegraphs.pdf")
    plt.close(fig)


# -----------------------------------------------------------------
def run(*, derived: Path, out: Path, qc_path: Path | None = None,
        exclude: bool = True) -> None:
    global TITLE_SUFFIX
    TITLE_SUFFIX = " (dead channels excluded)" if exclude else ""
    out.mkdir(parents=True, exist_ok=True)

    qc_p = Path(qc_path) if qc_path is not None else derived / "qc.csv"
    ft_p = derived / "features_session.csv"
    nm_p = derived / "features_normalized.csv"
    dyn_p = derived / "features_dynamic.csv"

    qc = pd.read_csv(qc_p) if qc_p.exists() else None
    feat = pd.read_csv(ft_p) if ft_p.exists() else None
    norm = pd.read_csv(nm_p) if nm_p.exists() else None
    dyn = pd.read_csv(dyn_p) if dyn_p.exists() else None
    windows = _load_windows(derived)
    audit = pd.DataFrame()

    if dyn is not None and feat is not None:
        extra = [c for c in dyn.columns if c not in feat.columns]
        if extra:
            feat = feat.merge(dyn[["stem", *extra]], on="stem", how="left")

    if exclude:
        if qc is None:
            raise SystemExit(f"--exclude requires a QC table: {qc_p} not found")
        bad = find_bad_channels(qc)
        bmap = bad_channel_map(bad)
        if feat is not None:
            feat, audit = apply_exclusions(feat, bmap)
        if norm is not None:
            norm, _ = apply_exclusions(norm, bmap)
        if feat is None:
            audit = bad.merge(
                qc[["stem", "cohort", "group", "drug", "rectype"]].drop_duplicates("stem"),
                on="stem", how="left")

    if qc is not None:
        fig0_qc(qc, out); print("F0 ok")
        if exclude:
            fig0g_exclusions(audit, qc, out); print("F0g ok")
    if norm is not None:
        fig3_band_heatmap(norm, out); print("F3 ok")
    if feat is not None:
        fig4_bursts(feat, out); print("F4 ok")
        fig5_slopegraph(feat, out); print("F5 ok")
        fig6_phase_polar(feat, out); print("F6 ok")
        fig7_wpli_trace(windows, feat, out); print("F7 ok")
        fig8_wpli_var_slopegraph(feat, out); print("F8 ok")
        fig9_wpli_triangles(feat, out); print("F9 ok")
        fig10_delta_slopegraphs(feat, out); print("F10 ok")

    print(f"\nFigures written to {out}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--derived", default=Path("../derived"), type=Path)
    ap.add_argument("--out", default=None, type=Path,
                    help="default: ../figures_clean with exclusions, else ../figures")
    ap.add_argument("--qc", default=None, type=Path,
                    help="QC table (default: <derived>/qc.csv)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--exclude", dest="exclude", action="store_true",
                   help="NaN dead/high-kurtosis channels (default)")
    g.add_argument("--no-exclude", dest="exclude", action="store_false")
    ap.set_defaults(exclude=True)
    args = ap.parse_args()

    out = args.out
    if out is None:
        out = Path("../figures_clean") if args.exclude else Path("../figures")
    qc = args.qc if args.qc is not None else args.derived / "qc.csv"
    run(derived=args.derived, out=out, qc_path=qc, exclude=args.exclude)


if __name__ == "__main__":
    main()
