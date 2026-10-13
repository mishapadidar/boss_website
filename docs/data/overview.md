# Database overview

The BoSS holds **179,049 stellarator configurations** gathered from a dozen
sources, from curated databases of optimized devices to randomly generated
shapes. Every configuration goes through the same pipeline: an
[ideal MHD](ideal-mhd.md) equilibrium computed with VMEC, followed by
[fast-ion confinement](fast-ion.md) simulations of 15,000 alpha particles.

<!-- Numbers on this page are printed by scripts/make_overview_figures.py.
     TODO: rerun it once the final confinement and trajectory files are generated;
     the numbers and histograms below are from the previous processing. -->

::::{grid} 2 2 4 4
:gutter: 3

:::{grid-item}
:class: boss-stat
<span class="boss-stat-value">179,049</span>
<span class="boss-stat-label">configurations</span>
:::

:::{grid-item}
:class: boss-stat
<span class="boss-stat-value">2.7 billion</span>
<span class="boss-stat-label">alpha particles traced</span>
:::

:::{grid-item}
:class: boss-stat
<span class="boss-stat-value">134 million</span>
<span class="boss-stat-label">full particle orbits</span>
:::

:::{grid-item}
:class: boss-stat
<span class="boss-stat-value">3.2 TB</span>
<span class="boss-stat-label">of HDF5 files</span>
:::
::::

## Sources

The field `source_dataset` records where each configuration came from. The
configurations come from about 97,000 distinct source devices
(`source_id`). A device can appear more than once, with different
pressure and current profiles, and scaled to a different machine size and
field strength.

```{table}
:class: boss-sources
:widths: 26 58 16
:width: 100%

| Source (`source_dataset`) | Description | Configurations |
| --- | --- | ---: |
| `quasr` | Quasi-axisymmetric and quasi-helically symmetric stellarators from [QUASR](https://quasr.flatironinstitute.org/) ([Giuliani et al.](https://arxiv.org/abs/2409.04826)). | 70,764 |
| `constellaration` | Quasi-isodynamic-like boundaries from the [ConStellaration](https://arxiv.org/abs/2506.19583) dataset (Cadena et al., 2025). | 66,135 |
| `model_improvement_2026` | Random boundaries on which a loss-fraction surrogate model is likely to be wrong, added to improve surrogate models. Generated for the BoSS. | 13,922 |
| `random_ellipse` | Unoptimized rotating ellipses with random elongation, aspect ratio and axis torsion. Generated for the BoSS. | 7,932 |
| `model_improvement_bo_2026` | Boundaries chosen by Bayesian optimization to improve surrogate models. Generated for the BoSS. | 7,635 |
| `random_ellipse_perturbed` | Rotating ellipses with random perturbations in their higher Fourier modes. Generated for the BoSS. | 6,872 |
| `fast_ion_opt_2026` | Boundaries optimized for alpha-particle confinement using a surrogate model. Generated for the BoSS. | 5,530 |
| `omnigenity` | Omnigenous equilibria computed with DESC, from the omnigenity database of [Gaur et al.](https://archive.aps.org/dpp/2023/ap01/33) (2023). | 185 |
| `kappel_2024` | Stellarator and tokamak configurations collected by [Kappel et al.](https://arxiv.org/abs/2309.11342) (2024). | 64 |
| Others | `bindel_2023`: configurations optimized for fast-ion confinement by [Bindel et al.](https://arxiv.org/abs/2302.11369) (2023). `bindel_2023_perturbed`, `quasr_perturbed`: perturbed copies of a few devices. | 10 |
```

## Distributions

```{image} ../_static/overview/distributions-light.svg
:class: only-light
:alt: Histograms of the number of field periods, aspect ratio, plasma beta and alpha-particle loss fraction over all configurations.
```

```{image} ../_static/overview/distributions-dark.svg
:class: only-dark
:alt: Histograms of the number of field periods, aspect ratio, plasma beta and alpha-particle loss fraction over all configurations.
```

The histograms leave out 16 configurations with aspect ratio above 13 and one
with $n_\text{fp} = 12$. Two thirds of the configurations are vacuum equilibria ($\beta = 0$). The rest
have finite pressure, with $\langle\beta\rangle$ up to about 6%. Each
configuration is scaled to a randomly chosen machine size (major radius
1–33 m) and field strength (volume-averaged $B$ of 4–11 T).

## Files

The data comes in two kinds of HDF5 file. Both kinds hold every
[ideal MHD](ideal-mhd.md) field of their configurations; they differ in the
[fast-ion data](fast-ion.md) they carry.

| | Confinement files | Trajectory files |
| --- | --- | --- |
| **Fast-ion data** | Start and end state of all 15,000 particles | Full orbits of 6,000 particles |
| **Configurations per file** | up to 3,000 | up to 40 |
| **Train split** | 52 files, 279 GB, 154,128 configurations | 479 files, 2.46 TB, 19,123 configurations |
| **Test split** | 9 files, 45 GB, 24,921 configurations | 80 files, 411 GB, 3,184 configurations |

The confinement files (325 GB in all) are enough to compute loss fractions
and heat fluxes. The trajectory files (2.9 TB) hold 134 million orbits for
22,307 of the configurations, for work on particle motion itself. See
[Download Data](../download.md) to get them.

## Train/test split

The file names give the split. The test split holds 24,921 configurations
(14%), drawn at random across sources. All configurations that come from the
same source device are in the same split, so a model is never tested on a
reshaped or rescaled copy of a device it was trained on.
