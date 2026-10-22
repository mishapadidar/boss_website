# Overview

`boss-bench` is the Python package of the BoSS. It loads the data and computes the
benchmark metrics exactly as they are defined in the paper. It depends only on NumPy,
SciPy, h5py and Matplotlib, and needs Python 3.9 or newer. The pretrained models also
need PyTorch. Install it with

```bash
pip install boss-bench
```

or from source:

```bash
git clone https://github.com/mishapadidar/boss_bench.git
cd boss_bench
pip install .
```

Then import it as

```python
import boss_bench as bb
```

The package works on local files, so [download the data](download.md) first.

## What's in the package

Each module has its own page, with every function and the formula of every metric.

{mod}`boss_bench.data`
: Finds the downloaded files and reads them: one configuration at a time with
  {func}`~boss_bench.data.load_record`, or chosen fields of many configurations at
  once.

{mod}`boss_bench.confinement`
: Computes the loss metrics of the particles born on one surface: the loss fraction,
  the energy loss and its normalized form, and the mean confinement time, e.g.
  {func}`~boss_bench.confinement.loss_fraction`.

{mod}`boss_bench.heat_flux`
: Finds where lost particles strike the plasma boundary and turns their energy into a
  heat flux on the boundary. It also scores predictions for the heat-flux benchmark,
  with {func}`~boss_bench.heat_flux.heat_flux_metrics`.

{mod}`boss_bench.trajectory`
: Provides convenience functions to load trajectory data for one particle or one
  device, and to convert orbits to Cartesian coordinates. It also computes the
  prediction-error metrics of the trajectory benchmark, with
  {func}`~boss_bench.trajectory.trajectory_metrics`.

{mod}`boss_bench.design`
: Scores generated designs for the inverse-design benchmark, with
  {func}`~boss_bench.design.design_metrics`.

{mod}`boss_bench.plotting`
: Plots a configuration, its particle losses and heat flux, and its orbits, alone or
  next to a model's predictions.

{mod}`boss_bench.models`
: Runs the pretrained models in PyTorch: the loss-fraction surrogate
  ({class}`~boss_bench.models.loss_fraction.LossFractionModel`), the heat-flux model
  ({class}`~boss_bench.models.heat_flux.HeatFluxModel`) and the inverse-design model
  ({class}`~boss_bench.models.inverse_design.InverseDesignModel`), downloaded from
  Hugging Face with {func}`~boss_bench.models.download`. It needs
  `pip install "boss-bench[models]"`; see [Download Models](download.md#download-models).

## Benchmarks

Each benchmark scores a model's predictions on the test split with the metrics of
the paper:

- **Surrogate models:** predict a quantity of each configuration, such as its
  {func}`~boss_bench.confinement.loss_fraction` or
  {func}`~boss_bench.confinement.normalized_energy_loss` at $s_0 = 0.1$.
- **Heat flux:** predict the loss fraction and the strike points of the lost
  particles, for each configuration and birth surface; scored by
  {func}`~boss_bench.heat_flux.heat_flux_metrics`.
- **Trajectories:** predict each orbit from its first sample; scored by
  {func}`~boss_bench.trajectory.trajectory_metrics`.
- **Inverse design:** generate designs and evaluate them with VMEC and particle
  tracing; scored by {func}`~boss_bench.design.design_metrics`.

## Tutorials

To see the package in use, work through the tutorials:

- [Exploring a stellarator](tutorials/exploring.md): load a configuration, plot it,
  and compute its losses and heat flux.
- [Loading trajectory data](tutorials/loading-trajectories.md): read and plot orbits,
  and draw rollouts.
- [Fitting a surrogate model](tutorials/surrogate.md): predict loss fractions with
  scikit-learn.
