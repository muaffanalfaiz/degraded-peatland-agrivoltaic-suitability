# Interactive Dashboard

A lightweight static dashboard for exploring the agrivoltaic suitability
analysis results.

## Files

| File | Description |
|------|-------------|
| `index.html` | Main entry point — open in any modern browser |
| `app.jsx` | React component source |

## Usage

Open `index.html` directly in a browser for a static preview of the
suitability classification outputs and criterion weights.

For local development with live reload, serve the folder with any static
server, for example:

```
python -m http.server 8000
```

then navigate to `http://localhost:8000`.

## Contents

The dashboard presents a summary of the four-class suitability
classification, AHP criterion weights, and area statistics derived from
the GIS–MCDA analysis.
