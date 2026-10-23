# Designing stellarators with a generative model

This tutorial generates a stellarator boundary with the Diffusion baseline of the
paper's inverse-design task: a generative model that draws boundaries with the
properties we ask for.

Install the package with its models:

```bash
pip install "boss-bench[models]"
```

Now download and load the model using the convenience functions from `boss-bench`:

```python
from boss_bench import models
from boss_bench.models import InverseDesignModel

path = models.download("inverse_design", "BoSS-models/inverse_design")
model = InverseDesignModel.load(path)
```

## The conditions

The model is conditioned on properties the design should have, given by the names of
BoSS fields and in their units: the number of field periods `nfp`, the `loss_fraction`
of the alpha particles born on $s = 0.1$, the toroidal flux `toroidal_flux_edge`, the
`minor_radius`, the `aspect_ratio`, the minimum field strength `min_modB`, the
`mirror_ratio`, the `pressure` and `iota` profiles, and `vmec_ncurr`, which says
whether the equilibrium is computed with the $\iota$ (0) or the current profile (1).

Good designs come from realistic conditions with a low loss fraction. Download
`confinement_data_test_split_00000.hdf5` from the [Download Data](../download.md) page
into a folder, here `BoSS/`, and take the conditions of the first stellarator of the
test split that loses less than 10% of its alpha particles:

```python
import h5py
import numpy as np

import boss_bench as bb

path = bb.list_files("BoSS", "confinement", "test")[0]
with h5py.File(path, "r") as f:
    for i in range(len(f["uuid"])):
        lost = bb.load_record(f, i, ["confinement_time", "t_max", "s_init"])
        loss_fraction = bb.loss_fraction(
            lost["confinement_time"], lost["t_max"], lost["s_init"], s0=0.1)
        if loss_fraction < 0.1:
            break
    record = bb.load_record(f, i)

conditions = {}
for name in models.inverse_design.CONDITIONS:
    if name == "loss_fraction":
        conditions[name] = loss_fraction
    else:
        conditions[name] = record[name]
    print(f"{name}: {np.round(conditions[name], 3)}")
```

```text
nfp: 2
loss_fraction: 0.001
toroidal_flux_edge: 70.581
minor_radius: 2.184
aspect_ratio: 10.0
min_modB: 4.642
mirror_ratio: 1.148
pressure: [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
iota: [0.402 0.402 0.402 0.401 0.401 0.401 0.401 0.4   0.4   0.4   0.4   0.399
 0.399 0.399 0.399]
vmec_ncurr: 1
```

## Generate and plot a design

{meth}`~boss_bench.models.inverse_design.InverseDesignModel.sample` generates a
boundary with these properties, laid out as the field `boundary_xyz`. Each call with
another seed draws another design:

```python
design = model.sample(conditions, seed=0)
```

{func}`~boss_bench.plotting.plot_device` draws it over the full torus. A generated
boundary has no $\lvert B \rvert$ until its equilibrium is computed, so it is drawn in
one color:

```python
generated = {name: record[name] for name in ("nfp", "phi1d", "theta1d")}
generated["boundary_xyz"] = design
bb.plot_device(generated)
```

```{figure} ../_static/tutorials/designing_stellarators.png
:alt: A stellarator boundary generated with the properties of a low-loss test stellarator
```

To ask for a different design, change the conditions, for example a lower
`loss_fraction`. To check a design, compute its equilibrium with VMEC and trace its
alpha particles; the inverse-design benchmark, {func}`~boss_bench.design.design_metrics`,
scores designs evaluated this way.
