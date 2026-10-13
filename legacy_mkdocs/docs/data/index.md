# Data documentation

BoSS stores stellarator **configurations** together with the results of
**simulations** run on them. Each is documented on its own page:

<div class="grid cards" markdown>

-   :material-shape-outline: **[Configuration fields](configurations.md)**

    ---

    Geometry, magnetic field, equilibrium profiles, and figures of merit.
    These fields appear in every file.

-   :material-atom-variant: **[Fast-ion confinement](fast-ion.md)**

    ---

    The alpha-particle simulation: its setup, the particle fields in the
    confinement files, and the orbits in the trajectory files.

</div>

## File layout

Each HDF5 file holds a set of stellarator configurations. Every field is a
top-level dataset whose first axis runs over configurations, so row `i` of
every dataset belongs to the same configuration. The `uuid` field
identifies a configuration across all files. Field tables list shapes
**per configuration**.

All quantities are in SI units (m, T, Wb, Pa, A, s, m/s), and angles are in
radians unless noted.

## Grids and array shapes

Gridded fields use 15 radial points (`s1d`), 41 toroidal angles over one
field period (`phi1d`), and 41 poloidal angles (`theta1d`). They are stored
flattened in C order:

```python
modB = f["modB"][i].reshape(15, 41, 41)         # [s, phi, theta]
surf = f["surf_xyz"][i].reshape(41, 41, 3)      # [phi, theta, xyz]
axis = f["xyz_axis"][i].reshape(41, 3)          # [phi, xyz]
```

## Boundary Fourier modes

`surf_full_res_fourier_modes` describes the boundary as a
stellarator-symmetric series, in SIMSOPT `SurfaceRZFourier` order:

\[
R(\theta, \phi) = \sum_{m,n} R_{mn} \cos(m\theta - n\,n_\text{fp}\,\phi), \qquad
Z(\theta, \phi) = \sum_{m,n} Z_{mn} \sin(m\theta - n\,n_\text{fp}\,\phi).
\]

The vector is \([R_{mn}]\) followed by \([Z_{mn}]\). For \(R_{mn}\), \(m = 0\)
runs over \(n = 0, \dots, 20\), and each \(m = 1, \dots, 20\) runs over
\(n = -20, \dots, 20\), giving 841 terms. \(Z_{mn}\) has the same layout
without \(Z_{00}\), giving 840 terms.
