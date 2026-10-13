# Configuration fields

These fields describe each stellarator configuration and are present in
every file. Shapes are per configuration. See
[grids and array shapes](index.md#grids-and-array-shapes) for how to reshape
the arrays.

## Identifiers

<div class="field-table" markdown>

| HDF5 name | Symbol | Description |
| --- | --- | --- |
| `uuid` | – | Unique identifier of the configuration. It is the same in every file. |
| `database_from` | – | Source collection the configuration came from, e.g. `quasr`, `constellaration`. |
| `database_from_ID` | – | Identifier of the configuration in its source collection. |
| `timestamp` | – | When the record was computed. |

</div>

## Geometry

<div class="field-table" markdown>

| HDF5 name | Symbol | Description |
| --- | --- | --- |
| `nfp` | \(n_\text{fp}\) | Number of field periods. |
| `stellsym` | – | Whether the configuration is stellarator-symmetric. |
| `major_radius` | \(R_0\) | Major radius of the plasma boundary [m]. |
| `minor_radius` | \(a\) | Effective minor radius of the plasma boundary [m]. |
| `aspect_ratio` | \(A = R_0 / a\) | Aspect ratio. |
| `volume` | \(V\) | Plasma volume [m³]. The sign follows the surface orientation, so use \(\lvert V \rvert\). |
| `surf_full_res_fourier_modes` | \(R_{mn},\ Z_{mn}\) | Fourier coefficients of the plasma boundary [m], zero-padded to `mpol = ntor = 20`. Shape `(1681,)`. See [boundary Fourier modes](index.md#boundary-fourier-modes). |
| `surf_full_res_mpol`, `surf_full_res_ntor` | \(M,\ N\) | Resolution of `surf_full_res_fourier_modes` (always 20). |
| `surf_mpol`, `surf_ntor` | – | Resolution of the boundary in its original representation. |
| `surf_xyz` | \(\mathbf{x}(\phi, \theta)\) | Cartesian points on the plasma boundary over one field period [m]. Shape `(5043,)` → `(41, 41, 3)`, indexed \((\phi, \theta, xyz)\). |
| `surf_quadpoints_phi` | \(\phi\) | Toroidal angles of `surf_xyz`, in turns, \([0, 1/n_\text{fp})\). Shape `(41,)`. |
| `surf_quadpoints_theta` | \(\theta\) | Poloidal angles of `surf_xyz`, in turns, \([0, 1)\). Shape `(41,)`. |
| `xyz_axis` | \(\mathbf{r}_\text{axis}(\phi)\) | Cartesian points on the magnetic axis over one field period [m], at the angles `surf_quadpoints_phi`. Shape `(123,)` → `(41, 3)`. |
| `axis_helicity` | – | Helicity of the magnetic axis. |
| `integrated_axis_torsion` | \(\int \tau \, d\ell\) | Torsion of the magnetic axis, integrated along its length. |

</div>

## Magnetic field

<div class="field-table" markdown>

| HDF5 name | Symbol | Description |
| --- | --- | --- |
| `s1d` | \(s\) | Normalized toroidal flux of the radial grid, from \(10^{-4}\) to 1 (\(s = 1\) is the boundary). Shape `(15,)`. |
| `theta1d` | \(\theta\) | Poloidal angle grid, \([0, 2\pi)\). Shape `(41,)`. |
| `phi1d` | \(\phi\) | Toroidal angle grid over one field period, \([0, 2\pi/n_\text{fp})\). Shape `(41,)`. |
| `modB` | \(\lvert B \rvert(s, \phi, \theta)\) | Magnetic field strength on the grid, in VMEC angles [T]. Shape `(25215,)` → `(15, 41, 41)`. |
| `modB_boozer` | \(\lvert B \rvert(s, \zeta_B, \theta_B)\) | Magnetic field strength on the grid, in Boozer angles [T]. Shape `(25215,)` → `(15, 41, 41)`. |
| `R_boozer` | \(R(s, \zeta_B, \theta_B)\) | Cylindrical radius of the Boozer grid points [m]. Shape `(25215,)` → `(15, 41, 41)`. |
| `Z_boozer` | \(Z(s, \zeta_B, \theta_B)\) | Cylindrical height of the Boozer grid points [m]. Shape `(25215,)` → `(15, 41, 41)`. |
| `nu_boozer` | \(\nu(s, \zeta_B, \theta_B)\) | Difference between the Boozer and cylindrical toroidal angles [rad]. Shape `(25215,)` → `(15, 41, 41)`. |
| `max_modB` | \(B_\text{max}\) | Maximum field strength [T]. |
| `min_modB` | \(B_\text{min}\) | Minimum field strength [T]. |
| `mirror_ratio` | \(B_\text{max} / B_\text{min}\) | Mirror ratio. |
| `volavgB` | \(\langle B \rangle\) | Volume-averaged field strength [T]. |
| `min_L_grad_B` | \(\min L_{\nabla B}\) | Minimum magnetic gradient scale length on the boundary [m]. |
| `phiedge` | \(\Phi_\text{edge}\) | Toroidal flux enclosed by the boundary [Wb]. |

</div>

## Equilibrium profiles

Profiles are sampled on the 15 radial points of `s1d`.

<div class="field-table" markdown>

| HDF5 name | Symbol | Description |
| --- | --- | --- |
| `enforce_vacuum` | – | `True` for vacuum equilibria (\(\beta = 0\)). |
| `plasma_beta` | \(\langle \beta \rangle\) | Volume-averaged plasma beta. |
| `pressure` | \(p(s)\) | Pressure profile [Pa]. Shape `(15,)`. |
| `d_pressure_d_s` | \(dp/ds\) | Radial derivative of the pressure [Pa]. Shape `(15,)`. |
| `iota` | \(\iota(s)\) | Rotational transform. Shape `(15,)`. |
| `current` | \(I_\text{tor}(s)\) | Toroidal current profile [A]. Shape `(15,)`. |
| `jdotb_vmec` | \(\langle \mathbf{J} \cdot \mathbf{B} \rangle\) | Flux-surface-averaged parallel current from VMEC [T·A/m²]. Shape `(15,)`. |
| `boozer_G` | \(G(s)\) | Boozer covariant toroidal field component [T·m]. Shape `(15,)`. |
| `boozer_I` | \(I(s)\) | Boozer covariant poloidal field component [T·m]. Shape `(15,)`. |
| `vacuum_well` | \(W\) | Magnetic well depth. Positive values mean a magnetic well, which is favorable. |
| `mercier_criterion` | \(D_\text{Merc}(s)\) | Mercier stability criterion. Positive values mean stable. Shape `(15,)`. |

</div>

## Confinement proxies

<div class="field-table" markdown>

| HDF5 name | Symbol | Description |
| --- | --- | --- |
| `epsilon_eff` | \(\epsilon_\text{eff}(s)\) | Effective helical ripple (\(1/\nu\) transport proxy). Shape `(15,)`. |
| `sqrt_boozer_qs_error` | \(\sqrt{f_\text{QS}}(s)\) | Square root of the Boozer quasi-symmetry residual. Shape `(15,)`. |
| `qi_error` | \(f_\text{QI}(s)\) | Quasi-isodynamicity residual. Shape `(15,)`. |

</div>

## VMEC settings

Solver settings used to compute each equilibrium.

<div class="field-table" markdown>

| HDF5 name | Symbol | Description |
| --- | --- | --- |
| `vmec_mpol`, `vmec_ntor` | – | Poloidal and toroidal Fourier resolution. |
| `vmec_ntheta`, `vmec_nzeta` | – | Real-space poloidal and toroidal grid sizes. |
| `vmec_ns_array` | – | Radial resolution at each multigrid stage. Shape `(10,)`. |
| `vmec_niter_array` | – | Maximum iterations at each stage. Shape `(10,)`. |
| `vmec_ftol_array` | – | Force-residual tolerance at each stage. Shape `(10,)`. |
| `vmec_delt` | – | Solver time step. |
| `vmec_ncurr` | – | `0` = prescribed \(\iota\) profile, `1` = prescribed current profile. |
| `vmec_signgs` | – | Sign of the Jacobian. |

</div>
