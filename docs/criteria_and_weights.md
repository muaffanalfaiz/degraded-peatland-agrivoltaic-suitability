# Criteria and weights

The public repository uses the AHP weights reported in the manuscript.

| Criterion | Weight | Direction | Notes |
|---|---:|---|---|
| Fire hazard (FRP-weighted KDE) | 0.1965 | Cost | Higher fire hazard reduces suitability |
| Peat depth / geotechnical proxy | 0.1781 | Cost | Higher-risk peat conditions reduce suitability |
| Flood vulnerability index | 0.1599 | Cost | Higher flood vulnerability reduces suitability |
| Slope | 0.1412 | Benefit after scoring | Gentler slopes are preferred in scoring |
| Proximity to roads | 0.1216 | Benefit | Closer access is preferred |
| Global Horizontal Irradiance (GHI) | 0.1099 | Benefit | Higher solar resource increases suitability |
| Aspect | 0.0573 | Benefit after scoring | Minor terrain-orientation refinement |
| Topographic Position Index (TPI) | 0.0355 | Benefit after scoring | Micro-topographic suitability refinement |

## Consistency
Reported AHP consistency values from the manuscript:
- λmax ≈ 8.0241
- CI ≈ 0.00344
- CR ≈ 0.00244

This CR is comfortably within acceptable consistency thresholds.

If you later revise terminology, keep the wording consistent across:
- README
- docs
- tables
- figure captions
- GitHub repo description
