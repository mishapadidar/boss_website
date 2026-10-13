# Ideal MHD

These fields describe the quantities used to compute the ideal MHD
equilibria, or quantities derived from the equilibria. For quantities
describing fast-ion confinement, see [Fast-ion confinement](fast-ion.md).

## File layout

Each HDF5 file holds a set of stellarator configurations. Every field is a
top-level dataset whose first axis runs over configurations, so row `i` of
every dataset belongs to the same configuration. The `uuid` field
identifies a configuration across all files. Field tables list types and
shapes **per configuration**.

All quantities are in SI units (m, T, Wb, Pa, A, s, m/s), and angles are in
radians unless noted. Every dataset also carries a short `description` and its
`units` as HDF5 attributes, e.g. `f["modB"].attrs["units"]`.

## Grids and array shapes

Gridded fields use 15 radial points (`s1d`), 41 toroidal angles over one
field period (`phi1d`), and 41 poloidal angles (`theta1d`). They are stored
flattened in C order:

```python
modB = f["modB"][i].reshape(15, 41, 41)             # [s, phi, theta]
boundary = f["boundary_xyz"][i].reshape(41, 41, 3)   # [phi, theta, xyz]
axis = f["xyz_axis"][i].reshape(41, 3)              # [phi, xyz]
```

## Identifiers

```{table}
:class: boss-fields
:width: 100%

| HDF5 name | Symbol | Type | Description |
| --- | --- | --- | --- |
| `uuid` | – | str | Unique identifier of the configuration. It is the same in every file. |
| `source_dataset` | – | str | Source dataset the configuration came from, e.g. `quasr`, `constellaration`. See [Sources](overview.md#sources). |
| `source_id` | – | str | Identifier of the configuration in its source dataset. |
| `timestamp` | – | str | When the particle tracing was run. |
```


## Geometry

`boundary_full_res_fourier_modes` describes the boundary as a Fourier
series, stellarator-symmetric and in SIMSOPT `SurfaceRZFourier` order:

$$
R(\theta, \phi) = \sum_{m,n} R_{mn} \cos(m\theta - n\,n_\text{fp}\,\phi), \qquad
Z(\theta, \phi) = \sum_{m,n} Z_{mn} \sin(m\theta - n\,n_\text{fp}\,\phi).
$$

The vector is $[R_{mn}]$ followed by $[Z_{mn}]$. For $R_{mn}$, $m = 0$
runs over $n = 0, \dots, 20$, and each $m = 1, \dots, 20$ runs over
$n = -20, \dots, 20$, giving 841 terms. $Z_{mn}$ has the same layout
without $Z_{00}$, giving 840 terms.

```{table}
:class: boss-fields
:width: 100%

| HDF5 name | Symbol | Type | Description |
| --- | --- | --- | --- |
| `boundary_full_res_fourier_modes` | $R_{mn},\ Z_{mn}$ | array `(1681,)` | Fourier coefficients of the plasma boundary [m], zero-padded to `mpol = ntor = 20`, as described above. |
| `boundary_full_res_mpol`, `boundary_full_res_ntor` | $M,\ N$ | int | Resolution of `boundary_full_res_fourier_modes` (always 20). |
| `boundary_mpol`, `boundary_ntor` | – | int | Resolution of the boundary in its original representation. |
| `boundary_xyz` | $\mathbf{x}(\phi, \theta)$ | array `(5043,)` | Cartesian points on the plasma boundary over one field period [m]. Reshape to `(41, 41, 3)`, indexed $(\phi, \theta, xyz)$. |
| `boundary_quadpoints_phi` | $\phi$ | array `(41,)` | Toroidal angles of `boundary_xyz`, in turns, $[0, 1/n_\text{fp})$. |
| `boundary_quadpoints_theta` | $\theta$ | array `(41,)` | Poloidal angles of `boundary_xyz`, in turns, $[0, 1)$. |
| `nfp` | $n_\text{fp}$ | int | Number of field periods. |
| `stellsym` | – | bool | Whether the configuration is stellarator-symmetric. |
| `major_radius` | $R_0$ | float | Major radius of the plasma boundary [m]. |
| `minor_radius` | $a$ | float | Effective minor radius of the plasma boundary [m]. |
| `aspect_ratio` | $A = R_0 / a$ | float | Aspect ratio. |
| `volume` | $V$ | float | Plasma volume [m³]. |
| `xyz_axis` | $\mathbf{r}_\text{axis}(\phi)$ | array `(123,)` | Cartesian points on the magnetic axis over one field period [m], at the angles `boundary_quadpoints_phi`. Reshape to `(41, 3)`. |
| `axis_helicity` | – | int | Helicity of the magnetic axis. |
| `integrated_axis_torsion` | $\int \tau \, d\ell$ | float | Torsion of the magnetic axis, integrated along its length over one field period. |
```


## Magnetic field

