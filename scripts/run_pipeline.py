"""run_pipeline

Convenience runner for the full ArcPy workflow.

Run from ArcGIS Pro Python:
    python scripts/run_pipeline.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

ORDER = [
    "00_env_setup.py",
    "01_prepare_study_area.py",
    "02_prepare_constraints.py",
    "03_prepare_fire_risk.py",
    "04_prepare_peat_layer.py",
    "05_prepare_flood_layer.py",
    "06_prepare_terrain_layers.py",
    "07_prepare_accessibility_layer.py",
    "08_prepare_ghi_layer.py",
    "09_weighted_overlay.py",
    "10_postprocess_statistics.py",
    "11_export_maps.py",
]


def main() -> None:
    for script_name in ORDER:
        script_path = SCRIPT_DIR / script_name
        print(f"Running {script_name}")
        subprocess.check_call([sys.executable, str(script_path)])


if __name__ == "__main__":
    main()
