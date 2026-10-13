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

## Confinement Data

The **confinement files** hold the start and end state of every traced
particle: 15,000 alpha particles per configuration, and up to 3,000
configurations per file, along with the [Ideal MHD](ideal-mhd.md) fields of
each configuration. They are enough to compute loss fractions, lost energy and
heat fluxes.

A particle is lost if its confinement time is shorter than the simulation
time, $t_\text{loss} < t_\text{max}$. Loss quantities are computed over the
particles born on one surface; for example, the loss fraction of the particles
born on $s = 0.1$ is `bb.loss_fraction(confinement_time, t_max, s_init, s0=0.1)`
(see [Particle losses](../package.md#particle-losses)). For a lost particle,
`zeta_end` and `theta_end` give where it left the plasma; the
[heat-flux benchmark](../package.md#heat-flux) takes these as its strike point
on the plasma boundary.

```{table}
:class: boss-fields
:width: 100%

| HDF5 name | Symbol | Type | Description |
| --- | --- | --- | --- |
| `confinement_time` | $t_\text{loss}$ | array `(15000,)` | Time at which the particle was lost, i.e. reached $s = 0.98$ [s]. Equals `t_max` if it was never lost. |
| `s_init` | $s_0$ | array `(15000,)` | Birth surface, $s_0 \in \{0.1, 0.25, 0.5\}$. |
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

## Trajectory Data

The **trajectory files** hold the full guiding-center orbits of 6,000
particles per configuration, sampled every 1 µs for the first 1 ms, for up to
40 configurations per file, along with the [Ideal MHD](ideal-mhd.md) fields of
each configuration. They are meant for work on particle motion itself. The
samples of an orbit are regularly spaced, 1 µs apart, unless the particle is
lost: its trajectory then ends with one last sample at the time it was lost.

The orbits are stored in a **compressed sparse row (CSR) format**. Orbits have
different lengths, because a lost particle stops early, so all samples of all
orbits in a file are stacked in one array, `traj_data`, and two offset arrays
mark where each orbit and each configuration starts. Unlike the other fields,
`traj_data`, `traj_offsets` and `config_offsets` run over the whole file
rather than one configuration. {func}`~boss_bench.trajectory.load_trajectory`
reads one orbit, and {func}`~boss_bench.trajectory.read_trajectories` all orbits
of a configuration; see [Loading trajectory data](../tutorials/loading-trajectories.md).

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
