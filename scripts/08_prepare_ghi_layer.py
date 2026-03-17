"""08_prepare_ghi_layer

Normalize the GHI raster to a 0-1 benefit scale where higher irradiance is more suitable.

Required config inputs:
- ghi_raster
"""

from __future__ import annotations

from _helpers import (
    dataset_name,
    ensure_arcpy,
    ensure_file_gdb,
    get_workspace_paths,
    load_config,
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

    inputs = require_inputs(config, ["ghi_raster"])
    analysis_mask = dataset_name(paths["geodatabase"], config["outputs"]["analysis_mask_raster"])
    if not arcpy.Exists(analysis_mask):
        raise FileNotFoundError("Run 01_prepare_study_area.py first.")

    ghi_score = dataset_name(paths["geodatabase"], config["outputs"]["ghi_score"])
    set_env(config, snap_raster=analysis_mask, mask_raster=analysis_mask)

    projected = dataset_name(paths["geodatabase"], "ghi_projected")
    arcpy.management.ProjectRaster(
        str(inputs["ghi_raster"]),
        projected,
        arcpy.SpatialReference(config["projection_epsg"]),
        cell_size=config["cell_size"],
    )

    normalize_raster(projected, ghi_score, benefit=True, mask_raster=analysis_mask)

    print("GHI score complete")
    print(f"Score raster: {ghi_score}")


if __name__ == "__main__":
    main()
