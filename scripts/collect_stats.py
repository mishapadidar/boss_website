"""Collect the numbers behind docs/data/overview.md from the release files on the cluster.

Writes one row per configuration (source, split, scalar properties, the mean of the iota and
quasi-symmetry error profiles, and the loss fraction of the particles born on each surface)
to boss_site_stats.npz, and the size and contents of every file to boss_site_files.json,
both in overview_data/ of this checkout (not committed). Run on rusty, then plot with
make_overview_figures.py (see README.md).
"""
import glob, json, os, pathlib
import h5py
import numpy as np

ROOT = "/mnt/home/mpadidar/ceph/artemiss/bossbench"
OUT = pathlib.Path(__file__).resolve().parents[1] / "overview_data"
SCALARS = ["nfp", "aspect_ratio", "major_radius", "minor_radius", "plasma_beta",
           "volume_avg_modB", "mirror_ratio", "enforce_vacuum", "stellsym"]
PROFILES = ["iota", "sqrt_boozer_qs_error"]
S_INITS = {"10": 0.1, "25": 0.25, "50": 0.5}
LOSS_TOL = 1e-14   # as in boss_bench.confinement
CHUNK = 256

files = []
rows = {k: [] for k in ["uuid", "source_dataset", "source_id", "split", "fname", "row"] + SCALARS
        + [f"{k}_mean" for k in PROFILES] + [f"loss_fraction_s_0_{s}" for s in S_INITS]}
for path in sorted(glob.glob(f"{ROOT}/confinement/*.hdf5")):
    name = os.path.basename(path)
    split = "test" if "_test_" in name else "train"
    with h5py.File(path, "r") as f:
        n = f["uuid"].shape[0]
        rows["uuid"] += list(f["uuid"].asstr()[:])
        rows["source_dataset"] += list(f["source_dataset"].asstr()[:])
        rows["source_id"] += list(f["source_id"].asstr()[:])
        for k in SCALARS:
            rows[k] += list(f[k][:].reshape(n))
        for k in PROFILES:                    # averaged over the 15 flux surfaces of s1d
            rows[f"{k}_mean"] += list(f[k][:].mean(axis=1))
        t_max = f["t_max"][:]
        for a in range(0, n, CHUNK):
            lost = f["confinement_time"][a:a + CHUNK] < t_max[a:a + CHUNK, None] - LOSS_TOL
            s_init = f["s_init"][a:a + CHUNK]
            for key, s0 in S_INITS.items():
                born = np.isclose(s_init, s0)
                rows[f"loss_fraction_s_0_{key}"] += list((lost & born).sum(1) / born.sum(1))
    rows["split"] += [split] * n
    rows["fname"] += [name] * n
    rows["row"] += list(range(n))
    files.append({"kind": "confinement", "name": name, "split": split,
                  "bytes": os.path.getsize(path), "n_configs": n})
    print(name, n, flush=True)

for path in sorted(glob.glob(f"{ROOT}/trajectories/*.hdf5")):
    name = os.path.basename(path)
    with h5py.File(path, "r") as f:
        n = f["config_offsets"].shape[0] - 1
        n_orbits = f["traj_offsets"].shape[0] - 1
        n_samples = f["traj_data"].shape[0]
        uuids = list(f["uuid"].asstr()[:])
    files.append({"kind": "trajectory", "name": name,
                  "split": "test" if "_test_" in name else "train",
                  "bytes": os.path.getsize(path), "n_configs": n,
                  "n_orbits": n_orbits, "n_samples": n_samples, "uuids": uuids})
print("trajectory files", sum(f["kind"] == "trajectory" for f in files), flush=True)

OUT.mkdir(exist_ok=True)
np.savez_compressed(f"{OUT}/boss_site_stats.npz",
                    **{k: np.asarray(v) for k, v in rows.items()})
json.dump(files, open(f"{OUT}/boss_site_files.json", "w"))
print("configs", len(rows["uuid"]))
