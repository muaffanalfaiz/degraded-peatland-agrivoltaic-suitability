"""00_env_setup

Create the local analysis workspace and validate the minimum project configuration.

Run from ArcGIS Pro Python:
    python scripts/00_env_setup.py
"""

from __future__ import annotations

from pathlib import Path

from _helpers import ensure_arcpy, ensure_file_gdb, get_workspace_paths, load_config, set_env


def main() -> None:
    ensure_arcpy()
    config = load_config()
    paths = get_workspace_paths(config)
    ensure_file_gdb(paths["geodatabase"])
    set_env(config)

    print("Environment ready")
    print(f"Project root      : {paths['project_root']}")
    print(f"Local workspace   : {paths['local_workspace']}")
    print(f"Analysis geodatabase: {paths['geodatabase']}")
    print(f"Final public TIFF : {paths['final_public_tif']}")
    print("")
    print("Next:")
    print("1. Edit config/project_config.json with your local source-data paths.")
    print("2. Run 01_prepare_study_area.py")
    print("3. Continue step-by-step through the pipeline.")


if __name__ == "__main__":
    main()
