# Download Models

The trained models of the BoSS paper are distributed through Hugging Face, in PyTorch
and ONNX.

```{button-link} https://huggingface.co/mishapadidar/boss
:color: primary
:shadow:

The BoSS models on Hugging Face
```

Three models are available, each in its own folder of the repository:

`loss_fraction`
: A neural surrogate which predicts the loss fraction of the alpha particles born on
  $s_0 = 0.1$ from the plasma boundary and profiles, without a VMEC run.

`heat_flux`
: A flow matching model which samples the locations at which lost fast ions strike the
  boundary.

`inverse_design`
: A flow matching model which generates plasma boundaries with a desired loss fraction,
  shape, field and profiles.

Use the [`boss-bench`](package.md) pip package to download and run the models.
Install it with its models:

```bash
pip install "boss-bench[models]"
```

Then this downloads one model into a folder, with its ONNX files if `onnx=True`:

```python
from boss_bench import models

models.download("heat_flux", "BoSS-models/heat_flux", onnx=True)
```

The models can also be downloaded directly from Hugging Face, with its command line:

```bash
pip install huggingface_hub

# one model
hf download mishapadidar/boss --include "heat_flux/*" \
    --local-dir BoSS-models

# the ONNX files only
hf download mishapadidar/boss --include "*.onnx" \
    --include "*/config.json" --local-dir BoSS-models

# everything
hf download mishapadidar/boss --local-dir BoSS-models
```

or one file at a time, from the **Files and versions** tab of the repository.

The tutorials show how to run each model:
[Using the loss-fraction surrogate](tutorials/using-loss-fraction-surrogate.md),
[Using the heat-flux model](tutorials/using-heat-flux-model.md) and
[Designing stellarators with a generative model](tutorials/designing-stellarators.md).
