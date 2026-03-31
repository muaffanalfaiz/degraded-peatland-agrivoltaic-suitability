# Data

Spatial datasets produced by the agrivoltaic suitability analysis.

## Structure

```
data/
├── final/                        Primary analysis output
│   ├── final_suitability.tif     Final weighted overlay raster (4-class)
│   └── final_vectors.gdb/        Study area, peatlands, WDPA layers
└── criteria_optional/            Reclassified input criterion rasters
    ├── fire_hazard_sumsel.tif
    ├── peat_depth_reclass.tif
    ├── flood_reclass.tif
    ├── slope_reclass.tif
    ├── road_distance_reclass.tif
    ├── aspect_reclass.tif
    ├── tpi_reclass.tif
    └── ghi_reclass.tif
```

## final/

`final_suitability.tif` is the primary output. It represents the weighted
overlay result after hard-constraint exclusions (protected areas, non-peat
land cover), classified into four levels: Very Low, Low, Moderately
Suitable, and Highly Suitable.

`final_vectors.gdb` contains the study area boundary, peatland extent
mask, and WDPA protected area layer used as spatial context in the ArcGIS
Pro project.

## criteria_optional/

The eight reclassified criterion rasters as exported from the original
ArcGIS Pro workflow. These are provided as visual reference exports. Input
datasets were processed at different native resolutions and projections
before resampling to the common 30 m analysis grid; they are not intended
as a standalone overlay stack independent of the original workflow.

## Coordinate system

`final_suitability.tif` — Indonesian 1974 / UTM Zone 48S (EPSG:23888),
30 m resolution.

## Source data

Full source dataset details are in `../docs/data_sources.md`.
