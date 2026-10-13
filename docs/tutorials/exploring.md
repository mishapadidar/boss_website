# Exploring a stellarator

This tutorial loads one stellarator from a confinement file and looks at its
main characteristics with the `boss-bench` package: the plasma boundary,
$\lvert B \rvert$ on a flux surface, the boundary rebuilt from its Fourier
modes, its alpha-particle losses, and the heat flux those losses put on the
plasma boundary.

```bash
pip install boss-bench
```

## Load a stellarator

Download at least one confinement file of the test split from the
[Download Data](../download.md) page into a folder, here `BoSS/`. Each file
holds about 3,000 stellarators, and every field is an HDF5 dataset whose
first axis runs over them, so row `i` of every dataset belongs to stellarator
`i`.

```python
import h5py
import matplotlib.pyplot as plt
import numpy as np

import boss_bench as bb

path = bb.list_files("BoSS", "confinement", "test")[0]
f = h5py.File(path, "r")
print(len(f["uuid"]), "stellarators in", path)
```

{func}`~boss_bench.data.load_record` reads every field of one stellarator
into a dict. Give it the row of the stellarator, or its `uuid`:

```python
rec = bb.load_record(f, 0)
nfp = int(rec["nfp"])
print(rec["uuid"], "| source:", rec["source_dataset"], "| nfp =", nfp,
      f"| aspect ratio = {rec['aspect_ratio']:.2f} | beta = {rec['plasma_beta']:.4f}")
```

