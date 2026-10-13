# The BoSS: Benchmark of Stellarator Simulations

**The BoSS** is a growing database of stellarator configurations paired with
physics simulations.

<figure class="boss-hero-video">
  <video autoplay muted loop playsinline preload="metadata"
         poster="_static/video/fast_ion_losses_poster.webp"
         aria-label="Alpha particles orbiting inside a stellarator; the ones that are lost leave orange marks where they strike the plasma boundary.">
    <source src="_static/video/fast_ion_losses.mp4" type="video/mp4">
  </video>
  <figcaption>Alpha particles followed along their guiding-center orbits in one
  configuration of the BoSS. Orange marks show where lost particles strike the
  plasma boundary.</figcaption>
</figure>
<script>
  // no autoplay for readers who ask for reduced motion
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const v = document.querySelector(".boss-hero-video video");
    v.removeAttribute("autoplay"); v.pause(); v.controls = true;
  }
</script>

[Installation](installation.md){.sd-btn .sd-btn-primary .sd-shadow-sm}
[Download Data](download.md){.sd-btn .sd-btn-primary .sd-shadow-sm}
[Data Explorer](data-explorer.md){.sd-btn .sd-btn-primary .sd-shadow-sm}

## What is the BoSS?

Predicting how a stellarator will perform takes expensive simulations, and
that cost is what limits both design studies and data-driven methods.
The BoSS collects stellarator configurations from many sources, runs each one
through the same pipeline, and publishes both the configurations and their
simulation results in a consistent, ML-ready format.

The database currently holds data from [Ideal MHD](data/ideal-mhd.md)
simulations with VMEC, and [collisionless guiding center](data/fast-ion.md)
simulations from CATAPULT/FIRM3D. The database keeps growing. New configurations are added over time, and
results from **other kinds of simulation** will be added as new sections.

With the BoSS you can:

- train **surrogate models** that predict simulation outcomes, such as alpha-particle losses, from geometry or equilibrium quantities;
- study how confinement correlates with **quasi-symmetry, quasi-isodynamicity** and other proxies across very different families of devices;
- benchmark **generative and inverse-design** methods on physically meaningful targets.

## Installation

The BoSS comes with a Python package for working with the data: reading the
files, computing derived quantities such as loss fractions and heat fluxes,
and evaluating models with the benchmark's metrics. Install it with

```bash
pip install boss-bench
```

See [Installation](installation.md) to install from source.

## Citing the BoSS

If you find this project useful for your research, please consider citing:

- A. Author, B. Author, and C. Author. *The BoSS: a benchmark of stellarator
  simulations.* 2026. [doi:XX.XXXXX/XXXXX](https://doi.org/XX.XXXXX/XXXXX),
  [arXiv:XXXX.XXXXX](https://arxiv.org/abs/XXXX.XXXXX).

The corresponding BibTeX entry is given hereunder.

```bibtex
@unpublished{boss,
  author       = {Author, A. and Author, B. and Author, C.},
  title        = {The {BoSS}: a benchmark of stellarator simulations},
  eprint       = {XXXX.XXXXX},
  eprinttype   = {arxiv},
  eprintclass  = {physics.plasm-ph},
  year         = 2026,
  doi          = {XX.XXXXX/XXXXX},
}
```

The data is released under the
[Creative Commons Attribution 4.0 International (CC BY 4.0) license](https://creativecommons.org/licenses/by/4.0/).

## Contact

For questions regarding this project, please contact
[Misha Padidar](https://mishapadidar.com/).

## Acknowledgements

We thank the Flatiron Institute’s Scientific Computing Core and the Simons Foundation.

<!-- The toctrees below are hidden on this page; they define the left sidebar. -->

```{toctree}
:caption: Get Started
:hidden:

installation
download
data-explorer
```

```{toctree}
:caption: Tutorials
:hidden:

tutorials/exploring
tutorials/loading-trajectories
tutorials/surrogate
```

```{toctree}
:caption: Data Documentation
:hidden:

data/overview
data/ideal-mhd
data/fast-ion
```

```{toctree}
:caption: Package documentation
:hidden:
:glob:

package
api/*
```
