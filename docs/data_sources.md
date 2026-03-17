# Data sources

This file records the data lineage used in the project based on the manuscript text.  
It is meant for transparency and future metadata cleanup.

## Criteria data sources

### 1. Fire hazard
- Source: NASA FIRMS (VIIRS 375 m) with FRP attribute
- Derived product: FRP-weighted kernel density surface

### 2. Peat depth / geotechnical proxy
- Source noted in manuscript: BBSDLP / Ministry of Agriculture
- Public note: clarify later whether this was used as direct peat depth classes, a proxy, or a processed interpretation layer

### 3. Flood vulnerability index
- Source: BNPB InaRISK Geoservices

### 4. Terrain-derived variables
- DEM source: Badan Informasi Geospasial (BIG)
- Derived layers:
  - slope
  - aspect
  - TPI

### 5. Road accessibility
- Source: OpenStreetMap / Geofabrik
- Derived product: distance-to-road raster

### 6. Solar resource
- Source: Global Solar Atlas v2
- Provider: World Bank / ESMAP / Solargis

### 7. Protected areas / conservation exclusions
- Source: WDPA and other constraint layers described in the manuscript

## Recommended next step
Create `data/metadata/data_inventory.csv` with columns:
- layer_name
- original_source
- format
- year
- resolution
- processing_step
- shared_publicly (yes/no)
- notes
