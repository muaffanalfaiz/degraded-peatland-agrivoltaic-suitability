"""11_export_maps

Export the final classified suitability raster to the public GeoTIFF path tracked in GitHub.

Creates:
- data/rasters/final_suitability_30m.tif
"""

from __future__ import annotations

from _helpers import (
    copy_raster_to_public_tif,
    dataset_name,
    ensure_arcpy,
    ensure_file_gdb,
    get_workspace_paths,
    load_config,
)
import arcpy


def main() -> None:
    ensure_arcpy()
    config = load_config()
    paths = get_workspace_paths(config)
    ensure_file_gdb(paths["geodatabase"])

    final_class = dataset_name(paths["geodatabase"], config["outputs"]["final_class_raster"])
    if not arcpy.Exists(final_class):
        raise FileNotFoundError("Run 09_weighted_overlay.py first.")

    out_tif = copy_raster_to_public_tif(final_class, paths["final_public_tif"])

    print("Public TIFF export complete")
    print(f"Exported: {out_tif}")


if __name__ == "__main__":
    main()
