# The BoSS: a benchmark of stellarator simulations

[Download Data](download.md){.sd-btn .sd-btn-primary .sd-shadow-sm}
[Data Explorer](data-explorer.md){.sd-btn .sd-btn-primary .sd-shadow-sm}

The Benchmark of Stellarator Simulations (BoSS) is a database of stellarator
configurations paired with physics simulations. It holds about 3 TB of data from
[ideal MHD](data/ideal-mhd.md) and [collisionless guiding-center](data/fast-ion.md)
simulations of roughly 180,000 stellarators. The database keeps growing: new
configurations are added over time, and results from other kinds of simulation
will be added as new sections. It can be used to develop machine-learning methods
for fusion applications, or to improve our understanding of the underlying
physics.

<figure class="boss-hero-video">
  <video autoplay muted loop playsinline preload="metadata"
         poster="_static/video/fast_ion_losses_poster.webp"
         aria-label="A burst of 400 alpha particles orbiting inside a stellarator; the ones that are lost leave orange marks where they strike the plasma boundary, and a counter beside it tracks the losses over time.">
    <source src="_static/video/fast_ion_losses.mp4" type="video/mp4">
  </video>
  <figcaption>A burst of 400 alpha particles followed along their guiding-center
  orbits in one stellarator configuration. Orange marks show where lost
  particles strike the plasma boundary. The panel on the right counts the
  particles lost so far: the loss fraction is the share of the 400 particles
  that have been lost, and the loss rate is the number of particles lost per
  millisecond at each moment.</figcaption>
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
and evaluating models with the benchmark's metrics. It needs Python 3.9 or
newer. Install it with:

```bash
pip install boss-bench
```

### From source

```bash
git clone https://github.com/mishapadidar/boss_bench.git
cd boss_bench
pip install .
```

See the [package documentation](package.md) for how to use it.

<!-- Restore once the paper is out.

## Citing the BoSS

If you find this project useful for your research, please consider citing:

- A. Author, B. Author, and C. Author. *The BoSS: a benchmark of stellarator
  simulations.* 2026. [doi:XX.XXXXX/XXXXX](https://doi.org/XX.XXXXX/XXXXX),
  [arXiv:XXXX.XXXXX](https://arxiv.org/abs/XXXX.XXXXX).

The BibTeX entry is below.

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

-->

## License

The data is released under the
[Creative Commons Attribution 4.0 International (CC BY 4.0) license](https://creativecommons.org/licenses/by/4.0/).
The `boss-bench` package is released under the
[Apache License 2.0](https://github.com/mishapadidar/boss_bench/blob/main/LICENSE).
Copyright 2026 The Simons Foundation.

## Contact

For questions regarding this project, please contact
[Misha Padidar](https://mishapadidar.com/).

## Acknowledgments

We thank the Flatiron Institute’s Scientific Computing Core and the Simons Foundation.

<!-- The toctrees below are hidden on this page; they define the left sidebar. -->

```{toctree}
:caption: Get Started
:hidden:

download
download-models
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
