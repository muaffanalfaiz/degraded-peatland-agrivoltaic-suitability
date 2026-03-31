# ArcGIS Pro Project

This folder contains the cleaned ArcGIS Pro project file for the degraded
peatland agrivoltaic suitability analysis.

## File

`agrivoltaic_suitability_clean.aprx` — presentation-ready project containing
two maps:

- **Final Suitability Map** — final suitability raster with study area
  boundary, peatland extent, and protected area constraint layers.
- **Criteria Map** — the eight reclassified input criteria used in the
  weighted overlay, provided as an optional reference map.

## Data dependencies

Layers reference datasets in `../data/final/` and
`../data/criteria_optional/`. If layers appear broken after cloning to a
new machine, open the project in ArcGIS Pro and use the Repair Data Source
tool, pointing each layer to the corresponding file in those folders.

## Coordinate system

Indonesian 1974 / UTM Zone 48S (EPSG:23888), 30 m cell size for the final
suitability raster.
