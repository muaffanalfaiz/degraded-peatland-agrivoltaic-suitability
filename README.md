# Degraded Peatland Agrivoltaic Suitability

GIS–MCDA-based land suitability analysis for agrivoltaic development on degraded peatlands in South Sumatra, Indonesia.

## Overview

This repository presents a GIS-based multi-criteria decision analysis framework for screening degraded peatlands in South Sumatra for potential agrivoltaic development. The project was originally developed in ArcGIS Pro and integrates peatland-specific risk factors, accessibility, terrain variables, and solar resource information to identify candidate zones while avoiding ecologically sensitive or restricted areas.

## Why this project matters

Peatlands in South Sumatra face recurring fire risk, seasonal flooding, drainage-related instability, and land degradation. At the same time, the region has meaningful solar potential. This project explores whether degraded peatlands can be screened for agrivoltaic development without encouraging expansion into intact peat ecosystems.

## Core idea

This is a risk-first agrivoltaic siting framework. Rather than prioritizing irradiance alone, the analysis first considers:

- fire hazard
- peat depth or peat-condition proxy
- flood vulnerability
- topographic feasibility
- road accessibility

Solar resource acts as an additional suitability factor after major ecological and constructability filters are considered.

## Study area

South Sumatra, Indonesia.

## Methods

The workflow was developed in ArcGIS Pro using a GIS–MCDA approach with:

- common spatial grid: 30 m
- projected coordinate system: WGS 84 / UTM Zone 48S
- Analytic Hierarchy Process (AHP) for criterion weighting
- Weighted Linear Combination (WLC) for suitability integration
- protected areas and related exclusions as hard constraints

## Evaluation criteria

Eight criteria were integrated:

1. Fire hazard
2. Peat depth or peat-condition proxy
3. Flood vulnerability
4. Slope
5. Distance to roads
6. Global Horizontal Irradiance (GHI)
7. Aspect
8. Topographic Position Index (TPI)

## Main result

The final suitability surface highlights clustered agrivoltaic opportunity zones within the degraded peat domain after constraints were applied. The project is intended as a first-pass spatial screening tool for planning, prioritization, and future validation.

## Repository contents

- `outputs/figures/` — thematic and final suitability maps
- `outputs/tables/` — weights, area summaries, and supporting tables
- `results/` — short summary findings
- `docs/` — project summary, methods, data sources, and limitations
- `scripts/` — ArcPy workflow scaffold reflecting the project logic
- `config/project_config.json` — public example configuration template
- `data/rasters/final_suitability_30m.tif` — final public raster output

## Reproducibility note

The Python workflow in this repository is provided as a structured ArcPy implementation of the project logic. The included `config/project_config.json` uses example input paths and is intended as a template for adaptation. Users who wish to rerun or adapt the workflow should replace those paths with their own local datasets and confirm field names, schemas, and processing assumptions.

This repository should therefore be understood as a public project showcase plus adaptable workflow template, not as a fully plug-and-play rerun package.

## Publication status

This project is based on a study that has been accepted for publication but is not yet formally published. The manuscript file is not included in this repository.

## Limitations

- The original analysis was developed in ArcGIS Pro through a GUI-led workflow and later translated into a structured ArcPy scaffold.
- Some original source datasets are not redistributed directly in this repository.
- The final suitability map is a screening product and should not be treated as final engineering approval or site investment advice.
- Field validation, hydrological checks, geotechnical feasibility, land tenure review, and grid connection assessment are still required for implementation decisions.

## Citation

A formal citation and DOI will be added after publication.

## Author

Muaffan Alfaiz Wisaksono  
Precision Agriculture / GIS / Environmental Spatial Analysis