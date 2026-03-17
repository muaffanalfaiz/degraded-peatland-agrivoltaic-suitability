"""02_prepare_constraints

Create a hard-constraint raster where:
- 1 = eligible
- 0 = constrained

This script currently uses protected areas as the hard constraint because that is the
publicly documented constraint in the paper. You can extend it later with additional
exclusion layers if needed.

Required config inputs:
- protected_areas
- study_area_boundary
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
from arcpy.sa import Con, IsNull, Raster


def main() -> None:
    ensure_arcpy()
    config = load_config()
    paths = get_workspace_paths(config)
    ensure_file_gdb(paths["geodatabase"])

    inputs = require_inputs(config, ["protected_areas", "study_area_boundary"])
    analysis_mask = dataset_name(paths["geodatabase"], config["outputs"]["analysis_mask_raster"])
    if not arcpy.Exists(analysis_mask):
        raise FileNotFoundError("Run 01_prepare_study_area.py first to create the analysis mask raster.")

    set_env(config, snap_raster=analysis_mask, mask_raster=analysis_mask)

    protected_fc = dataset_name(paths["geodatabase"], "protected_areas_projected")
    protected_clip = dataset_name(paths["geodatabase"], "protected_areas_clip")
    protected_raster = dataset_name(paths["geodatabase"], "protected_areas_raster")
    eligible_mask = dataset_name(paths["geodatabase"], config["outputs"]["eligible_constraint_mask"])

    sr = arcpy.SpatialReference(config["projection_epsg"])

    arcpy.management.Project(str(inputs["protected_areas"]), protected_fc, sr)
    arcpy.analysis.Clip(protected_fc, str(inputs["study_area_boundary"]), protected_clip)

    field_names = [f.name for f in arcpy.ListFields(protected_clip)]
    if "EXCLUDE" not in field_names:
        arcpy.management.AddField(protected_clip, "EXCLUDE", "SHORT")
    arcpy.management.CalculateField(protected_clip, "EXCLUDE", 1)

    arcpy.conversion.FeatureToRaster(protected_clip, "EXCLUDE", protected_raster, config["cell_size"])

    eligible = Con(IsNull(Raster(protected_raster)), Raster(analysis_mask), 0)
    eligible.save(eligible_mask)

    print("Constraint preparation complete")
    print(f"Eligible mask raster: {eligible_mask}")


if __name__ == "__main__":
    main()
