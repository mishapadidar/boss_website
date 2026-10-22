# Using the heat-flux model

This tutorial predicts where the lost alpha particles of a stellarator from the test
split strike the plasma boundary, with the IID baseline of the paper's heat-flux task,
and plots the predicted heat flux next to the true one.

As in [Using the loss-fraction surrogate](using-loss-fraction-surrogate.md), install
the package with its models and download `confinement_data_test_split_00000.hdf5` into
`BoSS/`. {meth}`~boss_bench.models.heat_flux.HeatFluxModel.sample` samples the strike
points of the particles born on one surface $s_0$, with the predicted loss fraction:

```python
import h5py

import boss_bench as bb
from boss_bench import models
from boss_bench.models import HeatFluxModel

path = models.download("heat_flux", "BoSS-models/heat_flux")
model = HeatFluxModel.load(path)

path = bb.list_files("BoSS", "confinement", "test")[0]
with h5py.File(path, "r") as f:
    record = bb.load_record(f, 0)

predictions = {}
for s0 in (0.1, 0.25, 0.5):
    predictions[s0] = model.sample(record, s0=s0, seed=0)
bb.plot_heat_flux(record, predictions)
```

```{figure} ../_static/tutorials/using_heat_flux_model.png
:alt: True and predicted heat flux on the plasma boundary over one field period, for each birth surface
```

Each prediction is a tuple `(zeta, theta, energy, loss_fraction)`, the format that
{func}`~boss_bench.heat_flux.heat_flux_error` and the heat-flux benchmark,
{func}`~boss_bench.heat_flux.heat_flux_metrics`, score:

```python
for s0, prediction in predictions.items():
    error = bb.heat_flux_error(prediction, record, s0)
    print(f"s0 = {s0}: heat-flux error {error:.3f}")
```

```text
s0 = 0.1: heat-flux error 0.332
s0 = 0.25: heat-flux error 0.378
s0 = 0.5: heat-flux error 0.565
```

Next: [Using the inverse-design model →](using-inverse-design-model.md)
