# The Benchmark of Stellarator Simulations (BoSS)

[Installation](installation.md){.sd-btn .sd-btn-primary .sd-shadow-sm}
[Download Data](download.md){.sd-btn .sd-btn-primary .sd-shadow-sm}
[Data Explorer](data-explorer.md){.sd-btn .sd-btn-primary .sd-shadow-sm}

The Benchmark of Stellarator Simulations (BoSS) is a database of stellarator
configurations paired with physics simulations. The database contains roughly
3TB of [Ideal MHD](data/ideal-mhd.md) and [collisionless guiding center](data/fast-ion.md)
simulations for roughly 180,000 stellarators. The database keeps growing. New
configurations are added over time, and results from other kinds of simulation
will be added as new sections. This database can be used to accelerate machine
learning methods for fusion applications, or improve our understanding of
fundamental physics.

<figure class="boss-hero-video">
  <video autoplay muted loop playsinline preload="metadata"
         poster="_static/video/fast_ion_losses_poster.webp"
         aria-label="A burst of 400 alpha particles orbiting inside a stellarator; the ones that are lost leave orange marks where they strike the plasma boundary, and a counter beside it tracks the losses over time.">
    <source src="_static/video/fast_ion_losses.mp4" type="video/mp4">
  </video>
  <figcaption>A burst of 400 alpha particles followed along their guiding-center
  orbits in one stellarator configuration. Orange marks show where lost
  particles strike the plasma boundary.</figcaption>
</figure>
<script>
  // no autoplay for readers who ask for reduced motion
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const v = document.querySelector(".boss-hero-video video");
    v.removeAttribute("autoplay"); v.pause(); v.controls = true;
  }
</script>

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
