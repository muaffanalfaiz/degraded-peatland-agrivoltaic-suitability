"""07_prepare_accessibility_layer

Create a distance-to-roads raster and normalize it to a 0-1 benefit scale where
pixels closer to roads are more suitable.

Required config inputs:
- roads
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

    inputs = require_inputs(config, ["roads"])
    analysis_mask = dataset_name(paths["geodatabase"], config["outputs"]["analysis_mask_raster"])
    if not arcpy.Exists(analysis_mask):
        raise FileNotFoundError("Run 01_prepare_study_area.py first.")

    set_env(config, snap_raster=analysis_mask, mask_raster=analysis_mask)

    roads_projected = dataset_name(paths["geodatabase"], "roads_projected")
    roads_distance = dataset_name(paths["geodatabase"], "distance_to_roads_raw")
    roads_score = dataset_name(paths["geodatabase"], config["outputs"]["roads_score"])

    arcpy.management.Project(str(inputs["roads"]), roads_projected, arcpy.SpatialReference(config["projection_epsg"]))

    euc = arcpy.sa.EucDistance(roads_projected, cell_size=config["cell_size"])
    euc.save(roads_distance)

    normalize_raster(roads_distance, roads_score, benefit=False, mask_raster=analysis_mask)

    print("Accessibility score complete")
    print(f"Distance raster: {roads_distance}")
    print(f"Score raster   : {roads_score}")


if __name__ == "__main__":
    main()
