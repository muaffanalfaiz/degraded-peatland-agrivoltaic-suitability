"""04_prepare_peat_layer

Normalize the peat-depth or peat-proxy raster to a 0-1 benefit scale where lower
depth / lower geotechnical constraint scores higher.

Required config inputs:
- peat_raster
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

    inputs = require_inputs(config, ["peat_raster"])
    analysis_mask = dataset_name(paths["geodatabase"], config["outputs"]["analysis_mask_raster"])
    if not arcpy.Exists(analysis_mask):
        raise FileNotFoundError("Run 01_prepare_study_area.py first.")

    peat_score = dataset_name(paths["geodatabase"], config["outputs"]["peat_score"])
    set_env(config, snap_raster=analysis_mask, mask_raster=analysis_mask)

    projected = dataset_name(paths["geodatabase"], "peat_raster_projected")
    arcpy.management.ProjectRaster(
        str(inputs["peat_raster"]),
        projected,
        arcpy.SpatialReference(config["projection_epsg"]),
        cell_size=config["cell_size"],
    )

    normalize_raster(projected, peat_score, benefit=False, mask_raster=analysis_mask)

    print("Peat score complete")
    print(f"Score raster: {peat_score}")


if __name__ == "__main__":
    main()
