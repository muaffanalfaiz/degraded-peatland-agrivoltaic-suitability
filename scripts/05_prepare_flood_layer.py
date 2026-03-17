"""05_prepare_flood_layer

Normalize the flood-vulnerability raster to a 0-1 benefit scale where lower flood
vulnerability scores higher.

Required config inputs:
- flood_raster
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

    inputs = require_inputs(config, ["flood_raster"])
    analysis_mask = dataset_name(paths["geodatabase"], config["outputs"]["analysis_mask_raster"])
    if not arcpy.Exists(analysis_mask):
        raise FileNotFoundError("Run 01_prepare_study_area.py first.")

    flood_score = dataset_name(paths["geodatabase"], config["outputs"]["flood_score"])
    set_env(config, snap_raster=analysis_mask, mask_raster=analysis_mask)

    projected = dataset_name(paths["geodatabase"], "flood_raster_projected")
    arcpy.management.ProjectRaster(
        str(inputs["flood_raster"]),
        projected,
        arcpy.SpatialReference(config["projection_epsg"]),
        cell_size=config["cell_size"],
    )

    normalize_raster(projected, flood_score, benefit=False, mask_raster=analysis_mask)

    print("Flood-vulnerability score complete")
    print(f"Score raster: {flood_score}")


if __name__ == "__main__":
    main()
