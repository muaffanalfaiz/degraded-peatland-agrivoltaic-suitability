# Data folder

This repository does not include the full original working datasets used during analysis.

## What is included

- `rasters/final_suitability_30m.tif` — the final public suitability raster intended for viewing, download, and portfolio demonstration
- `example_inputs/` — placeholder paths and filenames referenced by the public template configuration file

## What is not included

The following are not distributed in this repository:

- full raw source datasets
- intermediate scratch rasters
- temporary processing outputs
- institutional or third-party datasets with uncertain redistribution status
- manuscript files

## How to interpret the code

The scripts in this repository reflect the project workflow in ArcPy form. They are intended to document the structure of the analysis and provide a reusable template for adaptation.

Users who want to adapt the workflow should replace the example paths in `config/project_config.json` with their own local datasets.

## Suggested input types

Typical inputs expected by the scripts include:

- study area boundary
- degraded peat polygons
- protected areas
- roads
- DEM raster
- GHI raster
- peat-depth or peat-condition raster
- flood vulnerability raster
- hotspot point layer with an FRP field