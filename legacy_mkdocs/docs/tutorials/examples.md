# Working with records

These examples build on [Loading the data](loading.md). Each one starts from a
single configuration record `rec`, a dict of NumPy arrays read with the
`load_record` helper:

```python
import h5py
import numpy as np

path = "BoSS/confinement/confinement_data_test_split_00000.hdf5"
with h5py.File(path, "r") as f:
    rec = load_record(f, 0)       # defined in "Loading the data"
```

## Reshape the gridded fields

Multi-dimensional fields are stored flattened (see
[conventions](../data/index.md#grids-and-array-shapes)):

```python
modB        = rec["modB"].reshape(15, 41, 41)          # (s, phi, theta), VMEC angles
modB_boozer = rec["modB_boozer"].reshape(15, 41, 41)   # (s, phi, theta), Boozer angles
surf        = rec["surf_xyz"].reshape(41, 41, 3)       # (phi, theta, xyz), one field period
axis        = rec["xyz_axis"].reshape(41, 3)           # (phi, xyz), one field period
```

## Plot |B| on a flux surface

In Boozer coordinates, a quasi-symmetric configuration has straight \(|B|\)
contours, and a quasi-isodynamic one has poloidally closed contours.

```python
import matplotlib.pyplot as plt

js = 7                                         # index into s1d (s = 0.5)
fig, ax = plt.subplots(figsize=(5, 4))
cs = ax.contourf(rec["phi1d"], rec["theta1d"], modB_boozer[js].T, levels=20)
ax.set_xlabel(r"Boozer $\varphi$")
ax.set_ylabel(r"Boozer $\theta$")
ax.set_title(f"|B| at s = {rec['s1d'][js]:.2f}  ({rec['database_from']})")
fig.colorbar(cs, label="|B| [T]")
```

## Plot the plasma boundary in 3-D

`surf_xyz` covers one field period. To get the full torus, rotate it by
\(2\pi k / n_\text{fp}\) for each period \(k\):

```python
def full_torus(xyz, nfp):
    """Tile a one-field-period (nphi, ntheta, 3) array around the torus."""
    parts = []
    for k in range(nfp):
        a = 2 * np.pi * k / nfp
        rot = np.array([[np.cos(a), -np.sin(a), 0],
                        [np.sin(a),  np.cos(a), 0],
                        [0,          0,         1]])
        parts.append(xyz @ rot.T)
    full = np.concatenate(parts, axis=0)
    full = np.concatenate([full, full[:1]], axis=0)      # close in phi
    return np.concatenate([full, full[:, :1]], axis=1)   # close in theta

X = full_torus(surf, rec["nfp"])
ax = plt.figure(figsize=(7, 5)).add_subplot(projection="3d")
ax.plot_surface(X[..., 0], X[..., 1], X[..., 2], cmap="viridis", linewidth=0)
ax.set_aspect("equal")
ax.set_axis_off()
```

## Reconstruct the boundary from Fourier modes

`surf_xyz` is sampled on a fixed 41 × 41 grid. For a finer surface, or for normals and
curvature, evaluate the Fourier series in `surf_full_res_fourier_modes` at any
resolution. With NumPy alone:

```python
def boundary_from_modes(modes, nfp, phi, theta, mpol=20, ntor=20):
    """Evaluate a stellarator-symmetric SurfaceRZFourier at angles in turns.

    phi, theta: 1-D arrays in units of full turns (as in surf_quadpoints_*).
    Returns an array of shape (len(phi), len(theta), 3).
    """
    m_rc = np.r_[np.zeros(ntor + 1), np.repeat(np.arange(1, mpol + 1), 2 * ntor + 1)]
    n_rc = np.r_[np.arange(ntor + 1), np.tile(np.arange(-ntor, ntor + 1), mpol)]
    m_zs, n_zs = m_rc[1:], n_rc[1:]            # Z has no (m, n) = (0, 0) term
    rc, zs = modes[: len(m_rc)], modes[len(m_rc):]

    P, T = np.meshgrid(2 * np.pi * phi, 2 * np.pi * theta, indexing="ij")
    ang_r = m_rc * T[..., None] - n_rc * nfp * P[..., None]
    ang_z = m_zs * T[..., None] - n_zs * nfp * P[..., None]
    R = np.cos(ang_r) @ rc
    Z = np.sin(ang_z) @ zs
    return np.stack([R * np.cos(P), R * np.sin(P), Z], axis=-1)

# sanity check: reproduces surf_xyz to ~1e-14
xyz = boundary_from_modes(rec["surf_full_res_fourier_modes"], rec["nfp"],
                          rec["surf_quadpoints_phi"], rec["surf_quadpoints_theta"])
assert np.allclose(xyz, surf)

# a fine grid over the full torus
fine = boundary_from_modes(rec["surf_full_res_fourier_modes"], rec["nfp"],
                           np.linspace(0, 1, 200), np.linspace(0, 1, 64))
```

??? note "With SIMSOPT instead"
    ```python
    from simsopt.geo import SurfaceRZFourier

    s = SurfaceRZFourier(nfp=int(rec["nfp"]), stellsym=True, mpol=20, ntor=20,
                         quadpoints_phi=np.linspace(0, 1, 200, endpoint=False),
                         quadpoints_theta=np.linspace(0, 1, 64, endpoint=False))
    s.x = rec["surf_full_res_fourier_modes"]
    xyz = s.gamma()            # (200, 64, 3)
    normals = s.unitnormal()
    ```

## Alpha-particle losses

A particle is lost if its `confinement_time` is shorter than `t_max`:

```python
ct, t_max = rec["confinement_time"], rec["t_max"]
lost = ct < t_max
print(f"total loss fraction: {lost.mean():.3f}")

# per birth surface
for s0 in np.unique(rec["s_init"]):
    on_surface = rec["s_init"] == s0
    print(f"  s_init = {s0:.2f}: {lost[on_surface].mean():.3f}")
```

Loss fraction as a function of time, the usual way to show confinement:

```python
t = np.logspace(-5, np.log10(t_max), 200)
loss_vs_t = (ct[None, :] < t[:, None]).mean(axis=1)

fig, ax = plt.subplots()
ax.semilogx(t, loss_vs_t)
ax.set_xlabel("time [s]")
ax.set_ylabel("cumulative loss fraction")
```

Where on the torus do lost particles start? Plot their initial Boozer angles:

```python
fig, ax = plt.subplots()
ax.scatter(rec["z_init"][~lost], rec["t_init"][~lost], s=1, c="lightgray", label="confined")
ax.scatter(rec["z_init"][lost],  rec["t_init"][lost],  s=1, c="C3", label="lost")
ax.set_xlabel(r"Boozer $\zeta_0$")
ax.set_ylabel(r"Boozer $\theta_0$")
ax.legend(markerscale=8)
```

## A first surrogate model

Predict the loss fraction of particles born at \(s = 0.25\) from a few scalar
properties. Train on a train file, and evaluate on a test file.

```python
import h5py
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

FEATURES = ["nfp", "plasma_beta", "aspect_ratio", "mirror_ratio",
            "axis_helicity", "vacuum_well", "min_L_grad_B"]

def features_and_target(path, s0=0.25):
    with h5py.File(path, "r") as f:
        X = np.column_stack([f[k][:] for k in FEATURES])
        ct, s_init, t_max = f["confinement_time"][:], f["s_init"][:], f["t_max"][:]
    lost = ct < t_max[:, None]
    on_surface = s_init == s0
    y = (lost & on_surface).sum(axis=1) / on_surface.sum(axis=1)
    return X, y

X_train, y_train = features_and_target("BoSS/confinement/confinement_data_train_split_00000.hdf5")
X_test, y_test = features_and_target("BoSS/confinement/confinement_data_test_split_00000.hdf5")

model = HistGradientBoostingRegressor().fit(X_train, y_train)
print(f"test MAE: {mean_absolute_error(y_test, model.predict(X_test)):.3f}")
```