```{table}
:class: boss-fields
:width: 100%

| HDF5 name | Symbol | Type | Description |
| --- | --- | --- | --- |
| `s1d` | $s$ | array `(15,)` | Normalized toroidal flux of the radial grid: 15 linearly spaced values from $10^{-4}$ to 1 ($s = 1$ is the boundary). |
| `theta1d` | $\theta$ | array `(41,)` | Poloidal angle grid, $[0, 2\pi)$. |
| `phi1d` | $\phi$ | array `(41,)` | Toroidal angle grid over one field period, $[0, 2\pi/n_\text{fp})$. |
| `modB` | $\lvert B \rvert(s, \phi, \theta)$ | array `(25215,)` | Magnetic field strength on the grid, in VMEC angles [T]. Reshape to `(15, 41, 41)`. |
| `modB_boozer` | $\lvert B \rvert(s, \zeta_B, \theta_B)$ | array `(25215,)` | Magnetic field strength on the grid, in Boozer angles [T]. Reshape to `(15, 41, 41)`. |
| `R_boozer` | $R(s, \zeta_B, \theta_B)$ | array `(25215,)` | Cylindrical radius of the Boozer grid points [m]. Reshape to `(15, 41, 41)`. |
| `Z_boozer` | $Z(s, \zeta_B, \theta_B)$ | array `(25215,)` | Cylindrical height of the Boozer grid points [m]. Reshape to `(15, 41, 41)`. |
| `nu_boozer` | $\nu(s, \zeta_B, \theta_B)$ | array `(25215,)` | Difference $\nu = \zeta_B - \phi$ between the Boozer and cylindrical toroidal angles [rad], so the cylindrical angle of a point is $\phi = \zeta_B - \nu$. Reshape to `(15, 41, 41)`. |
| `max_modB` | $B_\text{max}$ | float | Maximum field strength [T]. |
| `min_modB` | $B_\text{min}$ | float | Minimum field strength [T]. |
| `mirror_ratio` | $B_\text{max} / B_\text{min}$ | float | Mirror ratio. |
| `volume_avg_modB` | $\langle B \rangle$ | float | Volume-averaged field strength [T]. |
| `min_L_grad_B` | $\min L_{\nabla B}$ | float | Minimum magnetic gradient scale length on the boundary [m]. |
| `toroidal_flux_edge` | $\Phi_\text{edge}$ | float | Toroidal flux enclosed by the boundary [Wb]. |
```


## Equilibrium profiles

Profiles are sampled on the 15 radial points of `s1d`.

```{table}
:class: boss-fields
:width: 100%

| HDF5 name | Symbol | Type | Description |
| --- | --- | --- | --- |
| `enforce_vacuum` | – | bool | `True` for vacuum equilibria ($\beta = 0$). Their particles are traced with the vacuum guiding-center equations ($I = K = 0$). |
| `plasma_beta` | $\langle \beta \rangle$ | float | Volume-averaged plasma beta. |
| `pressure` | $p(s)$ | array `(15,)` | Pressure profile [Pa]. |
| `d_pressure_d_s` | $dp/ds$ | array `(15,)` | Radial derivative of the pressure [Pa]. |
| `iota` | $\iota(s)$ | array `(15,)` | Rotational transform. |
| `toroidal_current` | $I_\text{tor}(s)$ | array `(15,)` | Enclosed toroidal current profile [A]. |
| `jdotb_vmec` | $\langle \mathbf{J} \cdot \mathbf{B} \rangle$ | array `(15,)` | Flux-surface-averaged parallel current from VMEC [T·A/m²]. |
| `boozer_G` | $G(s)$ | array `(15,)` | Boozer covariant toroidal field component [T·m]. |
| `boozer_I` | $I(s)$ | array `(15,)` | Boozer covariant poloidal field component [T·m]. |
| `vacuum_well` | $W$ | float | Magnetic well depth. Positive values mean a magnetic well, which is favorable. |
| `mercier_criterion` | $D_\text{Merc}(s)$ | array `(15,)` | Mercier stability criterion. Positive values mean stable. |
```


## Quasi-symmetry

```{table}
:class: boss-fields
:width: 100%

| HDF5 name | Symbol | Type | Description |
| --- | --- | --- | --- |
| `sqrt_boozer_qs_error` | $\sqrt{f_\text{QS}}(s)$ | array `(15,)` | Quasi-symmetry error: the root-sum-square of the Boozer $\lvert B \rvert$ modes that break quasi-symmetry with helicity (1, `axis_helicity`), divided by that of the symmetric modes. |
```


## VMEC settings

Solver settings used to compute each equilibrium.

```{table}
:class: boss-fields
:width: 100%

| HDF5 name | Symbol | Type | Description |
| --- | --- | --- | --- |
| `vmec_mpol`, `vmec_ntor` | – | int | Poloidal and toroidal Fourier resolution. |
| `vmec_ntheta`, `vmec_nzeta` | – | int | Real-space poloidal and toroidal grid sizes. |
| `vmec_ns_array` | – | array `(10,)` | Radial resolution at each multigrid stage. |
| `vmec_niter_array` | – | array `(10,)` | Maximum iterations at each stage. |
| `vmec_ftol_array` | – | array `(10,)` | Force-residual tolerance at each stage. |
| `vmec_delt` | – | float | Solver time step. |
| `vmec_ncurr` | – | int | `0` = prescribed $\iota$ profile, `1` = prescribed current profile. |
| `vmec_signgs` | – | int | Sign of the Jacobian. |
```
