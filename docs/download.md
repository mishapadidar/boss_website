# Download Data

The BoSS is distributed through Globus.

```{button-link} https://app.globus.org/file-manager?origin_id=04779ab9-4a4e-4381-be6a-860f0433a4af&origin_path=%2F
:color: primary
:shadow:

The BoSS on Globus
```

To download from Globus, open the link and log in with your institution,
Google, or ORCID account. Select the files you want and click **Download**,
or, for large transfers, use **Transfer or Sync to…** to send them to your
own Globus endpoint (for example a cluster, or your laptop running
[Globus Connect Personal](https://www.globus.org/globus-connect-personal)).

Once the files are downloaded, use the [`boss-bench`](package.md) pip package to read and
plot the data.

## Download Models

The pretrained models of the paper are on Hugging Face, in PyTorch and ONNX.

```{button-link} https://huggingface.co/mishapadidar/boss
:color: primary
:shadow:

The BoSS models on Hugging Face
```

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

To run the PyTorch models, install the package with its `models` extra. Then
{func}`~boss_bench.pretrained.download_model` downloads a model into a folder, and
{func}`~boss_bench.models.load` loads it:

```bash
pip install "boss-bench[models]"
```

```python
import boss_bench as bb
from boss_bench import models

surrogate = models.load(bb.download_model("loss_fraction", "BoSS-models"))
surrogate.predict(record)       # a configuration's fields, from bb.load_record
```

Each model reads the BoSS fields it needs by name, from one configuration or from a
batch of them. The [package documentation](package.md) describes each model.

The ONNX files run without PyTorch, for example with
[ONNX Runtime](https://onnxruntime.ai/). To download them as well, pass `onnx=True` to
{func}`~boss_bench.pretrained.download_model`, or download them from Hugging Face. The
model card on Hugging Face describes their inputs.
