---
title: Overview
hide:
  - toc
---

<div class="boss-hero" markdown>

# BoSS

<p class="subtitle">Benchmark of Stellarator Simulations</p>

<p class="tagline">
A growing database of stellarator configurations and the physics simulations
run on them, built for machine learning and fusion design. The first release
pairs every configuration with fast-ion (alpha-particle) confinement
simulations.
</p>

[Download the data](download.md){ .md-button .md-button--primary }
[Tutorials](tutorials/index.md){ .md-button }
[Data documentation](data/index.md){ .md-button }
[Open the Navigator](navigator.md){ .md-button }

</div>

<div class="boss-stats">
  <div class="stat"><span class="value">179,049</span><span class="label">stellarator configurations</span></div>
  <div class="stat"><span class="value">15,000</span><span class="label">alpha particles traced per configuration</span></div>
  <div class="stat"><span class="value">154k / 25k</span><span class="label">train / test split</span></div>
  <div class="stat"><span class="value">3.2 TB</span><span class="label">confinement data and full trajectories</span></div>
</div>

## What is BoSS?

Predicting how a stellarator will perform takes expensive simulations, and
that cost is what limits both design studies and data-driven methods.
BoSS collects stellarator configurations from many sources, runs each one
through the same pipeline, and publishes both the configurations and their
simulation results in a consistent, ML-ready format.

The database keeps growing. New configurations are added over time, and so
are results from **other kinds of simulation**. Fast-ion confinement is the
first.

With BoSS you can:

- train **surrogate models** that predict simulation outcomes, such as alpha-particle losses, from geometry or equilibrium quantities;
- study how confinement correlates with **quasi-symmetry, quasi-isodynamicity** and other proxies across very different families of devices;
- benchmark **generative and inverse-design** methods on physically meaningful targets.

## What's in the database

<div class="grid cards" markdown>

-   :material-shape-outline: **Configurations**

    ---

    For each configuration: the boundary surface, magnetic axis, \(|B|\) on a
    3-D grid in VMEC and Boozer coordinates, radial profiles (\(\iota\),
    pressure, \(\epsilon_\text{eff}\), quasi-symmetry and QI errors, Mercier
    stability, …), and scalar figures of merit.

    [:octicons-arrow-right-24: Configuration fields](data/configurations.md)

-   :material-atom-variant: **Fast-ion confinement**

    ---

    15,000 collisionless alpha-particle guiding-center orbits per
    configuration, traced with CATAPULT (FIRM3D) at a randomly chosen reactor
    scale. Initial and final states, confinement times, and the full orbits.

    [:octicons-arrow-right-24: Fast-ion confinement](data/fast-ion.md)

-   :material-plus-circle-outline: **More simulations to come**

    ---

    Results from other codes will be added as new sections of the database,
    keyed by the same configuration `uuid`.

</div>

## Quick start

```python
import h5py

with h5py.File("confinement_data_test_split_00000.hdf5", "r") as f:
    aspect = f["aspect_ratio"][:]                  # one value per configuration
    ct, t_max = f["confinement_time"][:10], f["t_max"][:10]
    loss_fraction = (ct < t_max[:, None]).mean(axis=1)
    print(aspect[:10], loss_fraction)
```

See [Download](download.md) for the files, and [Tutorials](tutorials/index.md)
for more.

## Contact

Questions, bug reports, or configurations you'd like to contribute:
**Misha Padidar**, Flatiron Institute
([mpadidar@flatironinstitute.org](mailto:mpadidar@flatironinstitute.org)).

The data is released under the
[Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0).
