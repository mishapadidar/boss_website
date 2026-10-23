"""Figures and numbers for docs/data/overview.md.

Reads the per-configuration table written by collect_stats.py (run on the cluster)
and writes docs/_static/overview/distributions-{light,dark}.svg. It also prints the
numbers quoted on the overview page, so they can be updated when the database grows.

    python scripts/make_overview_figures.py boss_site_stats.npz boss_site_files.json
"""
import json
import pathlib
import sys

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = pathlib.Path(__file__).resolve().parents[1] / "docs" / "_static" / "overview"
QS_BINS = np.logspace(-5, 0, 41)      # the error spans five decades, so log bins on a log axis
IOTA_BINS = np.arange(-1.5, 2.001, 0.1)
AR_BINS = np.arange(1.5, 13.01, 0.5)

# One series per panel, in slot 1 of the reference palette; ink and grid per mode.
THEMES = {
    "light": {"bar": "#2a78d6", "ink": "#0b0b0b", "muted": "#52514e", "grid": "#e4e3df"},
    "dark": {"bar": "#3987e5", "ink": "#f0efec", "muted": "#c3c2b7", "grid": "#3a3a37"},
}


def load(stats_path):
    d = np.load(stats_path)
    return {k: d[k] for k in d.files}


def print_numbers(t, files):
    n = len(t["uuid"])
    print(f"configurations: {n:,}  (train {np.sum(t['split'] == 'train'):,}, "
          f"test {np.sum(t['split'] == 'test'):,})")
    print(f"alpha particles traced: {n * 15000:,}")
    for kind in ("confinement", "trajectory"):
        for split in ("train", "test"):
            fs = [f for f in files if f["kind"] == kind and f["split"] == split]
            line = (f"{kind:11s} {split:5s}: {len(fs):4d} files, "
                    f"{sum(f['bytes'] for f in fs) / 1e9:8.1f} GB, "
                    f"{sum(f['n_configs'] for f in fs):7,d} configurations")
            if kind == "trajectory":
                line += f", {sum(f['n_orbits'] for f in fs):,} orbits"
            print(line)
    print(f"total size: {sum(f['bytes'] for f in files) / 1e12:.2f} TB")
    print(f"vacuum: {np.mean(t['enforce_vacuum']):.0%}")
    print("left out of the histograms:",
          f"aspect ratio > {AR_BINS[-1]:g}: {np.sum(t['aspect_ratio'] > AR_BINS[-1])},",
          f"mean iota outside [{IOTA_BINS[0]:g}, {IOTA_BINS[-1]:g}]: "
          f"{np.sum((t['iota_mean'] < IOTA_BINS[0]) | (t['iota_mean'] > IOTA_BINS[-1]))},",
          f"QS error > {QS_BINS[-1]:g}: {np.sum(t['sqrt_boozer_qs_error_mean'] > QS_BINS[-1])},",
          f"nfp > 6: {np.sum(t['nfp'] > 6)}")
    print(f"non-vacuum beta: up to {100 * t['plasma_beta'].max():.2f}%, "
          f"above 1%: {np.mean(t['plasma_beta'][~t['enforce_vacuum'].astype(bool)] > 0.01):.0%} of non-vacuum")
    print(f"distinct source devices: {len(set(zip(t['source_dataset'], t['source_id']))):,}")
    print("\nconfigurations per source (source_dataset)")
    for src in sorted(set(t["source_dataset"]), key=lambda s: -np.sum(t["source_dataset"] == s)):
        print(f"  {src:26s} {np.sum(t['source_dataset'] == src):7,d}")


def panel(ax, theme, title, xlabel):
    ax.set_title(title, loc="left", color=theme["ink"], fontsize=12, fontweight="bold", pad=8)
    ax.set_xlabel(xlabel, color=theme["muted"], fontsize=10.5)
    ax.tick_params(colors=theme["muted"], labelsize=10, length=0)
    ax.grid(axis="y", color=theme["grid"], linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(theme["muted"])
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f"{v / 1000:.0f}k" if v else "0"))


def hist(ax, theme, x, bins):
    counts, edges = np.histogram(x, bins=bins)
    ax.bar(edges[:-1], counts, width=np.diff(edges) * 0.86, align="edge",
           color=theme["bar"], linewidth=0)


def figure(t, mode):
    theme = THEMES[mode]
    plt.rcParams["svg.fonttype"] = "none"          # text stays text: the page font renders it
    plt.rcParams["font.family"] = "sans-serif"
    fig, axes = plt.subplots(2, 3, figsize=(8.6, 5.6))
    axes = axes.ravel()
    fig.patch.set_alpha(0)

    ax = axes[0]
    hist(ax, theme, t["loss_fraction_s_0_25"], np.linspace(0, 1, 26))
    panel(ax, theme, "Loss fraction", "born on $s = 0.25$, lost by 0.1 s")

    ax = axes[1]
    hist(ax, theme, t["sqrt_boozer_qs_error_mean"], QS_BINS)
    panel(ax, theme, "Quasi-symmetry error", r"$\sqrt{f_\mathrm{QS}}$, mean over $s$")
    ax.set_xscale("log")
    ax.set_xticks([1e-4, 1e-2, 1])

    ax = axes[2]
    hist(ax, theme, t["aspect_ratio"], AR_BINS)
    panel(ax, theme, "Aspect ratio", r"$A = R_0 / a$")

    ax = axes[3]
    hist(ax, theme, t["iota_mean"], IOTA_BINS)
    panel(ax, theme, "Rotational transform", r"$\iota$, mean over $s$")

    ax = axes[4]
    beta = 100 * t["plasma_beta"][~t["enforce_vacuum"].astype(bool)]
    hist(ax, theme, beta, np.arange(0, 6.01, 0.25))
    panel(ax, theme, "Plasma beta (non-vacuum)", r"$\langle\beta\rangle$ [%]")

    ax = axes[5]
    nfp, counts = np.unique(t["nfp"][t["nfp"] <= 6], return_counts=True)
    ax.bar(nfp, counts, width=0.72, color=theme["bar"], linewidth=0)
    ax.set_xticks(nfp)
    panel(ax, theme, "Field periods", r"$n_\mathrm{fp}$")

    for ax in axes:
        ax.patch.set_alpha(0)
    fig.supylabel("configurations", color=theme["muted"], fontsize=10.5, x=0.004)
    fig.tight_layout(w_pad=2.0, h_pad=2.0)
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"distributions-{mode}.svg", transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    t = load(sys.argv[1])
    print_numbers(t, json.load(open(sys.argv[2])))
    for mode in THEMES:
        figure(t, mode)
    print("wrote", OUT)
