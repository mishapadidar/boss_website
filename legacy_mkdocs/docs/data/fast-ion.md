# Fast-ion confinement

For every configuration, BoSS follows 15,000 fusion-born alpha particles
and records whether each one is confined or lost. This is the first
simulation type in the database.

## Simulation setup

| | |
| --- | --- |
| **Code** | [CATAPULT](https://arxiv.org/abs/2604.07617), the GPU guiding-center timestepper in [FIRM3D](https://github.com/ColumbiaStellaratorTheory/firm3d) |
| **Physics** | Collisionless guiding-center motion in Boozer coordinates |
| **Particles** | 15,000 alpha particles per configuration, 3.5 MeV (\(v \approx 1.3 \times 10^{7}\) m/s) |
| **Birth surfaces** | 5,000 particles on each of \(s = 0.1\), \(0.25\), and \(0.5\) |
| **Birth distribution** | Uniform over the flux surface; isotropic in velocity, so \(v_\parallel\) is uniform on \([-v, v]\) |
| **Loss condition** | The particle reaches the plasma boundary \(s = 1\) |
| **Duration** | Until the particle is lost or \(t_\text{max} = 0.1\) s (`t_max`) |
| **Machine size** | Each configuration is scaled to a randomly chosen reactor size and field strength |

## Particle fields

Stored in the **confinement files**, with one entry per alpha particle
and 15,000 particles per configuration.

<div class="field-table" markdown>

| HDF5 name | Symbol | Description |
| --- | --- | --- |
| `confinement_time` | \(t_\text{loss}\) | Time at which the particle reached the boundary [s]. Equals `t_max` if it was never lost. Shape `(15000,)`. |
| `s_init` | \(s_0\) | Birth surface (0.1, 0.25, or 0.5). Shape `(15000,)`. |
| `t_init` | \(\theta_{B,0}\) | Initial Boozer poloidal angle [rad]. Shape `(15000,)`. |
| `z_init` | \(\zeta_{B,0}\) | Initial Boozer toroidal angle [rad]. Shape `(15000,)`. |
| `vpar_init` | \(v_{\parallel,0}\) | Initial parallel velocity [m/s]. Shape `(15000,)`. |
| `s_end` | \(s_\text{end}\) | Normalized toroidal flux when the simulation stopped. Shape `(15000,)`. |
| `t_end` | \(\theta_{B,\text{end}}\) | Final Boozer poloidal angle, wrapped to \((-\pi, \pi]\) [rad]. Shape `(15000,)`. |
| `z_end` | \(\zeta_{B,\text{end}}\) | Final Boozer toroidal angle, not wrapped [rad]. Shape `(15000,)`. |
| `vpar_end` | \(v_{\parallel,\text{end}}\) | Final parallel velocity [m/s]. Shape `(15000,)`. |
| `t_max` | \(t_\text{max}\) | Maximum simulation time [s]. |
| `tol` | – | Integrator tolerance. |

</div>

The loss fraction is `(confinement_time < t_max).mean()`.

## Trajectory fields

Stored in the **trajectory files**, which hold 40 configurations each, with 6,000 orbits per
configuration. The orbits are stored stacked in one array, and offsets mark
where each orbit starts.

<div class="field-table" markdown>

| HDF5 name | Symbol | Description |
| --- | --- | --- |
| `traj_data` | \((t, s, \theta_B, \zeta_B, v_\parallel)\) | All orbit samples in the file, one row per sample. Shape `(n_samples, 5)`. Columns: time [s], normalized flux, Boozer poloidal angle [rad], Boozer toroidal angle [rad], parallel velocity [m/s]. |
| `traj_offsets` | – | Orbit `k` is `traj_data[traj_offsets[k]:traj_offsets[k+1]]`. Shape `(n_orbits + 1,)`, over the whole file. |
| `config_offsets` | – | The orbits of configuration `i` are `config_offsets[i]` to `config_offsets[i+1] - 1`. Shape `(41,)`, over the whole file. |

</div>

## Reading an orbit

```python
import h5py

with h5py.File("trajectory_data_test_split_00000.hdf5", "r") as f:
    i, j = 0, 5                                    # configuration i, its orbit j
    k = f["config_offsets"][i] + j
    a, b = f["traj_offsets"][k], f["traj_offsets"][k + 1]
    t, s, theta, zeta, vpar = f["traj_data"][a:b].T
```
