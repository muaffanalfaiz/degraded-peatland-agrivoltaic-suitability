# GitHub upload guide

This guide assumes you are on Windows and already have:
- a GitHub account
- Git for Windows installed
- this repository folder downloaded and extracted

## 1. Create the repository on GitHub
1. Go to GitHub.
2. Click **New repository**.
3. Repository name: `degraded-peatland-agrivoltaic-suitability`
4. Description:
   `GIS–MCDA-based land suitability analysis for agrivoltaic development on degraded peatlands in South Sumatra`
5. Choose **Public**.
6. Do **not** add README, .gitignore, or license from GitHub, because this package already includes them.
7. Click **Create repository**.

## 2. Put your files in the folder
Inside this package:
- keep the current structure
- replace placeholders where needed
- optionally add your sanitized `.aprx` later to `arcgis-pro/`

## 3. Open terminal in the folder
On Windows:
- open the extracted folder
- right-click in the folder
- choose **Open in Terminal** or **Git Bash Here**

## 4. Run these commands

```bash
git init
git branch -M main
git add .
git commit -m "Initial public repo scaffold for degraded peatland agrivoltaic suitability project"
git remote add origin https://github.com/YOUR_USERNAME/degraded-peatland-agrivoltaic-suitability.git
git push -u origin main
```

## 5. If Git asks for login
Use your normal GitHub sign-in flow or personal access token if prompted.

## 6. Recommended first commit only
For your first push, keep it simple:
- docs
- figures
- tables
- README
- guides

Then later make a second commit for:
- cleaned `.aprx`
- scripts
- metadata inventory

## 7. Suggested second commit
```bash
git add arcgis-pro scripts data/metadata
git commit -m "Add ArcGIS Pro project notes and ArcPy reconstruction scaffold"
git push
```

## 8. Suggested repository description
Use this on GitHub:
`GIS–MCDA-based land suitability analysis for agrivoltaic development on degraded peatlands in South Sumatra`

## 9. Suggested topics
Add these GitHub topics:
- gis
- arcgis-pro
- mcda
- ahp
- agrivoltaic
- peatland
- indonesia
- solar-siting
- environmental-planning

## 10. Suggested featured sections in README
Pin these outputs at the top of the GitHub page:
- final suitability map
- fire risk map
- degraded peat mask
- criteria weights table

## 11. If you want to upload with GitHub Desktop instead
1. Create the repo on GitHub first.
2. Open GitHub Desktop.
3. Add local repository.
4. Select this extracted folder.
5. Publish repository as public.
6. Push the first commit.

## 12. Final reminder
Do not upload the manuscript DOCX yet unless you are sure journal policy allows it.