Gridded fields are stored flattened. Reshape them as described in
[grids and array shapes](../data/ideal-mhd.md#grids-and-array-shapes):

```python
modB_boozer = rec["modB_boozer"].reshape(15, 41, 41)   # (s, zeta, theta), Boozer angles
boundary    = rec["boundary_xyz"].reshape(41, 41, 3)   # (phi, theta, xyz), one field period
```

## The plasma boundary

`boundary_xyz` covers one field period.
{func}`~boss_bench.plotting.plot_device` copies it around the torus and draws
the whole boundary, colored by $\lvert B \rvert$ and viewed from above:

```python
bb.plot_device(rec)
```

```{figure} ../_static/tutorials/boundary_3d.png
:alt: The plasma boundary seen from above, colored by the magnitude of B
:width: 420px
```

## |B| on a flux surface

In Boozer coordinates a quasi-symmetric stellarator has straight
$\lvert B \rvert$ contours, and a quasi-isodynamic one has poloidally closed
contours. {func}`~boss_bench.plotting.plot_modB_boozer` draws
$\lvert B \rvert$ on the stored flux surface nearest to $s$, with field lines
in black:

```python
bb.plot_modB_boozer(rec, s=0.5)
```

```{figure} ../_static/tutorials/modB.png
:alt: Magnitude of B on the s = 0.5 flux surface, in Boozer angles
:width: 480px
```

## The boundary from its Fourier modes

`boundary_xyz` is sampled on a fixed 41 × 41 grid. For a finer surface, or
for normals and curvature, evaluate the Fourier series in
`boundary_full_res_fourier_modes` at any resolution
([boundary Fourier modes](../data/ideal-mhd.md#boundary-fourier-modes)
describes the layout). With NumPy alone:

```python
def boundary_from_modes(modes, nfp, phi, theta, mpol=20, ntor=20):
    """Evaluate a stellarator-symmetric SurfaceRZFourier at angles in turns.

    phi, theta: 1-D arrays in units of full turns (as in boundary_quadpoints_*).
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

modes = rec["boundary_full_res_fourier_modes"]

# on the stored grid it reproduces boundary_xyz to round-off
xyz = boundary_from_modes(modes, nfp, rec["boundary_quadpoints_phi"], rec["boundary_quadpoints_theta"])
print("max |difference| from boundary_xyz:", np.abs(xyz - boundary).max())

# a fine grid over the full torus
fine = boundary_from_modes(modes, nfp, np.linspace(0, 1, 200), np.linspace(0, 1, 64))
```

:::{dropdown} With SIMSOPT instead
```python
from simsopt.geo import SurfaceRZFourier

s = SurfaceRZFourier(nfp=nfp, stellsym=True, mpol=20, ntor=20,
                     quadpoints_phi=np.linspace(0, 1, 200, endpoint=False),
                     quadpoints_theta=np.linspace(0, 1, 64, endpoint=False))
s.x = modes
xyz = s.gamma()            # (200, 64, 3)
normals = s.unitnormal()
```
:::

## Alpha-particle losses

The stellarator has 15,000 alpha particles, 5,000 born on each of the
surfaces $s_0 = 0.1$, $0.25$ and $0.5$. A particle is lost if its
`confinement_time` is shorter than the simulation time `t_max`. Loss
quantities are computed over the particles born on one surface:

```python
ct, t_max, s_init = rec["confinement_time"], rec["t_max"], rec["s_init"]
for s0 in (0.1, 0.25, 0.5):
    print(f"born on s = {s0}: "
          f"loss fraction {bb.loss_fraction(ct, t_max, s_init, s0):.3f}, "
          f"normalized energy loss {bb.normalized_energy_loss(ct, t_max, s_init, s0):.3f}")
```

The fraction of particles lost by time $t$ shows how quickly they are lost.
Particles born closer to the edge are lost sooner:

```python
bb.plot_loss_fraction_curves(rec)
```

```{figure} ../_static/tutorials/loss_fraction_vs_time.png
:alt: Fraction of alpha particles lost versus time, by birth surface
:width: 440px
```

Where were the lost particles born? Plot their initial Boozer angles:

```python
lost = bb.is_lost(ct, t_max)
fig, ax = plt.subplots(figsize=(5.5, 3.5))
ax.scatter(rec["zeta_init"][~lost], rec["theta_init"][~lost], s=1, c="lightgray", label="confined")
ax.scatter(rec["zeta_init"][lost], rec["theta_init"][lost], s=1, c="C3", label="lost")
ax.set_xlabel(r"initial Boozer toroidal angle $\zeta_0$")
ax.set_ylabel(r"initial Boozer poloidal angle $\theta_0$")
ax.legend(markerscale=8, loc="upper right")
fig.tight_layout()
```

```{figure} ../_static/tutorials/birth_points.png
:alt: Birth positions of lost and confined particles in Boozer angles
:width: 480px
```

## Heat flux on the plasma boundary

Lost particles strike the plasma boundary at their final Boozer angles
`zeta_end` ($\zeta_B$) and `theta_end` ($\theta_B$).
{func}`~boss_bench.heat_flux.lost_particles` returns the strike points of the
particles born on one surface, and their energies. A particle lost at time
$t_\text{loss}$ carries
$E = 3.5\,\text{MeV} \cdot e^{-2 t_\text{loss} / t_\text{max}}$, a weight that
models slowing down (the tracing itself conserves energy):

```python
zeta, theta, energy, n_launched = bb.lost_particles(rec, s0=0.1)
print(f"{len(zeta)} of the {n_launched} particles born on s = 0.1 are lost")
```

{func}`~boss_bench.heat_flux.binned_heat_flux` folds the strike points of all
field periods into one, bins their energy, and divides each bin by its area on
the boundary, computed from `R_boozer`, `Z_boozer` and `nu_boozer` at $s = 1$.
The result is the heat flux $Q$ in MeV/m² per launched particle:

```python
Q = bb.binned_heat_flux(zeta, theta, energy, n_launched, rec, resolution=32)
print(Q.shape, f"peak {Q.max():.3g} MeV/m^2 per particle")    # (zeta bin, theta bin)
```

To get W/m², multiply $Q$ by an alpha birth rate (particles per second) and
by $1.602 \times 10^{-13}$ J/MeV.

{func}`~boss_bench.plotting.plot_strike_points` and
{func}`~boss_bench.plotting.plot_heat_flux` draw the strike points and the
heat flux for each birth surface:

```python
bb.plot_strike_points(rec)
bb.plot_heat_flux(rec)
```

```{figure} ../_static/tutorials/strike_points.png
:alt: Strike points of the lost particles colored by energy, and their density, for each birth surface
:width: 640px
```

```{figure} ../_static/tutorials/heat_flux.png
:alt: Heat flux of lost alpha particles on the plasma boundary over one field period, for each birth surface
:width: 400px
```

Both functions also take predicted strike points and draw them next to the
truth. Predicting them is the heat-flux benchmark; see
[Heat flux](../package.md#heat-flux).

```python
f.close()
```

The figures on this page are the output for stellarator 0 of
`confinement_data_test_split_00000.hdf5`.

Next: [Loading trajectory data →](loading-trajectories.md)
