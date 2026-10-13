# Loading trajectory data

The trajectory files hold full guiding-center orbits of alpha particles. Each
file covers **40 configurations** with **6,000 orbits per configuration**,
sampled every 1 µs for the first 1 ms. See
[Trajectory fields](../data/fast-ion.md#trajectory-fields) for every field.

```bash
pip install boss-bench
```

## How the orbits are stored

Orbits have different lengths, because a lost particle stops early, so they
are stacked into one array with offsets marking where each one starts:

| Dataset | Shape | What it holds |
| --- | --- | --- |
| `traj_data` | `(n_samples, 5)` | Every orbit sample in the file, one row each: time $t$ [s], $s$, Boozer $\theta$ [rad], Boozer $\zeta$ [rad], $v_\parallel$ [m/s] |
| `traj_offsets` | `(n_orbits + 1,)` | Orbit `k` is rows `traj_offsets[k]` to `traj_offsets[k+1]` of `traj_data` |
| `config_offsets` | `(n_configs + 1,)` | The orbits of configuration `i` are `config_offsets[i]` to `config_offsets[i+1] - 1` |

The file also holds the [configuration fields](../data/ideal-mhd.md)
(`uuid`, `nfp`, `modB_boozer`, `iota`, …) for its 40 configurations, one row
per configuration, exactly as in a confinement file.

## One orbit

With the offsets, one orbit can be read with h5py alone:

```python
import h5py
import numpy as np

import boss_bench as bb

path = bb.list_files("BoSS", "trajectory", "test")[0]

with h5py.File(path, "r") as f:
    i, j = 0, 5                                    # configuration i, its orbit j
    k = f["config_offsets"][i] + j
    a, b = f["traj_offsets"][k], f["traj_offsets"][k + 1]
    t, s, theta, zeta, vpar = f["traj_data"][a:b].T
    uuid = f["uuid"].asstr()[i]

print(f"{uuid}: {b - a} samples, t from {t[0] * 1e6:.0f} to {t[-1] * 1e6:.1f} us")
```

The first sample is at $t = 1$ µs and the samples are 1 µs apart. The angles
are wrapped to $(-\pi, \pi]$.

## All orbits of one configuration

{func}`~boss_bench.trajectory.read_trajectories` reads all orbits of a
configuration at once. `traj_data` is stored in chunks that run down each
column, so this one contiguous read is much faster than reading orbits one at
a time. It returns the orbits on a common 1 µs grid, in the embedded form
that the [trajectory benchmark](../package.md#trajectories) uses,

$$
z = \left(\sqrt{s}\cos\theta,\ \sqrt{s}\sin\theta,\ \cos\varphi,\ \sin\varphi,\ v_\parallel / v_\alpha\right),
$$

with $\theta$ and $\varphi$ the Boozer poloidal and toroidal angles, and
$v_\alpha$ the speed of a 3.5 MeV alpha particle
({func}`~boss_bench.trajectory.embed_state` computes $z$ from a state):

```python
with h5py.File(path, "r") as f:
    orbits = bb.read_trajectories(f, 0)            # by row, or by uuid

z = orbits["z"]
print(z.shape)                                     # (n_orbits, 1000, 5)
```

Row `k` of an orbit is the state $k$ µs after its first sample. A lost orbit
stops early, and its rows after the last sample are NaN; `n_valid` counts the
rows that are filled.

## Which orbits are lost

A particle that leaves the plasma within the 1 ms window stops early, at
$s \ge 0.98$, where the integrator stops it. `t_loss` holds the time it was
lost, and NaN for particles that are still confined at 1 ms:

```python
t_loss = orbits["t_loss"]
print(f"lost within 1 ms: {np.isfinite(t_loss).mean():.3f}")
print(f"lost before their first sample: {np.sum(orbits['n_valid'] == 0)}")
```

## Plot orbits

{func}`~boss_bench.plotting.plot_rollouts` draws each channel of $z$ against
time, one row per orbit:

```python
shown = np.flatnonzero(orbits["n_valid"] >= 1)[:3]
bb.plot_rollouts(z[shown])
```

It also takes a model's predicted orbits, `bb.plot_rollouts(z_true, z_pred)`,
and draws them on top.

## Match orbits to their configuration

{func}`~boss_bench.data.load_record` reads the configuration fields of a
trajectory file, as it does for a confinement file. To pair orbits with the
confinement results of the same configuration, look for its `uuid` in the
confinement files of the same split:

```python
with h5py.File(path, "r") as f:
    rec = bb.load_record(f, 0)                     # configuration fields

for conf_path in bb.list_files("BoSS", "confinement", "test"):
    with h5py.File(conf_path, "r") as g:
        if rec["uuid"] in g["uuid"].asstr()[:]:
            conf = bb.load_record(g, rec["uuid"])  # the same configuration, with its 15,000 particles
            break
```

Next: [Fitting a surrogate model →](surrogate.md)
