# Using the inverse-design model

This tutorial generates a stellarator boundary with the Diffusion baseline of the
paper's inverse-design task, and plots it. The boundary is asked to have the properties
of a stellarator from the test split, but a tenth of its loss fraction.

As in [Using the loss-fraction surrogate](using-loss-fraction-surrogate.md), install
the package with its models and download `confinement_data_test_split_00000.hdf5` into
`BoSS/`. {meth}`~boss_bench.models.inverse_design.InverseDesignModel.sample` takes the
properties by the names of the BoSS fields, and returns a boundary laid out as
`boundary_xyz`:

```python
import h5py
import matplotlib.pyplot as plt

import boss_bench as bb
from boss_bench import models
from boss_bench.models import InverseDesignModel

path = models.download("inverse_design", "BoSS-models/inverse_design")
model = InverseDesignModel.load(path)

path = bb.list_files("BoSS", "confinement", "test")[0]
with h5py.File(path, "r") as f:
    record = bb.load_record(f, 0)

loss_fraction = bb.loss_fraction(
    record["confinement_time"], record["t_max"], record["s_init"], s0=0.1)

# the properties of the test stellarator, with a tenth of its loss fraction
names = models.inverse_design.CONDITIONS
conditions = {name: record[name] for name in names if name != "loss_fraction"}
conditions["loss_fraction"] = 0.1 * loss_fraction
design = model.sample(conditions, seed=0)
```

{func}`~boss_bench.plotting.plot_device` draws the test stellarator, colored by
$\lvert B \rvert$, and the generated boundary, which has no $\lvert B \rvert$ until its
equilibrium is computed:

```python
generated = {name: record[name] for name in ("nfp", "phi1d", "theta1d")}
generated["boundary_xyz"] = design

fig = plt.figure(figsize=(10, 5))
ax1 = fig.add_subplot(1, 2, 1, projection="3d")
ax2 = fig.add_subplot(1, 2, 2, projection="3d")
bb.plot_device(record, ax=ax1)
bb.plot_device(generated, ax=ax2)
ax1.set_title(f"test stellarator, loss fraction {loss_fraction:.2f}")
ax2.set_title(f"generated for loss fraction {0.1 * loss_fraction:.2f}")
```

```{figure} ../_static/tutorials/using_inverse_design_model.png
:alt: A test stellarator colored by |B|, next to a boundary generated with the same properties and a tenth of its loss fraction
```

To check a design, compute its equilibrium with VMEC and trace its alpha particles; the
inverse-design benchmark, {func}`~boss_bench.design.design_metrics`, scores designs
evaluated this way.
