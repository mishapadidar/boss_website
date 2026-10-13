# Overview

`boss-bench` is the Python package of the BoSS. It loads the data and computes the
benchmark metrics exactly as they are defined in the paper. It depends only on NumPy,
SciPy, h5py and Matplotlib, and needs Python 3.9 or newer. Install it with

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
The most useful functions are:

- {mod}`boss_bench.data`: find and read the data files, with
  {func}`~boss_bench.data.list_files`, {func}`~boss_bench.data.load_record` (one
  configuration) and {func}`~boss_bench.data.load` (chosen fields of many).
- {mod}`boss_bench.confinement`: alpha-particle losses of the particles born on one
  surface, with {func}`~boss_bench.confinement.loss_fraction`,
  {func}`~boss_bench.confinement.energy_loss` and
  {func}`~boss_bench.confinement.normalized_energy_loss`.
- {mod}`boss_bench.heat_flux`: where lost particles strike the plasma boundary, with
  {func}`~boss_bench.heat_flux.lost_particles` and
  {func}`~boss_bench.heat_flux.binned_heat_flux`, and the heat-flux benchmark,
  {func}`~boss_bench.heat_flux.heat_flux_metrics`.
- {mod}`boss_bench.trajectory`: orbits, with
  {func}`~boss_bench.trajectory.load_trajectory` (one orbit),
  {func}`~boss_bench.trajectory.read_trajectories` (all orbits of a configuration) and
  {func}`~boss_bench.trajectory.to_xyz` (Cartesian positions), and the trajectory
  benchmark, {func}`~boss_bench.trajectory.trajectory_metrics`.
- {mod}`boss_bench.design`: the inverse-design benchmark,
  {func}`~boss_bench.design.design_metrics`.
- {mod}`boss_bench.plotting`: plots of a configuration
  ({func}`~boss_bench.plotting.plot_device`,
  {func}`~boss_bench.plotting.plot_modB_boozer`), its losses
  ({func}`~boss_bench.plotting.plot_loss_fraction_curves`,
  {func}`~boss_bench.plotting.plot_heat_flux`,
  {func}`~boss_bench.plotting.plot_strike_points`) and its orbits
  ({func}`~boss_bench.plotting.plot_rollouts`).

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
