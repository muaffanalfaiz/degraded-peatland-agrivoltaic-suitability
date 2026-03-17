# Scripts roadmap

This folder is a **reproducibility scaffold** for rebuilding the ArcGIS Pro workflow into ArcPy modules.

## Important note
These scripts are templates and placeholders.  
They are intentionally not wired to your local paths yet.

## Planned script flow

1. `00_env_setup.py`
   - ArcGIS environment settings
   - projection
   - cell size
   - snap raster
   - mask
   - workspace variables

2. `01_prepare_study_area.py`
   - South Sumatra boundary
   - peatland subset
   - degraded peat mask
   - analysis extent

3. `02_prepare_constraints.py`
   - WDPA and other excluded zones
   - rasterized hard constraint mask

4. `03_prepare_fire_risk.py`
   - FIRMS / FRP preprocessing
   - KDE surface
   - normalized fire-risk raster

5. `04_prepare_peat_layer.py`
   - peat-depth or peat proxy preparation
   - scoring and normalization

6. `05_prepare_flood_layer.py`
   - flood vulnerability layer prep
   - scoring and normalization

7. `06_prepare_terrain_layers.py`
   - DEM preprocessing
   - slope
   - aspect
   - TPI
   - scoring

8. `07_prepare_accessibility_layer.py`
   - road preprocessing
   - Euclidean distance
   - accessibility scoring

9. `08_prepare_ghi_layer.py`
   - GHI prep
   - scoring / normalization

10. `09_weighted_overlay.py`
    - apply weights
    - combine layers
    - classify output

11. `10_postprocess_statistics.py`
    - class areas
    - patch counts
    - summary outputs

12. `11_export_maps.py`
    - export outputs
    - save figures and tables

## Suggested next step
Replace placeholders one module at a time, starting with:
- `00_env_setup.py`
- `01_prepare_study_area.py`
- `09_weighted_overlay.py`
