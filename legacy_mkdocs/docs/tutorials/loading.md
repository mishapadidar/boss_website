# Loading the data

The examples assume you have [downloaded](../download.md) some or all of the
database into a folder called `BoSS/`:

```text
BoSS/
├── confinement/      # configuration data + fast-ion confinement
└── trajectories/     # full particle orbits
```

## A confinement file with `h5py`

Each confinement file holds about 3,000 complete configuration records.
Every field is a top-level dataset whose first axis runs over
configurations, so you can slice what you need without loading the whole
5 GB file.

```python
import h5py

path = "BoSS/confinement/confinement_data_test_split_00000.hdf5"

with h5py.File(path, "r") as f:
    # list every field with its shape
    for name, dset in f.items():
        print(f"{name:30s} {dset.shape} {dset.dtype}")

    n = f["uuid"].shape[0]                         # configurations in this file
    aspect = f["aspect_ratio"][:]                  # (n,) one scalar per configuration
    iota_10 = f["iota"][10]                        # (15,) profile of configuration 10
    ct_first_100 = f["confinement_time"][:100]     # (100, 15000)

    # string fields are variable-length strings
    uuids = f["uuid"].asstr()[:]
    source = f["database_from"].asstr()[:]
```

!!! tip "Read only what you need"
    The particle arrays (`confinement_time`, `s_init`, …, each
    `(n, 15000)`) and the gridded fields (`modB`, …, each `(n, 25215)`) make
    up almost all of each file. Reading a slice like `f["modB"][i]` touches
    only the chunks it needs.

## One configuration as a dict

This helper reads configuration `i` from any confinement or trajectory
file:

```python
def load_record(f, i):
    """Return configuration i of an open h5py.File as a dict of NumPy arrays / str.

    Skips the ragged trajectory datasets, which are not indexed by configuration.
    """
    rec = {}
    for name, dset in f.items():
        if name in ("traj_data", "traj_offsets", "config_offsets"):
            continue
        rec[name] = dset.asstr()[i] if dset.dtype.kind == "O" else dset[i]
    return rec

with h5py.File(path, "r") as f:
    rec = load_record(f, 0)
```

## Find a configuration by `uuid`

To find the full record of a configuration, search the files for its `uuid`:

```python
import glob
import h5py
import numpy as np

def find_record(uuid, folder="BoSS/confinement"):
    for path in sorted(glob.glob(f"{folder}/*.hdf5")):
        with h5py.File(path, "r") as f:
            hits = np.flatnonzero(f["uuid"].asstr()[:] == uuid)
            if hits.size:
                return load_record(f, hits[0])
    raise KeyError(uuid)
```

For repeated lookups, build a `uuid → (file, row)` index once and save it.

## A table of scalars across many files

Many analyses need only the scalar fields. Here they are collected from
every train file into one table:

```python
import glob
import h5py
import pandas as pd

SCALARS = [
    "nfp", "aspect_ratio", "major_radius", "minor_radius", "volume",
    "axis_helicity", "integrated_axis_torsion", "max_modB", "min_modB",
    "mirror_ratio", "volavgB", "min_L_grad_B", "phiedge", "plasma_beta",
    "vacuum_well", "enforce_vacuum",
]
STRINGS = ["uuid", "database_from", "database_from_ID"]

frames = []
for path in sorted(glob.glob("BoSS/confinement/confinement_data_train_split_*.hdf5")):
    with h5py.File(path, "r") as f:
        df = pd.DataFrame({k: f[k][:] for k in SCALARS})
        for k in STRINGS:
            df[k] = f[k].asstr()[:]
        frames.append(df)

scalars = pd.concat(frames, ignore_index=True)
```

Next: [Working with records →](examples.md)
