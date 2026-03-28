# Dashboard

Interactive project dashboard for the degraded peatland agrivoltaic suitability analysis.

## Contents

- `app.jsx` — Standalone React component with three tabs: Overview, Criteria, and Maps

## What it shows

- Key result metrics (eligible domain, suitability percentages, AHP consistency)
- Suitability class distribution (donut chart)
- Peatland domain context and screening funnel
- Analytical pipeline steps
- AHP criterion weights (bar chart and radar profile)
- Full criteria reference table with data sources
- Switchable map explorer for all 12 thematic layers

## How to preview

**Option 1 — Claude.ai**: Copy the contents of `app.jsx` into a Claude.ai conversation and ask it to render the artifact.

**Option 2 — Local React environment**: Drop `app.jsx` into any React project. The component requires `recharts` as a dependency. Map images are loaded from this repository via GitHub raw URLs.

## Dependencies

- React 18+
- recharts
- Google Fonts: DM Sans, JetBrains Mono (loaded via CDN)
