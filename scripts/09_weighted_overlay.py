"""09_weighted_overlay

Combine the normalized criterion rasters using the published AHP weights and apply
the hard-constraint mask.

Outputs:
- continuous suitability index (0-1)
- final four-class suitability raster

Run this after scripts 01-08 are complete.
"""

from __future__ import annotations

from _helpers import (
    classify_continuous_raster,
    dataset_name,
    ensure_arcpy,
    ensure_file_gdb,
    get_workspace_paths,
    load_config,
    set_env,
)
import arcpy
from arcpy.sa import Raster


def main() -> None:
    ensure_arcpy()
    arcpy.CheckOutExtension("Spatial")

    config = load_config()
    paths = get_workspace_paths(config)
    ensure_file_gdb(paths["geodatabase"])

    analysis_mask = dataset_name(paths["geodatabase"], config["outputs"]["analysis_mask_raster"])
    eligible_mask = dataset_name(paths["geodatabase"], config["outputs"]["eligible_constraint_mask"])

    required_outputs = [
        config["outputs"]["fire_score"],
        config["outputs"]["peat_score"],
        config["outputs"]["flood_score"],
        config["outputs"]["slope_score"],
        config["outputs"]["roads_score"],
        config["outputs"]["ghi_score"],
        config["outputs"]["aspect_score"],
        config["outputs"]["tpi_score"],
        config["outputs"]["eligible_constraint_mask"],
    ]
    for name in required_outputs:
        path = dataset_name(paths["geodatabase"], name)
        if not arcpy.Exists(path):
            raise FileNotFoundError(f"Required raster missing: {path}")

    set_env(config, snap_raster=analysis_mask, mask_raster=analysis_mask)

    w = config["weights"]
    suitability_index = (
        Raster(dataset_name(paths["geodatabase"], config["outputs"]["fire_score"])) * w["fire_hazard"]
        + Raster(dataset_name(paths["geodatabase"], config["outputs"]["peat_score"])) * w["peat_depth_proxy"]
        + Raster(dataset_name(paths["geodatabase"], config["outputs"]["flood_score"])) * w["flood_vulnerability"]
        + Raster(dataset_name(paths["geodatabase"], config["outputs"]["slope_score"])) * w["slope"]
        + Raster(dataset_name(paths["geodatabase"], config["outputs"]["roads_score"])) * w["distance_to_roads"]
        + Raster(dataset_name(paths["geodatabase"], config["outputs"]["ghi_score"])) * w["ghi"]
        + Raster(dataset_name(paths["geodatabase"], config["outputs"]["aspect_score"])) * w["aspect"]
        + Raster(dataset_name(paths["geodatabase"], config["outputs"]["tpi_score"])) * w["tpi"]
    )

    continuous_out = dataset_name(paths["geodatabase"], config["outputs"]["continuous_suitability"])
    class_out = dataset_name(paths["geodatabase"], config["outputs"]["final_class_raster"])

    constrained = suitability_index * Raster(eligible_mask)
    constrained.save(continuous_out)

    classify_continuous_raster(continuous_out, class_out, config["class_breaks"])

    print("Weighted overlay complete")
    print(f"Continuous suitability: {continuous_out}")
    print(f"Final class raster    : {class_out}")


if __name__ == "__main__":
    main()
