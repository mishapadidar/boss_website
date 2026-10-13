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

## Loading the data

The package works on local files, so [download the data](download.md) first and put
the files in one folder, for example `BoSS/`; any layout inside it works.
{func}`~boss_bench.data.list_files` lists the files of one kind and split under that
folder, {func}`~boss_bench.data.load_record` reads the fields of one configuration of
an open file, by its row or its `uuid`, and {func}`~boss_bench.data.load` reads chosen
fields of every configuration in a list of files.

```python
import h5py

files = bb.list_files("BoSS", "confinement", "test")
with h5py.File(files[0], "r") as f:
    record = bb.load_record(f, 0)                   # every field of configuration 0
data = bb.load(files, ["nfp", "aspect_ratio"])      # fields stacked over files
```

Row `i` of every per-configuration field belongs to configuration `i`. The fields are
described in [Ideal MHD](data/ideal-mhd.md) and
[Fast-ion confinement](data/fast-ion.md).

## Particle losses

A particle is lost if its confinement time is shorter than the simulation time,
$t_\text{loss} < t_\text{max}$ ({func}`~boss_bench.confinement.is_lost`). The loss
metrics, such as the loss fraction and the (normalized) energy loss, are computed over
the particles born on one surface $s_0$:

```python
ct, t_max, s_init = record["confinement_time"], record["t_max"], record["s_init"]
bb.loss_fraction(ct, t_max, s_init, s0=0.1)           # fraction lost
bb.energy_loss(ct, t_max, s_init, s0=0.1)             # mean of 3.5 MeV * exp(-2 t_loss / t_max)
bb.normalized_energy_loss(ct, t_max, s_init, s0=0.1)  # the same, rescaled to [0, 1]
```

## Benchmarks

Each benchmark takes a model's predictions and returns the paper's metrics.
Predictions may use any field of a configuration except the outcomes of the particle
tracing: `confinement_time`, `s_end`, `theta_end`, `zeta_end` and `vpar_end`. The
benchmarks score every test sample, and the metrics report how many samples were
scored.

### Surrogate models

Predict a quantity of each configuration of the test split, such as
{func}`~boss_bench.confinement.loss_fraction` or
{func}`~boss_bench.confinement.normalized_energy_loss` at $s_0 = 0.1$, from its shape
and profiles. [Fitting a surrogate model](tutorials/surrogate.md) fits a first one.

### Heat flux

A sample is one test configuration and one birth surface $s_0$. For each sample,
predict the loss fraction, and the strike points of the lost particles on the plasma
boundary: their Boozer angles $\zeta$, $\theta$ and their energies.
{func}`~boss_bench.heat_flux.lost_particles` returns the true strike points of a
sample, and {func}`~boss_bench.heat_flux.binned_heat_flux` turns strike points into
the heat flux on the boundary.

```python
paths = bb.list_files("BoSS", "confinement", "test")
predictions = {}
for path in paths:
    with h5py.File(path, "r") as f:
        for i in range(len(f["uuid"])):
            record = bb.load_record(f, i, ["uuid", "boundary_xyz", "iota", "nfp"])  # what your model needs
            for s0 in (0.1, 0.25, 0.5):
                predictions[record["uuid"], s0] = my_model(record, s0)  # (zeta, theta, energy, loss_fraction)
bb.heat_flux_metrics(paths, predictions)
```

{func}`~boss_bench.heat_flux.heat_flux_metrics` reports the median energy distance of
the strike points ({func}`~boss_bench.heat_flux.energy_distance`, over samples with at
least 10 lost particles), the median and mean heat-flux error on 16 × 16 and 32 × 32
grids ({func}`~boss_bench.heat_flux.heat_flux_error`), and the median and mean
absolute error of the loss fraction.

### Trajectories

For each orbit in the test files, predict from its first sample the state at lead
times $\tau = 10$, $100$ and $999\,\mu$s, and the time the particle is lost (`NaN` if
it is not lost within 1 ms). States are in the embedded form of
{func}`~boss_bench.trajectory.embed_state`,

$$
z = \left(\sqrt{s}\cos\theta,\ \sqrt{s}\sin\theta,\ \cos\varphi,\ \sin\varphi,\ v_\parallel / v_\alpha\right),
$$

and {func}`~boss_bench.trajectory.read_trajectories` reads the orbits of a
configuration in this form. {func}`~boss_bench.trajectory.load_trajectory` reads a
single orbit as it is stored. {func}`~boss_bench.trajectory.to_xyz` converts points in Boozer
coordinates, such as the samples of an orbit, to Cartesian positions.

```python
paths = bb.list_files("BoSS", "trajectory", "test")
predictions = {}  # uuid -> (z of shape (n_orbits, 3, 5), t_loss of shape (n_orbits,))
bb.trajectory_metrics(paths, predictions)
```

A predicted particle is lost at the first time its predicted $s \ge 0.98$, and its
predicted state is held at the loss state afterwards. Orbits lost before their first
sample are not scored. {func}`~boss_bench.trajectory.trajectory_metrics` reports the
normalized RMSE of the states at each lead time
({func}`~boss_bench.trajectory.nrmse`), with its breakdown by channel group, the mean absolute error of the fraction lost
within 1 ms ({func}`~boss_bench.trajectory.loss_fraction_mae`), and the
Wasserstein-1 distance of the confinement times
({func}`~boss_bench.trajectory.confinement_time_w1`).
[Loading trajectory data](tutorials/loading-trajectories.md) shows how the orbits are
stored.

### Inverse design

Evaluate each design with VMEC and particle tracing at ARIES-CS scale, then score the
set with {func}`~boss_bench.design.design_metrics`:

```python
bb.design_metrics(loss_fraction, mirror_ratio, mirror_target, aspect_ratio, aspect_target)
```

It reports the percentage of designs with loss fraction (of the particles born on
$s_0 = 0.1$) at most 10% and 15%, with mirror ratio at most the target and 1.1 times
the target, and the median relative error of the aspect ratio.

## Plotting

The heat-flux plots take optional predictions, a dict that maps each birth surface
$s_0$ to a predicted `(zeta, theta, energy, loss_fraction)`, and draw them next to the
truth.

```python
bb.plot_device(record)                          # plasma boundary colored by |B|
bb.plot_modB_boozer(record, s=0.5)              # |B| on a flux surface in Boozer coordinates
bb.plot_loss_fraction_curves(record)            # fraction lost vs time, per birth surface
bb.plot_strike_points(record, predictions)      # strike points and density of lost particles, per s0
bb.plot_heat_flux(record, predictions)          # heat flux over one field period, per s0
bb.plot_rollouts(z_true, z_pred)                # trajectories vs lead time, per channel
```

[Exploring a stellarator](tutorials/exploring.md) shows most of them.

## Errors

Every function raises a `ValueError` if its input, or a model's prediction, contains
NaN or inf where a number is expected. A NaN loss time is allowed: it means the
particle is not lost.
