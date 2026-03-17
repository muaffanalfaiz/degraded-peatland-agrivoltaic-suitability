"""Shared helper utilities for the ArcPy pipeline."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

try:
    import arcpy
    from arcpy.sa import Con, ExtractByMask, IsNull, Raster, Reclassify, RemapRange
except ImportError:  # pragma: no cover
    arcpy = None


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "project_config.json"


def ensure_arcpy() -> None:
    if arcpy is None:
        raise ImportError(
            "ArcPy is not available. Run these scripts from the ArcGIS Pro Python environment."
        )


def load_config(config_path: str | Path | None = None) -> Dict:
    path = Path(config_path) if config_path else DEFAULT_CONFIG
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def project_root() -> Path:
    return PROJECT_ROOT


def resolve_path(path_str: str | None, base: Path | None = None) -> Path | None:
    if not path_str:
        return None
    p = Path(path_str)
    if p.is_absolute():
        return p
    return (base or PROJECT_ROOT) / p


def get_workspace_paths(config: Dict) -> Dict[str, Path]:
    root = project_root()
    local_workspace = resolve_path(config.get("local_workspace", "scratch"), root)
    local_workspace.mkdir(parents=True, exist_ok=True)
    geodatabase = local_workspace / "analysis_outputs.gdb"
    return {
        "project_root": root,
        "local_workspace": local_workspace,
        "geodatabase": geodatabase,
        "final_public_tif": resolve_path(config["final_public_tif"], root),
    }


def ensure_file_gdb(gdb_path: Path) -> Path:
    ensure_arcpy()
    if not arcpy.Exists(str(gdb_path)):
        arcpy.management.CreateFileGDB(str(gdb_path.parent), gdb_path.name)
    return gdb_path


def set_env(config: Dict, snap_raster: str | None = None, mask_raster: str | None = None, extent=None) -> None:
    ensure_arcpy()
    arcpy.env.overwriteOutput = True
    arcpy.env.parallelProcessingFactor = "100%"
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(config["projection_epsg"])
    arcpy.env.cellSize = config["cell_size"]
    if snap_raster:
        arcpy.env.snapRaster = snap_raster
    if mask_raster:
        arcpy.env.mask = mask_raster
    if extent:
        arcpy.env.extent = extent


def require_inputs(config: Dict, required_keys: Iterable[str]) -> Dict[str, Path]:
    resolved = {}
    for key in required_keys:
        value = config["inputs"].get(key, "")
        path = resolve_path(value)
        if not path:
            raise ValueError(f"Missing config input path for '{key}' in project_config.json")
        if not arcpy.Exists(str(path)):
            raise FileNotFoundError(f"Input path for '{key}' does not exist: {path}")
        resolved[key] = path
    return resolved


def normalize_raster(in_raster: str, out_raster: str, benefit: bool, mask_raster: str | None = None) -> str:
    ensure_arcpy()
    ras = Raster(in_raster)
    if mask_raster:
        ras = ExtractByMask(ras, mask_raster)

    rmin = float(arcpy.management.GetRasterProperties(ras, "MINIMUM").getOutput(0))
    rmax = float(arcpy.management.GetRasterProperties(ras, "MAXIMUM").getOutput(0))

    if rmax == rmin:
        normalized = Con(IsNull(ras), None, 1)
    else:
        if benefit:
            normalized = (ras - rmin) / (rmax - rmin)
        else:
            normalized = (rmax - ras) / (rmax - rmin)

    normalized.save(out_raster)
    return out_raster


def normalize_by_distance_to_target(
    in_raster: str,
    out_raster: str,
    target_value: float,
    mask_raster: str | None = None,
) -> str:
    """Convert closeness to target value into a 0-1 benefit score."""
    ensure_arcpy()
    ras = Raster(in_raster)
    if mask_raster:
        ras = ExtractByMask(ras, mask_raster)

    distance = abs(ras - target_value)
    dmin = float(arcpy.management.GetRasterProperties(distance, "MINIMUM").getOutput(0))
    dmax = float(arcpy.management.GetRasterProperties(distance, "MAXIMUM").getOutput(0))

    if dmax == dmin:
        normalized = Con(IsNull(distance), None, 1)
    else:
        normalized = (dmax - distance) / (dmax - dmin)

    normalized.save(out_raster)
    return out_raster


def classify_continuous_raster(in_raster: str, out_raster: str, breaks: Sequence[float]) -> str:
    ensure_arcpy()
    if len(breaks) != 5:
        raise ValueError("Expected exactly 5 class break values for 4 classes.")
    remap = RemapRange([
        [breaks[0], breaks[1], 1],
        [breaks[1], breaks[2], 2],
        [breaks[2], breaks[3], 3],
        [breaks[3], breaks[4], 4],
    ])
    classified = Reclassify(in_raster, "Value", remap, "NODATA")
    classified.save(out_raster)
    return out_raster


def raster_area_table_to_csv(
    in_raster: str,
    csv_path: Path,
    class_labels: Dict[str, str],
    cell_size: float,
) -> None:
    ensure_arcpy()
    tmp_table = str(csv_path.with_suffix(".dbf"))
    if arcpy.Exists(tmp_table):
        arcpy.management.Delete(tmp_table)

    arcpy.sa.BuildRasterAttributeTable(in_raster, "Overwrite")
    arcpy.conversion.TableToTable(in_raster, str(csv_path.parent), csv_path.stem + ".dbf")
    dbf_table = str(csv_path.with_suffix(".dbf"))

    fields = [f.name for f in arcpy.ListFields(dbf_table)]
    value_field = "Value" if "Value" in fields else "VALUE"
    count_field = "Count" if "Count" in fields else "COUNT"

    rows: List[Tuple[int, int, float, float, str]] = []
    area_m2 = float(cell_size) * float(cell_size)

    with arcpy.da.SearchCursor(dbf_table, [value_field, count_field]) as cursor:
        for value, count in cursor:
            hectares = (count * area_m2) / 10000.0
            km2 = hectares / 100.0
            label = class_labels.get(str(value), f"class_{value}")
            rows.append((value, count, hectares, km2, label))

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    import csv
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["class_value", "pixel_count", "area_ha", "area_km2", "class_label"])
        writer.writerows(rows)

    # clean temporary dbf copy
    if arcpy.Exists(dbf_table):
        arcpy.management.Delete(dbf_table)


def copy_raster_to_public_tif(in_raster: str, out_tif: Path) -> Path:
    ensure_arcpy()
    out_tif.parent.mkdir(parents=True, exist_ok=True)
    arcpy.management.CopyRaster(
        in_raster,
        str(out_tif),
        format="TIFF",
        nodata_value="0",
    )
    return out_tif


def dataset_name(gdb_path: Path, name: str) -> str:
    return str(gdb_path / name)
