"""03_prepare_fire_risk

Create a fire-hazard score raster from hotspot points using FRP-weighted kernel density,
then normalize to a 0-1 benefit scale where lower fire hazard scores higher.

Required config inputs:
- hotspot_points
- study_area_boundary
Optional:
- hotspot_frp field name in config["fields"]["hotspot_frp"]
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

    inputs = require_inputs(config, ["hotspot_points", "study_area_boundary"])
    analysis_mask = dataset_name(paths["geodatabase"], config["outputs"]["analysis_mask_raster"])
    if not arcpy.Exists(analysis_mask):
        raise FileNotFoundError("Run 01_prepare_study_area.py first.")

    set_env(config, snap_raster=analysis_mask, mask_raster=analysis_mask)

    sr = arcpy.SpatialReference(config["projection_epsg"])
    hotspot_fc = dataset_name(paths["geodatabase"], "hotspots_projected")
    hotspot_clip = dataset_name(paths["geodatabase"], "hotspots_clip")
    fire_kde = dataset_name(paths["geodatabase"], "fire_kde_raw")
    fire_score = dataset_name(paths["geodatabase"], config["outputs"]["fire_score"])

    arcpy.management.Project(str(inputs["hotspot_points"]), hotspot_fc, sr)
    arcpy.analysis.Clip(hotspot_fc, str(inputs["study_area_boundary"]), hotspot_clip)

    frp_field = config.get("fields", {}).get("hotspot_frp", "")
    available_fields = [f.name for f in arcpy.ListFields(hotspot_clip)]
    population_field = frp_field if frp_field in available_fields else None

    kde = arcpy.sa.KernelDensity(
        in_features=hotspot_clip,
        population_field=population_field,
        cell_size=config["cell_size"],
    )
    kde.save(fire_kde)

    normalize_raster(fire_kde, fire_score, benefit=False, mask_raster=analysis_mask)

    print("Fire-risk score complete")
    print(f"Raw KDE  : {fire_kde}")
    print(f"Score    : {fire_score}")


if __name__ == "__main__":
    main()
