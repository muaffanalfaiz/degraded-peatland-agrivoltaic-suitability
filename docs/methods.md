# Methods

## Software
- ArcGIS Pro
- Raster-based GIS processing
- AHP for weight derivation
- WLC for final suitability integration

## Spatial environment
- Projection: WGS 84 / UTM Zone 48S
- Cell size: 30 m
- Processing domain: South Sumatra
- Analysis focus: degraded peatland domain after constraints

## Workflow summary

### 1. Define study area and mask
The analysis was restricted to degraded peatland areas within South Sumatra.

### 2. Build hard constraints
Restricted areas were excluded from suitability analysis. These included protected and conservation areas plus other operationally restricted zones described in the manuscript.

### 3. Prepare criterion layers
Eight criteria were used:
1. Fire hazard (FRP-weighted kernel density)
2. Peat depth / geotechnical proxy
3. Flood vulnerability index
4. Slope
5. Proximity to roads
6. Aspect
7. Topographic Position Index (TPI)
8. Global Horizontal Irradiance (GHI)

### 4. Normalize layers
All criteria were normalized to a benefit-oriented 0–1 scale before overlay.

### 5. Derive weights
Criterion weights were derived through AHP pairwise comparison.

### 6. Overlay and classify
A weighted linear combination produced the final suitability index, which was then classified into four planning classes.

## Output classes used in this repo
To keep repository terminology consistent, the public repo uses:
- Very low
- Low
- Moderately suitable
- Highly suitable

## Reproducibility note
The original workflow was completed inside ArcGIS Pro. The `scripts/` folder in this repository is a **reconstruction scaffold**, not a claim that the original analysis was fully coded from the start.
