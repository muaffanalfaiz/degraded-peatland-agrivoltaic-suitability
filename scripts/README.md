# Scripts

These ArcPy scripts reconstruct the GIS–MCDA workflow used for the agrivoltaic suitability analysis.

## Main design choices
- ArcGIS Pro / ArcPy workflow
- 30 m grid
- UTM Zone 48S
- published AHP weights already embedded in `config/project_config.json`
- only the final classified GeoTIFF is intended to be tracked publicly in GitHub

## Files
- `00_env_setup.py` — prepare local workspace and validate config
- `01_prepare_study_area.py` — create study area and degraded-peat analysis mask
- `02_prepare_constraints.py` — build hard-constraint mask from protected areas
- `03_prepare_fire_risk.py` — FRP-weighted fire kernel density and normalization
- `04_prepare_peat_layer.py` — normalize peat-depth / geotechnical proxy
- `05_prepare_flood_layer.py` — normalize flood-vulnerability raster
- `06_prepare_terrain_layers.py` — derive slope, aspect, and TPI scores from DEM
- `07_prepare_accessibility_layer.py` — derive road-distance score
- `08_prepare_ghi_layer.py` — normalize GHI raster
- `09_weighted_overlay.py` — weighted linear combination and final class raster
- `10_postprocess_statistics.py` — export class statistics to CSV
- `11_export_maps.py` — export the final classified GeoTIFF for GitHub
- `run_pipeline.py` — convenience runner for the full pipeline
- `_helpers.py` — shared utility functions

## Important
These scripts are designed to be real workflow code, but they still expect your local source data paths to be filled in inside `config/project_config.json`.
