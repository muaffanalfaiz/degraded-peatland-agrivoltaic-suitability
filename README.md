# Degraded Peatland Agrivoltaic Suitability

GIS–MCDA-based land suitability analysis for agrivoltaic development on degraded peatlands in South Sumatra, Indonesia.

## What this repository is

This repository is a **public project showcase plus reproducibility scaffold** for an ArcGIS Pro research project that evaluates agrivoltaic suitability on degraded peatlands in South Sumatra.

The original workflow was completed in **ArcGIS Pro** using:
- a 30 m raster grid
- UTM Zone 48S
- GIS-based Multi-Criteria Decision Analysis (MCDA)
- Analytic Hierarchy Process (AHP)
- Weighted Linear Combination (WLC)
- hard constraint masking for protected and restricted areas

## Core idea

This project does **not** treat solar irradiance as the only decision factor.  
It uses a **risk-first** screening logic tailored to peatland conditions by combining:
- fire hazard
- peat depth / geotechnical proxy
- flood vulnerability
- slope
- distance to roads
- aspect
- topographic position index (TPI)
- global horizontal irradiance (GHI)

## Study area

South Sumatra, Indonesia.

## Main result

Within the eligible degraded peat analysis domain (**124,007.76 ha**), the final suitability surface classified:
- **Highly suitable**: 66,665.25 ha (53.76%)
- **Moderately suitable**: 30,867.84 ha (24.89%)
- **Low**: 24,408.99 ha (19.69%)
- **Very low**: 2,065.68 ha (1.67%)

Overall, **78.65%** of the eligible degraded peat domain fell into the moderately suitable to highly suitable range.

## Repository status

This repository is intentionally structured in two layers:

1. **Ready now**
   - README
   - documentation
   - exported figures
   - tables
   - upload guide
   - Git/GitHub guide
   - script roadmap

2. **To be added gradually**
   - sanitized `.aprx`
   - ArcPy reconstruction modules
   - cleaned metadata inventory
   - sample shareable data
   - optional notebooks / validation outputs

## Recommended first public upload contents

Upload these first:
- `README.md`
- `docs/`
- `outputs/figures/`
- `outputs/tables/`
- `results/`
- `.gitignore`
- `LICENSE`
- `CITATION.cff`

Add later:
- `arcgis-pro/project_clean.aprx`
- `scripts/*.py`
- `data/metadata/*`

## Publication note

The study is **accepted but not yet formally published**.  
Because of that, the final accepted manuscript file is **not included** in this repository package by default.  
After formal publication, add the final citation, DOI, and any journal-permitted manuscript version.

## Quick start for GitHub

See:
- `GITHUB_UPLOAD_GUIDE.md`
- `docs/upload_checklist.md`
- `scripts/README.md`

## Author

**Muaffan Alfaiz Wisaksono**  
Lincoln University  
Precision Agriculture • GIS • Environmental Spatial Analysis
