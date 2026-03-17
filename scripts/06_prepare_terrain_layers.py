"""06_prepare_terrain_layers

Create terrain-based score rasters from the DEM:
- slope: lower slope is more suitable
- aspect: closer to preferred aspect azimuth is more suitable
- TPI: values closer to zero are more suitable

Required config inputs:
- dem
"""

from __future__ import annotations

from _helpers import (
    dataset_name,
    ensure_arcpy,
    ensure_file_gdb,
    get_workspace_paths,
    load_config,
    normalize_by_distance_to_target,
    normalize_raster,
    require_inputs,
    set_env,
)
import arcpy


def main() -> None:
    ensure_arcpy()
    arcpy.CheckOutExtension("Spatial")

    config = load_config()
    paths = get_workspace_paths(config)
    ensure_file_gdb(paths["geodatabase"])

    inputs = require_inputs(config, ["dem"])
    analysis_mask = dataset_name(paths["geodatabase"], config["outputs"]["analysis_mask_raster"])
    if not arcpy.Exists(analysis_mask):
        raise FileNotFoundError("Run 01_prepare_study_area.py first.")

    set_env(config, snap_raster=analysis_mask, mask_raster=analysis_mask)

    dem_projected = dataset_name(paths["geodatabase"], "dem_projected")
    slope_raw = dataset_name(paths["geodatabase"], "slope_raw")
    aspect_raw = dataset_name(paths["geodatabase"], "aspect_raw")
    tpi_raw = dataset_name(paths["geodatabase"], "tpi_raw")

    slope_score = dataset_name(paths["geodatabase"], config["outputs"]["slope_score"])
    aspect_score = dataset_name(paths["geodatabase"], config["outputs"]["aspect_score"])
    tpi_score = dataset_name(paths["geodatabase"], config["outputs"]["tpi_score"])

    arcpy.management.ProjectRaster(
        str(inputs["dem"]),
        dem_projected,
        arcpy.SpatialReference(config["projection_epsg"]),
        cell_size=config["cell_size"],
    )

    slope = arcpy.sa.Slope(dem_projected, output_measurement="DEGREE")
    slope.save(slope_raw)

    aspect = arcpy.sa.Aspect(dem_projected)
    aspect.save(aspect_raw)

    tpi = arcpy.sa.Minus(
        arcpy.sa.FocalStatistics(dem_projected, arcpy.sa.NbrRectangle(3, 3, "CELL"), "MEAN"),
        arcpy.sa.Raster(dem_projected),
    )
    tpi.save(tpi_raw)

    normalize_raster(slope_raw, slope_score, benefit=False, mask_raster=analysis_mask)
    normalize_by_distance_to_target(
        aspect_raw,
        aspect_score,
        target_value=float(config.get("preferred_aspect_degrees", 0)),
        mask_raster=analysis_mask,
    )
    normalize_by_distance_to_target(tpi_raw, tpi_score, target_value=0.0, mask_raster=analysis_mask)

    print("Terrain score rasters complete")
    print(f"Slope score : {slope_score}")
    print(f"Aspect score: {aspect_score}")
    print(f"TPI score   : {tpi_score}")


if __name__ == "__main__":
    main()
