# Degraded Peatland Agrivoltaic Suitability

GIS–MCDA-based land suitability analysis for agrivoltaic development on degraded peatlands in South Sumatra, Indonesia.

![Final Suitability Map](outputs/figures/12_final_suitability_map.jpg)

## Related article

This repository accompanies the published article:

> Wisaksono, M. A. (2026). GIS–MCDA-based land suitability analysis for agrivoltaic development on degraded peatlands in South Sumatra. *Jurnal Lahan Suboptimal: Journal of Suboptimal Lands*, 15(1), 7–20. https://doi.org/10.36706/jlso.15.1.2026.783

## Overview

This repository presents a GIS-based multi-criteria decision analysis (MCDA) framework for screening degraded peatlands in South Sumatra for potential agrivoltaic development. The project integrates peatland-specific risk factors, accessibility, terrain variables, and solar resource data to identify candidate zones while excluding ecologically sensitive and legally restricted areas.

The analysis was developed in ArcGIS Pro and is accompanied by a structured ArcPy reconstruction scaffold, exported thematic maps, and an interactive project dashboard.

## Why this project matters

Peatlands in South Sumatra face recurring fire risk, seasonal flooding, drainage-related land subsidence, and widespread degradation from past land conversion. At the same time, the region has meaningful solar irradiance potential. This project explores whether degraded peat areas can be screened for agrivoltaic development without encouraging encroachment into intact or protected peat ecosystems.

## Core idea

This is a **risk-first agrivoltaic siting framework**. Rather than prioritising irradiance alone, the analysis first considers fire hazard, peat depth, flood vulnerability, and topographic feasibility. Solar resource acts as an additional suitability factor after major ecological and constructability filters are applied.

## Key results

Of the **230,810 ha** of degraded peatland in South Sumatra, **124,008 ha** remained after protected-area constraints were applied. Within that eligible domain:

| Class | Area (ha) | Share of eligible domain |
|---|---:|---:|
| Very suitable | 66,665.25 | 53.76% |
| Moderately suitable | 30,867.84 | 24.89% |
| Unsuitable | 24,408.99 | 19.68% |
| Very unsuitable | 2,065.68 | 1.67% |

Overall, **78.65%** of the eligible degraded peatland domain was classified as moderately suitable or very suitable for agrivoltaic development.

## Dashboard

An interactive project dashboard is available in the [`dashboard/`](dashboard/) folder. It provides a visual overview of the suitability results, AHP-derived criterion weights, peatland domain context, analytical pipeline, and a switchable map explorer for all 12 thematic layers.

**To open it:** download [`dashboard/index.html`](dashboard/index.html) and open it in any browser. No install or build tools are required.

## Methods

The workflow was developed in ArcGIS Pro using a GIS–MCDA approach with:

- Common spatial grid: 30 m
- Projected coordinate system: Indonesian 1974 / UTM Zone 48S (EPSG:23888)
- Analytic Hierarchy Process (AHP) for criterion weighting (CR = 0.00244)
- Weighted Linear Combination (WLC) for suitability integration
- Protected areas (WDPA) and related land-cover exclusions as hard constraints

## Evaluation criteria

Eight criteria were integrated through AHP pairwise comparison:

| Criterion | Weight | Direction | Source |
|---|---:|---|---|
| Fire hazard (FRP-weighted KDE) | 0.1965 | Cost | NASA FIRMS (VIIRS 375 m) |
| Peat depth / geotechnical proxy | 0.1781 | Cost | BBSDLP / Ministry of Agriculture |
| Flood vulnerability index | 0.1599 | Cost | BNPB InaRISK Geoservices |
| Slope | 0.1412 | Benefit | BIG DEM |
| Distance to roads | 0.1216 | Benefit | OpenStreetMap / Geofabrik |
| Global Horizontal Irradiance | 0.1099 | Benefit | Global Solar Atlas v2 |
| Aspect | 0.0573 | Benefit | BIG DEM |
| Topographic Position Index | 0.0355 | Benefit | BIG DEM |

Risk factors (fire, peat depth, and flood vulnerability) collectively account for **53.5%** of the total weight, reflecting the risk-first design philosophy.

## Study area

South Sumatra, Indonesia.

![Fire Risk Map](outputs/figures/10_fire_risk_map.jpg)

## Repository structure

```text
degraded-peatland-agrivoltaic-suitability/
├── arcgis-pro/                  ArcGIS Pro project file
│   └── agrivoltaic_suitability_clean.aprx
├── config/                      Project configuration and AHP weights
│   ├── project_config.json
│   ├── project_config_template.yml
│   └── weights.yml
├── dashboard/                   Interactive results dashboard (open index.html)
│   ├── index.html
│   └── app.jsx
├── data/
│   ├── final/                   Primary analysis output
│   │   ├── final_suitability.tif
│   │   └── final_vectors.gdb/   Study area, peatlands, WDPA layers
│   └── criteria_optional/       Eight reclassified input criterion rasters
├── docs/                        Methods, data sources, limitations
├── outputs/
│   ├── figures/                 12 thematic and suitability maps
│   └── tables/                  AHP weights, area statistics, figure manifest
├── results/                     Key findings summary
└── scripts/                     ArcPy workflow scaffold (12 steps + helpers)
    ├── 00_env_setup.py … 11_export_maps.py
    ├── run_pipeline.py
    └── _helpers.py
```

## Reproducibility note

The Python workflow in this repository is a structured ArcPy implementation of the project logic. The `config/project_config.json` uses example input paths and should be adapted to local dataset locations and field schema before reuse.

The criteria rasters in `data/criteria_optional/` are exported from the original ArcGIS Pro workflow at their native processing resolutions and are provided as visual reference outputs. They were resampled to the common 30 m analysis grid within ArcGIS Pro before the weighted overlay was computed.

This repository is a **public project showcase and adaptable workflow template**, not a plug-and-play rerun package.

## Publication

This repository is associated with the following published article:

> Wisaksono, M. A. (2026). GIS–MCDA-based land suitability analysis for agrivoltaic development on degraded peatlands in South Sumatra. *Jurnal Lahan Suboptimal: Journal of Suboptimal Lands*, 15(1), 7–20. https://doi.org/10.36706/jlso.15.1.2026.783

## Limitations

- The original analysis was developed in ArcGIS Pro through a GUI-led workflow and later translated into a structured ArcPy scaffold.
- Peat depth was approximated using a morphometric distance-from-edge proxy rather than direct depth measurements.
- Some original source datasets are not redistributed in this repository due to size or licensing constraints.
- The final suitability map is a screening product and should not be treated as engineering approval or investment advice.
- Field validation, hydrological checks, geotechnical feasibility, land tenure review, and grid connection assessment are required before implementation decisions.

## Citation

If you use the scientific results, please cite the journal article:

> Wisaksono, M. A. (2026). GIS–MCDA-based land suitability analysis for agrivoltaic development on degraded peatlands in South Sumatra. *Jurnal Lahan Suboptimal: Journal of Suboptimal Lands*, 15(1), 7–20. https://doi.org/10.36706/jlso.15.1.2026.783

If you use the repository materials, workflow scaffold, figures, or dashboard, you may also cite the repository as software:

> Wisaksono, M. A. (2026). *Degraded Peatland Agrivoltaic Suitability* [Software]. GitHub. https://github.com/muaffanalfaiz/degraded-peatland-agrivoltaic-suitability

## Author

**Muaffan Alfaiz Wisaksono**  
Precision Agriculture / GIS / Environmental Spatial Analysis  
Lincoln University, New Zealand

## License

[MIT](LICENSE)
