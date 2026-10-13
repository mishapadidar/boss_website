# Data Explorer

The BoSS Data Explorer is a web app for browsing the database one record at a
time. You can filter configurations by their properties, look at
the boundary surface in 3-D, plot the radial profiles and $\lvert B \rvert$,
check alpha-particle loss statistics, and download a single record. It works
like the [QUASR navigator](https://quasr.flatironinstitute.org/).

:::{note}
The Data Explorer is under construction. This page will link to it once it is
live.
:::

::::{grid} 1 1 3 3
:gutter: 3

:::{grid-item-card} Search and filter
Narrow configurations down by source database, number of field periods,
aspect ratio, $\beta$, loss fraction, and more.
:::

:::{grid-item-card} Inspect a configuration
Rotate the plasma boundary in 3-D, colored by $\lvert B \rvert$, and look
through its profiles and scalar properties.
:::

:::{grid-item-card} Download one record
Get a single configuration without downloading the whole database. Records
are identified by `uuid`.
:::
::::

:::{admonition} Data Explorer vs. downloads
:class: info
The Data Explorer is for looking at individual records. To work with the data
in bulk, see [Download Data](download.md).
:::
