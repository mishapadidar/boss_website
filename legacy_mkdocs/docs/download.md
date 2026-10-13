# Download

BoSS is hosted on Hugging Face.

[BoSS on Hugging Face :material-open-in-new:](https://huggingface.co/datasets/mishapadidar/ARTEMISS){ .md-button .md-button--primary }

The dataset contains two kinds of data:

- **Confinement data**: for each stellarator configuration, its geometry,
  magnetic field, and equilibrium profiles, along with the initial and
  final states and confinement times of 15,000 alpha particles.
  See [Fast-ion confinement](data/fast-ion.md#particle-fields).
- **Trajectory data**: full guiding-center orbits of alpha particles,
  sampled over time. See [Trajectory fields](data/fast-ion.md#trajectory-fields).

Both are split into train and test sets, and the split is part of each
file name.
