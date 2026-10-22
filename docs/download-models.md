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

To download single files, open the link and use the **Files and versions** tab. To
download whole model folders, use the Hugging Face command line, `hf download`:

```bash
hf download mishapadidar/boss --include "heat_flux/*" --local-dir BoSS-models                # one model
hf download mishapadidar/boss --include "*/config.json" --include "*.onnx" --local-dir BoSS-models   # ONNX only
hf download mishapadidar/boss --local-dir BoSS-models                                         # everything
```

or the [`boss-bench`](package.md) pip package, for the PyTorch files of one model:

```python
boss_bench.models.download("heat_flux", "BoSS-models/heat_flux")
```

Once the files are downloaded, use the [`boss-bench`](package.md) pip package to load and
run the models.
