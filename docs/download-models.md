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
: Predicts the loss fraction of the alpha particles born on $s = 0.1$ from the plasma
  boundary and profiles, without a VMEC run. It is the surrogate used in the paper's
  surrogate-based optimization.

`heat_flux`
: Samples where the lost alpha particles strike the boundary, and predicts their loss
  fraction, for particles born on $s = 0.1$, $0.25$ or $0.5$. It is the flow-matching
  model of the heat-flux benchmark.

`inverse_design`
: Generates plasma boundaries with a chosen loss fraction, shape, field and profiles.

To download single files, open the link and use the **Files and versions** tab. To
download whole model folders, use the Hugging Face command line, from
`pip install huggingface_hub`:

```bash
hf download mishapadidar/boss --include "heat_flux/*" --local-dir BoSS-models                # one model
hf download mishapadidar/boss --include "*/config.json" --include "*.onnx" --local-dir BoSS-models   # ONNX only
hf download mishapadidar/boss --local-dir BoSS-models                                         # everything
```

Once the files are downloaded, use the [`boss-bench`](package.md) pip package to load and
run the models.
