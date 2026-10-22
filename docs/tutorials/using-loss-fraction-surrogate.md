# Using the loss-fraction surrogate

This tutorial predicts the loss fraction of a stellarator from the test split with
the paper's trained surrogate, which needs no VMEC run.

Install the package with its models:

```bash
pip install "boss-bench[models]"
```

and download `confinement_data_test_split_00000.hdf5` from the
[Download Data](../download.md) page into a folder, here `BoSS/`.
{func}`~boss_bench.models.download` saves the model in a folder, and
{meth}`~boss_bench.models.loss_fraction.LossFractionModel.load` loads it:

```python
import h5py

import boss_bench as bb
from boss_bench import models
from boss_bench.models import LossFractionModel

path = models.download("loss_fraction", "BoSS-models/loss_fraction")
model = LossFractionModel.load(path)

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
of configurations, such as the fields from {func}`~boss_bench.data.load`. The inputs
are described in {class}`~boss_bench.models.loss_fraction.LossFractionModel`.

Next: [Using the heat-flux model →](using-heat-flux-model.md)
