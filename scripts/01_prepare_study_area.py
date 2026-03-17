"""01_prepare_study_area

Prepare:
- projected study area boundary
- projected degraded peat polygons
- analysis mask raster (1 = eligible degraded peat domain)

Required config inputs:
- study_area_boundary
- degraded_peat_polygons
"""

from __future__ import annotations

from _helpers import (
    dataset_name,
    ensure_arcpy,
    ensure_file_gdb,
    get_workspace_paths,
    load_config,
    require_inputs,
    set_env,
)
import arcpy


def main() -> None:
    ensure_arcpy()
    config = load_config()
    paths = get_workspace_paths(config)
    ensure_file_gdb(paths["geodatabase"])

    inputs = require_inputs(config, ["study_area_boundary", "degraded_peat_polygons"])
    set_env(config)

    study_area_fc = dataset_name(paths["geodatabase"], "study_area_boundary")
    degraded_peat_fc = dataset_name(paths["geodatabase"], "degraded_peat_projected")
    degraded_peat_clip = dataset_name(paths["geodatabase"], "degraded_peat_clip")
    analysis_mask = dataset_name(paths["geodatabase"], config["outputs"]["analysis_mask_raster"])

    sr = arcpy.SpatialReference(config["projection_epsg"])

    arcpy.management.Project(str(inputs["study_area_boundary"]), study_area_fc, sr)
    arcpy.management.Project(str(inputs["degraded_peat_polygons"]), degraded_peat_fc, sr)
    arcpy.analysis.Clip(degraded_peat_fc, study_area_fc, degraded_peat_clip)

    field_names = [f.name for f in arcpy.ListFields(degraded_peat_clip)]
    if "MASKVAL" not in field_names:
        arcpy.management.AddField(degraded_peat_clip, "MASKVAL", "SHORT")
    arcpy.management.CalculateField(degraded_peat_clip, "MASKVAL", 1)

    arcpy.conversion.FeatureToRaster(
        degraded_peat_clip,
        "MASKVAL",
        analysis_mask,
        config["cell_size"],
    )

    set_env(config, snap_raster=analysis_mask, mask_raster=analysis_mask, extent=study_area_fc)

    print("Study-area preparation complete")
    print(f"Study area feature  : {study_area_fc}")
    print(f"Degraded peat clip  : {degraded_peat_clip}")
    print(f"Analysis mask raster: {analysis_mask}")


if __name__ == "__main__":
    main()
