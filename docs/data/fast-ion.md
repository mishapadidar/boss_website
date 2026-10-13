# Fast-ion confinement

These fields describe the fast-ion confinement simulations: fusion-born alpha
particles followed along their guiding-center orbits in each equilibrium, and
whether each one is confined or lost. For quantities describing the equilibria,
see [Ideal MHD](ideal-mhd.md).

## Simulation setup

| | |
| --- | --- |
| **Code** | [CATAPULT](https://arxiv.org/abs/2604.07617), the GPU guiding-center timestepper in [FIRM3D](https://github.com/ColumbiaStellaratorTheory/firm3d) |
| **Physics** | Collisionless guiding-center motion in Boozer coordinates |
| **Particles** | 15,000 alpha particles per configuration, 3.5 MeV ($v \approx 1.3 \times 10^{7}$ m/s) |
| **Birth surfaces** | 5,000 particles on each of $s = 0.1$, $0.25$, and $0.5$ |
| **Birth distribution** | Uniform over the flux surface; isotropic in velocity, so $v_\parallel$ is uniform on $[-v, v]$ |
| **Loss condition** | The particle reaches $s = 0.98$, just inside the plasma boundary ($s = 1$), where the integrator stops it |
| **Duration** | Until the particle is lost or $t_\text{max} = 0.1$ s (`t_max`) |
| **Machine size** | Each configuration is scaled to a randomly chosen reactor size and field strength |

## Particle fields

Stored in the **confinement files**, with one entry per alpha particle
and 15,000 particles per configuration.

```{table}
:class: boss-fields
:width: 100%

| HDF5 name | Symbol | Type | Description |
| --- | --- | --- | --- |
| `confinement_time` | $t_\text{loss}$ | array `(15000,)` | Time at which the particle was lost, i.e. reached $s = 0.98$ [s]. Equals `t_max` if it was never lost. |
| `s_init` | $s_0$ | array `(15000,)` | Birth surface (0.1, 0.25, or 0.5). |
| `theta_init` | $\theta_{B,0}$ | array `(15000,)` | Initial Boozer poloidal angle, in $[0, 2\pi)$ [rad]. |
| `zeta_init` | $\zeta_{B,0}$ | array `(15000,)` | Initial Boozer toroidal angle, in $[0, 2\pi)$ [rad]. |
| `vpar_init` | $v_{\parallel,0}$ | array `(15000,)` | Initial parallel velocity [m/s]. |
| `s_end` | $s_\text{end}$ | array `(15000,)` | Normalized toroidal flux when the simulation stopped. |
| `theta_end` | $\theta_{B,\text{end}}$ | array `(15000,)` | Final Boozer poloidal angle, in $[-\pi, \pi]$ [rad]. |
| `zeta_end` | $\zeta_{B,\text{end}}$ | array `(15000,)` | Final Boozer toroidal angle, in $[-\pi, \pi)$ [rad]. |
| `vpar_end` | $v_{\parallel,\text{end}}$ | array `(15000,)` | Final parallel velocity [m/s]. |
| `t_max` | $t_\text{max}$ | float | Maximum simulation time, 0.1 s [s]. |
| `tol` | – | float | Relative and absolute tolerance of the adaptive integrator. |
```


A particle is lost if `confinement_time < t_max - 1e-14`. Loss quantities are
computed over the particles born on one surface, e.g. the loss fraction of the
particles born on $s = 0.1$ is
`bb.loss_fraction(confinement_time, t_max, s_init, s0=0.1)` (see
[Particle losses](../package.md#particle-losses)). For a lost particle,
`zeta_end` and `theta_end` give where it left the plasma; the
[heat-flux benchmark](../package.md#heat-flux) takes these as its strike point
on the plasma boundary.

## Trajectory fields

Stored in the **trajectory files**, which hold up to 40 configurations each,
with 6,000 orbits per configuration. The orbits have different lengths, so they
are stored in a compressed sparse row (CSR) format: stacked in one array, with
offsets marking where each orbit starts. Unlike the other fields, `traj_data`,
`traj_offsets` and `config_offsets` run over the whole file rather than one
configuration.

```{table}
:class: boss-fields
:width: 100%

| HDF5 name | Symbol | Type | Description |
| --- | --- | --- | --- |
| `traj_data` | – | array `(n_samples, 5)` | All orbit samples in the file, one row per sample. Columns $(t, s, \theta_B, \zeta_B, v_\parallel)$: time [s], normalized toroidal flux, Boozer poloidal and toroidal angles in $[-\pi, \pi)$ [rad], parallel velocity [m/s]. |
| `traj_offsets` | – | array `(n_orbits + 1,)` | Orbit `k` is `traj_data[traj_offsets[k]:traj_offsets[k+1]]`. |
| `config_offsets` | – | array `(n_configs + 1,)` | The orbits of configuration `i` are `config_offsets[i]` to `config_offsets[i+1] - 1`. |
| `dt_save` | $\Delta t$ | float | Time between samples, 1 µs [s]. |
| `t_max` | $t_\text{max}$ | float | Maximum simulation time, 1 ms [s]. |
| `tol` | – | float | Relative and absolute tolerance of the adaptive integrator. |
```


## Reading an orbit

```python
import h5py

with h5py.File("trajectory_data_test_split_00000.hdf5", "r") as f:
    i, j = 0, 5                                    # configuration i, its orbit j
    k = f["config_offsets"][i] + j
    a, b = f["traj_offsets"][k], f["traj_offsets"][k + 1]
    t, s, theta, zeta, vpar = f["traj_data"][a:b].T
```

{func}`~boss_bench.trajectory.load_trajectory` reads one orbit, and
{func}`~boss_bench.trajectory.read_trajectories` all orbits of a
configuration at once; see [Loading trajectory data](../tutorials/loading-trajectories.md).
