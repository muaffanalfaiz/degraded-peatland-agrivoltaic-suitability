# Project Summary

## Overview

This project applies a GIS-based multi-criteria decision analysis framework
to screen degraded peatlands in South Sumatra, Indonesia for potential
agrivoltaic development. The analysis integrates peatland-specific risk
factors, terrain variables, accessibility, and solar resource data to
identify candidate zones while excluding ecologically sensitive and
legally restricted areas.

## Motivation

Peatlands in South Sumatra experience recurring fire events, seasonal
flooding, drainage-related land subsidence, and widespread degradation from
past land conversion. The region also has meaningful solar irradiance
potential. This project asks whether degraded peat areas can serve as
candidate zones for agrivoltaic development — combining solar energy
production with paludiculture — without promoting encroachment into intact
or protected peat ecosystems.

## Analytical approach

The workflow uses an Analytic Hierarchy Process (AHP) to derive criterion
weights from expert-informed pairwise comparisons, followed by Weighted
Linear Combination (WLC) to integrate eight spatially explicit criteria
into a composite suitability index. Hard constraints (protected areas,
intact peat, restricted land cover classes) are applied as binary
exclusion masks before final classification.

## Study area

South Sumatra province, Indonesia. The analysis domain is restricted to
the degraded peatland extent within the province.

## Main output

A 30 m resolution suitability raster classified into four levels, with
the highest-suitability class covering approximately 66,665 ha of degraded
peatland after constraint exclusions.

## Intended use

This is a first-pass spatial screening tool intended to support planning
prioritisation and field validation scoping. It is not a substitute for
site-level geotechnical assessment, hydrological modelling, land tenure
review, or grid connection feasibility analysis.
