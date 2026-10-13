# Tutorials

These tutorials take you from nothing to a working analysis or ML pipeline.
The snippets work on files from the
[downloaded data](../download.md).

<div class="grid cards" markdown>

-   :material-download-box: **[Loading the data](loading.md)**

    ---

    Read the HDF5 files with `h5py`, look up configurations by `uuid`,
    and gather scalars across files.

-   :material-chart-scatter-plot: **[Working with records](examples.md)**

    ---

    Reshape the gridded fields, plot a boundary surface, compute alpha-particle
    loss fractions, and train a first surrogate model.

</div>

## Requirements

```bash
pip install h5py numpy pandas matplotlib
# optional
pip install scikit-learn torch   # for the ML examples
pip install simsopt   # to rebuild full-resolution surfaces
```
