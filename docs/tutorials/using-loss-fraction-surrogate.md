# Using the loss-fraction surrogate

This tutorial shows how to download our neural surrogate for the loss fraction and use
it to predict the loss fraction of a stellarator from the test split, or a new design
altogether. The surrogate needs no VMEC run.

Install the package with its models:

```bash
pip install "boss-bench[models]"
```

Now download and load the model using the convenience functions from `boss-bench`.
{func}`~boss_bench.models.download` saves the model in a folder, and
{meth}`~boss_bench.models.loss_fraction.LossFractionModel.load` loads it:

```python
from boss_bench import models
from boss_bench.models import LossFractionModel

path = models.download("loss_fraction", "BoSS-models/loss_fraction")
model = LossFractionModel.load(path)
```

## A stellarator from the test split

Download `confinement_data_test_split_00000.hdf5` from the
[Download Data](../download.md) page into a folder, here `BoSS/`. We now load a device
from the test data and use the model to predict its loss fraction:

```python
import h5py

import boss_bench as bb

path = bb.list_files("BoSS", "confinement", "test")[0]
with h5py.File(path, "r") as f:
    record = bb.load_record(f, 0)

predicted = model.predict(record)
true = bb.loss_fraction(
    record["confinement_time"], record["t_max"], record["s_init"], s0=0.1)
print(f"loss fraction: predicted {predicted:.3f}, true {true:.3f}")
```

```text
loss fraction: predicted 0.264, true 0.252
```

{meth}`~boss_bench.models.loss_fraction.LossFractionModel.predict` also takes a batch
of configurations, such as the fields from {func}`~boss_bench.data.load`.

## A new design

The model reads only the plasma boundary, the pressure and current profiles, the
volume-averaged field strength and the number of field periods, so it can also predict
the loss fraction of a *new* design that is not in the data. The boundary is given as
`boundary_xyz`, a `(41, 41, 3)` array of Cartesian points on one field period of the
boundary surface, indexed $(\phi, \theta, xyz)$. Describe the boundary with a
[simsopt](https://simsopt.readthedocs.io) `SurfaceRZFourier` whose quadrature points
are 41 toroidal angles over one field period and 41 poloidal angles, uniformly spaced
and without the endpoint. As shown below, `boundary_xyz = surface.gamma()` is then the
correct input for the model. The profiles are evaluated at 15 radial points linearly
spaced from $s = 10^{-4}$ to 1, the grid `s1d` of the data.

Here the design is a rotating ellipse at the scale of ARIES-CS: three field periods,
a major radius of 7.75 m, a minor radius of about 1.7 m and a volume-averaged field of
5.86 T, in vacuum, so with zero pressure and current (`pip install simsopt`):

```python
import numpy as np
from simsopt.geo import SurfaceRZFourier

nfp = 3
surface = SurfaceRZFourier(
    nfp=nfp, stellsym=True, mpol=1, ntor=1,
    quadpoints_phi=np.linspace(0, 1 / nfp, 41, endpoint=False),
    quadpoints_theta=np.linspace(0, 1, 41, endpoint=False))
surface.set_rc(0, 0, 7.75)  # major radius [m]
surface.set_rc(1, 0, 1.7)   # minor radius [m]
surface.set_zs(1, 0, 1.7)
surface.set_rc(1, 1, 0.5)   # the rotating ellipse
surface.set_zs(1, 1, -0.5)

design = {
    "boundary_xyz": surface.gamma(),    # (41, 41, 3) [m]
    "pressure": np.zeros(15),           # [Pa]
    "toroidal_current": np.zeros(15),   # [A]
    "volume_avg_modB": 5.86,            # [T]
    "nfp": nfp,
}
print(f"predicted loss fraction: {model.predict(design):.3f}")
```

```text
predicted loss fraction: 0.272
```

A plain rotating ellipse is far from an optimized stellarator: the model predicts that
it loses about a quarter of the alpha particles born on $s = 0.1$.

The inputs are described in {class}`~boss_bench.models.loss_fraction.LossFractionModel`.
Calling the model on PyTorch tensors instead of
{meth}`~boss_bench.models.loss_fraction.LossFractionModel.predict` gives the prediction
with gradients, for example with respect to the boundary, for gradient-based
optimization.

Next: [Using the heat-flux model →](using-heat-flux-model.md)
