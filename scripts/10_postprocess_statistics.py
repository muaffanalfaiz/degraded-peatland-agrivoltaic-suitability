"""10_postprocess_statistics

Export class-wise summary statistics from the final classified suitability raster.

Creates:
- outputs/tables/suitability_area_stats.csv
"""

from __future__ import annotations

from pathlib import Path

from _helpers import (
    dataset_name,
    ensure_arcpy,
    ensure_file_gdb,
    get_workspace_paths,
    load_config,
    raster_area_table_to_csv,
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

    csv_path = paths["project_root"] / "outputs" / "tables" / "suitability_area_stats.csv"
    raster_area_table_to_csv(
        final_class,
        csv_path,
        config["class_labels"],
        cell_size=float(config["cell_size"]),
    )

    print("Post-processing statistics complete")
    print(f"CSV exported: {csv_path}")


if __name__ == "__main__":
    main()
