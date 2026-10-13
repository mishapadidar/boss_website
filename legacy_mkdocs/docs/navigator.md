---
hide:
  - toc
---

# Navigator

The BoSS Navigator is a web app for browsing the **latest** database one
record at a time. You can filter configurations by their properties, look at
the boundary surface in 3-D, plot the radial profiles and \(|B|\), check
alpha-particle loss statistics, and download a single record. It works like the
[QUASR navigator](https://quasr.flatironinstitute.org/).

!!! note "Coming soon"
    The Navigator is under construction. This page will link to it once it
    is live.

<div class="grid cards" markdown>

-   :material-filter-variant: **Search and filter**

    ---

    Narrow configurations down by source database, number of field periods,
    aspect ratio, \(\beta\), loss fraction, and more.

-   :material-rotate-3d-variant: **Inspect a configuration**

    ---

    Rotate the plasma boundary in 3-D, colored by \(|B|\), and look through
    its profiles and scalar properties.

-   :material-download: **Download one record**

    ---

    Get a single configuration without downloading the whole database.
    Records are identified by `uuid`.

</div>

!!! info "Navigator vs. downloads"
    The Navigator shows the **latest** database, which keeps growing. To work
    with the data in bulk, see [Download](download.md).
