import { useState } from "react";
import {
  PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip,
  ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis,
  PolarRadiusAxis, Radar,
} from "recharts";

const BASE = "https://raw.githubusercontent.com/muaffanalfaiz/degraded-peatland-agrivoltaic-suitability/main/outputs/figures";

const suitabilityData = [
  { name: "Very Low", area_ha: 2065.68, pct: 1.67, color: "#d4451a" },
  { name: "Low", area_ha: 24408.99, pct: 19.69, color: "#e8a735" },
  { name: "Moderate", area_ha: 30867.84, pct: 24.89, color: "#a3c94a" },
  { name: "Highly Suitable", area_ha: 66665.25, pct: 53.76, color: "#2d8a4e" },
];

const weightsData = [
  { criterion: "Fire Hazard", weight: 0.1965, pct: 19.65, type: "Risk", short: "Fire" },
  { criterion: "Peat Depth", weight: 0.1781, pct: 17.81, type: "Risk", short: "Peat" },
  { criterion: "Flood Vulnerability", weight: 0.1599, pct: 15.99, type: "Risk", short: "Flood" },
  { criterion: "Slope", weight: 0.1412, pct: 14.12, type: "Terrain", short: "Slope" },
  { criterion: "Road Access", weight: 0.1216, pct: 12.16, type: "Access", short: "Roads" },
  { criterion: "Solar (GHI)", weight: 0.1099, pct: 10.99, type: "Solar", short: "GHI" },
  { criterion: "Aspect", weight: 0.0573, pct: 5.73, type: "Terrain", short: "Aspect" },
  { criterion: "TPI", weight: 0.0355, pct: 3.55, type: "Terrain", short: "TPI" },
];

const radarData = weightsData.map((w) => ({ criterion: w.short, weight: w.pct, fullMark: 25 }));

const mapLayers = [
  { id: "final", label: "Final Suitability", desc: "Classified suitability output — 4 planning classes", img: `${BASE}/12_final_suitability_map.jpg` },
  { id: "fire", label: "Fire Risk", desc: "FRP-weighted kernel density from NASA FIRMS VIIRS hotspots", img: `${BASE}/10_fire_risk_map.jpg` },
  { id: "peat", label: "Peat Depth", desc: "Peat thickness / geotechnical proxy from BBSDLP", img: `${BASE}/02_peat_thickness_map.jpg` },
  { id: "flood", label: "Flood Index", desc: "Flood vulnerability index from BNPB InaRISK", img: `${BASE}/11_flood_vulnerability_map.jpg` },
  { id: "slope", label: "Slope", desc: "Terrain gradient derived from BIG DEM", img: `${BASE}/03_slope_map.jpg` },
  { id: "roads", label: "Road Access", desc: "Euclidean distance to roads from OpenStreetMap", img: `${BASE}/09_distance_to_road_map.jpg` },
  { id: "ghi", label: "Solar (GHI)", desc: "Global Horizontal Irradiance from Global Solar Atlas v2", img: `${BASE}/01_ghi_map.jpg` },
  { id: "aspect", label: "Aspect", desc: "Terrain orientation derived from BIG DEM", img: `${BASE}/07_aspect_map.jpg` },
  { id: "tpi", label: "TPI", desc: "Topographic Position Index derived from BIG DEM", img: `${BASE}/05_tpi_map.jpg` },
  { id: "constraints", label: "Protected Areas", desc: "WDPA hard constraint exclusion zones", img: `${BASE}/06_wdpa_constraints_map.jpg` },
  { id: "peat_mask", label: "Peat Mask", desc: "Degraded peatland domain boundary", img: `${BASE}/08_degraded_peat_mask.jpg` },
  { id: "landcover", label: "Land Cover", desc: "Forest / non-forest contextual layer", img: `${BASE}/04_land_cover_map.jpg` },
];

/* ---- Tooltip components ---- */
const TipBar = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div style={{ background: "#0d1117", border: "1px solid #2a3a2a", borderRadius: 8, padding: "10px 14px", color: "#c9d6c0" }}>
      <p style={{ margin: 0, fontWeight: 700, color: "#e8f0e4" }}>{d.criterion}</p>
      <p style={{ margin: "4px 0 0", fontSize: 13 }}>Weight: {(d.weight * 100).toFixed(2)}%</p>
      <p style={{ margin: "2px 0 0", fontSize: 12, opacity: 0.7 }}>Category: {d.type}</p>
    </div>
  );
};

const TipPie = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div style={{ background: "#0d1117", border: "1px solid #2a3a2a", borderRadius: 8, padding: "10px 14px", color: "#c9d6c0" }}>
      <p style={{ margin: 0, fontWeight: 700, color: "#e8f0e4" }}>{d.name}</p>
      <p style={{ margin: "4px 0 0", fontSize: 13 }}>{d.area_ha?.toLocaleString()} ha ({d.pct}%)</p>
    </div>
  );
};

/* ---- Reusable components ---- */
const StatCard = ({ label, value, sub, accent }) => (
  <div style={{
    background: "linear-gradient(135deg, #0f1a14 0%, #142018 100%)",
    border: "1px solid #1e3028", borderRadius: 12, padding: "20px 22px",
    flex: "1 1 180px", minWidth: 155,
  }}>
    <div style={{ fontSize: 10, textTransform: "uppercase", letterSpacing: "0.12em", color: "#5a7a62", fontWeight: 600, marginBottom: 6 }}>{label}</div>
    <div style={{ fontSize: 26, fontWeight: 800, color: accent || "#7dcea0", lineHeight: 1.1, fontFamily: "'DM Sans', sans-serif" }}>{value}</div>
    {sub && <div style={{ fontSize: 11, color: "#4a6a52", marginTop: 4 }}>{sub}</div>}
  </div>
);

const Sec = ({ children, tag }) => (
  <div style={{ marginBottom: 16, display: "flex", alignItems: "center", gap: 12 }}>
    {tag && <span style={{ fontSize: 10, textTransform: "uppercase", letterSpacing: "0.15em", background: "#1a2e22", color: "#5daa78", padding: "3px 10px", borderRadius: 4, fontWeight: 700, whiteSpace: "nowrap" }}>{tag}</span>}
    <h2 style={{ margin: 0, fontSize: 17, fontWeight: 700, color: "#d4e8d0", fontFamily: "'DM Sans', sans-serif" }}>{children}</h2>
    <div style={{ flex: 1, height: 1, background: "linear-gradient(90deg, #1e3028, transparent)" }} />
  </div>
);

const barFill = (t) => t === "Risk" ? "#e05a3a" : t === "Terrain" ? "#5daa78" : t === "Access" ? "#d4a03a" : "#4a9aca";

/* ======== Main Dashboard ======== */
export default function Dashboard() {
  const [tab, setTab] = useState("overview");
  const [layer, setLayer] = useState("final");
  const [imgLoaded, setImgLoaded] = useState({});

  const activeMap = mapLayers.find((l) => l.id === layer);

  return (
    <div style={{ minHeight: "100vh", background: "#080e0b", color: "#c9d6c0", fontFamily: "'DM Sans', 'Segoe UI', sans-serif", fontSize: 14, lineHeight: 1.5 }}>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />

      {/* ── Header ── */}
      <header style={{
        borderBottom: "1px solid #152018", padding: "14px 24px",
        display: "flex", alignItems: "center", justifyContent: "space-between",
        background: "linear-gradient(180deg, #0a120e, #080e0b)", position: "sticky", top: 0, zIndex: 100,
        flexWrap: "wrap", gap: 10,
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{
            width: 34, height: 34, borderRadius: 8,
            background: "linear-gradient(135deg, #2d8a4e, #1a5a30)",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 14, fontWeight: 800, color: "#e8f0e4",
          }}>AV</div>
          <div>
            <div style={{ fontWeight: 700, fontSize: 14, color: "#e8f0e4" }}>Degraded Peatland Agrivoltaic Suitability</div>
            <div style={{ fontSize: 10, color: "#4a6a52" }}>South Sumatra, Indonesia — GIS-MCDA Portfolio Project</div>
          </div>
        </div>
        <div style={{ display: "flex", gap: 2, background: "#0d1610", borderRadius: 8, padding: 3 }}>
          {["overview", "criteria", "maps"].map((t) => (
            <button key={t} onClick={() => setTab(t)} style={{
              padding: "6px 16px", borderRadius: 6, border: "none", cursor: "pointer",
              fontSize: 11, fontWeight: 600, textTransform: "capitalize",
              background: tab === t ? "#1a2e22" : "transparent",
              color: tab === t ? "#7dcea0" : "#4a6a52",
              transition: "all 0.2s",
            }}>{t}</button>
          ))}
        </div>
      </header>

      <main style={{ padding: "22px 24px", maxWidth: 1140, margin: "0 auto" }}>

        {/* ════════════ OVERVIEW ════════════ */}
        {tab === "overview" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 22 }}>
            {/* KPIs */}
            <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
              <StatCard label="Eligible Domain" value="124,008 ha" sub="After constraint exclusion" accent="#7dcea0" />
              <StatCard label="Highly Suitable" value="53.76%" sub="66,665 ha identified" accent="#2d8a4e" />
              <StatCard label="Mod + High" value="78.65%" sub="97,533 ha combined" accent="#a3c94a" />
              <StatCard label="AHP Consistency" value="CR 0.002" sub="Well below 0.10" accent="#4a9aca" />
            </div>

            {/* Charts row */}
            <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
              {/* Donut */}
              <div style={{ flex: "1 1 320px", background: "linear-gradient(135deg, #0f1a14, #142018)", border: "1px solid #1e3028", borderRadius: 12, padding: 20 }}>
                <Sec tag="Result">Suitability Distribution</Sec>
                <ResponsiveContainer width="100%" height={240}>
                  <PieChart>
                    <Pie data={suitabilityData} cx="50%" cy="50%" innerRadius={50} outerRadius={90} dataKey="area_ha" paddingAngle={3} stroke="none">
                      {suitabilityData.map((e, i) => <Cell key={i} fill={e.color} />)}
                    </Pie>
                    <Tooltip content={<TipPie />} />
                  </PieChart>
                </ResponsiveContainer>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 8, justifyContent: "center", marginTop: 4 }}>
                  {suitabilityData.map((s, i) => (
                    <div key={i} style={{ display: "flex", alignItems: "center", gap: 5, fontSize: 11 }}>
                      <span style={{ width: 10, height: 10, borderRadius: 3, background: s.color, display: "inline-block" }} />
                      <span style={{ color: "#8aa88e" }}>{s.name}</span>
                      <span style={{ color: "#5a7a62", fontFamily: "'JetBrains Mono', monospace", fontSize: 10 }}>{s.pct}%</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Peatland context */}
              <div style={{ flex: "1 1 320px", background: "linear-gradient(135deg, #0f1a14, #142018)", border: "1px solid #1e3028", borderRadius: 12, padding: 20 }}>
                <Sec tag="Context">Peatland Domain</Sec>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, marginBottom: 6, color: "#6a8a72" }}>
                  <span>Total peatland</span>
                  <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 10 }}>1,092,142 ha</span>
                </div>
                <div style={{ height: 28, borderRadius: 6, overflow: "hidden", display: "flex", background: "#0a120e", marginBottom: 18 }}>
                  <div style={{ width: "78.9%", background: "linear-gradient(90deg, #1a3a2a, #1e4430)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 10, fontWeight: 600, color: "#5daa78" }}>Intact — 78.9%</div>
                  <div style={{ width: "21.1%", background: "linear-gradient(90deg, #8a6540, #c4956a)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 10, fontWeight: 600, color: "#1a0e05" }}>Degraded</div>
                </div>
                {[
                  { label: "Total peatland", val: "1,092,142 ha", w: 100 },
                  { label: "Degraded subset", val: "230,810 ha", w: 55 },
                  { label: "After constraints", val: "124,008 ha", w: 30 },
                  { label: "Mod + High suitable", val: "97,533 ha", w: 23 },
                ].map((f, i) => (
                  <div key={i} style={{ marginBottom: 8 }}>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: "#6a8a72", marginBottom: 3 }}>
                      <span>{f.label}</span>
                      <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 10 }}>{f.val}</span>
                    </div>
                    <div style={{ height: 5, borderRadius: 3, background: "#0a120e" }}>
                      <div style={{ width: `${f.w}%`, height: "100%", borderRadius: 3, background: `linear-gradient(90deg, #2d8a4e, #1a5a30)`, opacity: 0.35 + i * 0.2 }} />
                    </div>
                  </div>
                ))}
                <div style={{ marginTop: 12, padding: "8px 12px", background: "#0a120e", borderRadius: 6, border: "1px solid #152018", fontSize: 10, color: "#4a6a52", lineHeight: 1.6 }}>
                  Only degraded peatland was analyzed. The framework avoids incentivizing conversion of intact peat ecosystems.
                </div>
              </div>
            </div>

            {/* Method pipeline */}
            <div style={{ background: "linear-gradient(135deg, #0f1a14, #142018)", border: "1px solid #1e3028", borderRadius: 12, padding: 20 }}>
              <Sec tag="Method">Analytical Pipeline</Sec>
              <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
                {[
                  { s: "01", t: "Define Domain", d: "Degraded peatland mask within South Sumatra" },
                  { s: "02", t: "Apply Constraints", d: "WDPA protected areas excluded" },
                  { s: "03", t: "Score Criteria", d: "8 layers normalized to 0\u20131 scale" },
                  { s: "04", t: "AHP Weighting", d: "Pairwise comparison (CR = 0.002)" },
                  { s: "05", t: "WLC Overlay", d: "Weighted suitability index" },
                  { s: "06", t: "Classify", d: "4 planning classes at 0.25 intervals" },
                ].map((step, i) => (
                  <div key={i} style={{ flex: "1 1 150px", padding: "12px 14px", background: "#0a120e", borderRadius: 8, border: "1px solid #152018" }}>
                    <div style={{ fontSize: 10, fontWeight: 700, color: "#2d8a4e", fontFamily: "'JetBrains Mono', monospace", marginBottom: 3 }}>STEP {step.s}</div>
                    <div style={{ fontSize: 12, fontWeight: 700, color: "#c9d6c0", marginBottom: 3 }}>{step.t}</div>
                    <div style={{ fontSize: 10, color: "#4a6a52", lineHeight: 1.5 }}>{step.d}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Preview map thumbnail */}
            <div style={{ background: "linear-gradient(135deg, #0f1a14, #142018)", border: "1px solid #1e3028", borderRadius: 12, padding: 20 }}>
              <Sec tag="Output">Final Suitability Map</Sec>
              <div style={{ borderRadius: 8, overflow: "hidden", border: "1px solid #1e3028", background: "#0a120e" }}>
                <img src={`${BASE}/12_final_suitability_map.jpg`} alt="Final Suitability Map" style={{ width: "100%", display: "block", opacity: imgLoaded["overview_final"] ? 1 : 0.3, transition: "opacity 0.4s" }} onLoad={() => setImgLoaded((p) => ({ ...p, overview_final: true }))} />
              </div>
              <div style={{ marginTop: 10, fontSize: 11, color: "#4a6a52", textAlign: "center" }}>
                See the <span onClick={() => setTab("maps")} style={{ color: "#5daa78", cursor: "pointer", textDecoration: "underline" }}>Maps tab</span> to explore all 12 thematic layers
              </div>
            </div>
          </div>
        )}

        {/* ════════════ CRITERIA ════════════ */}
        {tab === "criteria" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 22 }}>
            <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
              {/* Bar chart */}
              <div style={{ flex: "1 1 460px", background: "linear-gradient(135deg, #0f1a14, #142018)", border: "1px solid #1e3028", borderRadius: 12, padding: 20 }}>
                <Sec tag="AHP">Criterion Weights</Sec>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={weightsData} layout="vertical" margin={{ left: 10, right: 20, top: 5, bottom: 5 }}>
                    <XAxis type="number" domain={[0, 22]} tick={{ fill: "#4a6a52", fontSize: 10 }} tickFormatter={(v) => `${v}%`} axisLine={{ stroke: "#1e3028" }} />
                    <YAxis type="category" dataKey="criterion" width={115} tick={{ fill: "#8aa88e", fontSize: 11 }} axisLine={false} tickLine={false} />
                    <Tooltip content={<TipBar />} cursor={{ fill: "rgba(45,138,78,0.08)" }} />
                    <Bar dataKey="pct" radius={[0, 6, 6, 0]} barSize={20}>
                      {weightsData.map((e, i) => <Cell key={i} fill={barFill(e.type)} />)}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
                <div style={{ display: "flex", gap: 14, justifyContent: "center", marginTop: 6 }}>
                  {[{ l: "Risk", c: "#e05a3a" }, { l: "Terrain", c: "#5daa78" }, { l: "Access", c: "#d4a03a" }, { l: "Solar", c: "#4a9aca" }].map((x, i) => (
                    <div key={i} style={{ display: "flex", alignItems: "center", gap: 5, fontSize: 11 }}>
                      <span style={{ width: 8, height: 8, borderRadius: 2, background: x.c, display: "inline-block" }} />
                      <span style={{ color: "#6a8a72" }}>{x.l}</span>
                    </div>
                  ))}
                </div>
              </div>
              {/* Radar */}
              <div style={{ flex: "1 1 300px", background: "linear-gradient(135deg, #0f1a14, #142018)", border: "1px solid #1e3028", borderRadius: 12, padding: 20 }}>
                <Sec tag="Profile">Weight Radar</Sec>
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={radarData} cx="50%" cy="50%" outerRadius="68%">
                    <PolarGrid stroke="#1e3028" />
                    <PolarAngleAxis dataKey="criterion" tick={{ fill: "#6a8a72", fontSize: 11 }} />
                    <PolarRadiusAxis angle={90} domain={[0, 25]} tick={false} axisLine={false} />
                    <Radar dataKey="weight" stroke="#2d8a4e" fill="#2d8a4e" fillOpacity={0.25} strokeWidth={2} />
                  </RadarChart>
                </ResponsiveContainer>
                <div style={{ padding: "8px 12px", background: "#0a120e", borderRadius: 6, border: "1px solid #152018", fontSize: 11, color: "#5a7a62", textAlign: "center", marginTop: 6 }}>
                  Risk-first: 53.5% of weight on fire + peat + flood
                </div>
              </div>
            </div>

            {/* Table */}
            <div style={{ background: "linear-gradient(135deg, #0f1a14, #142018)", border: "1px solid #1e3028", borderRadius: 12, padding: 20, overflowX: "auto" }}>
              <Sec tag="Detail">Criteria Reference</Sec>
              <table style={{ width: "100%", borderCollapse: "separate", borderSpacing: "0 4px", fontSize: 12 }}>
                <thead>
                  <tr>
                    {["Criterion", "Weight", "Direction", "Data Source"].map((h) => (
                      <th key={h} style={{ textAlign: "left", padding: "8px 12px", color: "#4a6a52", fontSize: 10, textTransform: "uppercase", letterSpacing: "0.1em", fontWeight: 600, borderBottom: "1px solid #1e3028" }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {[
                    ["Fire Hazard (FRP-weighted KDE)", "0.1965", "Cost", "NASA FIRMS (VIIRS 375 m)"],
                    ["Peat Depth / Proxy", "0.1781", "Cost", "BBSDLP / Ministry of Agriculture"],
                    ["Flood Vulnerability Index", "0.1599", "Cost", "BNPB InaRISK Geoservices"],
                    ["Slope", "0.1412", "Benefit*", "BIG DEM"],
                    ["Distance to Roads", "0.1216", "Benefit", "OpenStreetMap / Geofabrik"],
                    ["Global Horizontal Irradiance", "0.1099", "Benefit", "Global Solar Atlas v2"],
                    ["Aspect", "0.0573", "Benefit*", "BIG DEM"],
                    ["Topographic Position Index", "0.0355", "Benefit*", "BIG DEM"],
                  ].map((row, i) => (
                    <tr key={i} style={{ background: i % 2 === 0 ? "#0c1610" : "transparent" }}>
                      {row.map((cell, j) => (
                        <td key={j} style={{
                          padding: "10px 12px",
                          color: j === 0 ? "#c9d6c0" : j === 1 ? "#7dcea0" : "#6a8a72",
                          fontFamily: j === 1 ? "'JetBrains Mono', monospace" : "inherit",
                          fontWeight: j === 0 ? 600 : 400,
                          borderRadius: j === 0 ? "6px 0 0 6px" : j === 3 ? "0 6px 6px 0" : 0,
                        }}>{cell}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
              <div style={{ fontSize: 10, color: "#3a5a42", marginTop: 8, fontStyle: "italic" }}>* Benefit after scoring — normalized via distance-to-target function</div>
            </div>
          </div>
        )}

        {/* ════════════ MAPS ════════════ */}
        {tab === "maps" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
            <Sec tag="Spatial">Thematic Map Explorer</Sec>

            {/* Layer selector grid */}
            <div style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(120px, 1fr))",
              gap: 6, background: "#0d1610", borderRadius: 10, padding: 8,
              border: "1px solid #152018",
            }}>
              {mapLayers.map((l) => (
                <button key={l.id} onClick={() => setLayer(l.id)} style={{
                  padding: "10px 8px", borderRadius: 6, border: layer === l.id ? "1px solid #2d6a3e" : "1px solid transparent",
                  cursor: "pointer", fontSize: 11, fontWeight: 600, textAlign: "center",
                  background: layer === l.id ? "#1a3a26" : "transparent",
                  color: layer === l.id ? "#7dcea0" : "#4a6a52",
                  transition: "all 0.15s",
                  lineHeight: 1.3,
                }}>
                  {l.label}
                </button>
              ))}
            </div>

            {/* Active map display */}
            <div style={{
              background: "linear-gradient(135deg, #0f1a14, #142018)",
              border: "1px solid #1e3028", borderRadius: 12, padding: 20,
            }}>
              {/* Map header */}
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 14, flexWrap: "wrap", gap: 8 }}>
                <div>
                  <h3 style={{ margin: 0, fontSize: 16, fontWeight: 700, color: "#d4e8d0" }}>{activeMap.label}</h3>
                  <p style={{ margin: "4px 0 0", fontSize: 12, color: "#5a7a62" }}>{activeMap.desc}</p>
                </div>
                <div style={{ display: "flex", gap: 8 }}>
                  {weightsData.find((w) => w.short === (activeMap.id === "ghi" ? "GHI" : activeMap.id === "fire" ? "Fire" : activeMap.id === "peat" ? "Peat" : activeMap.id === "flood" ? "Flood" : activeMap.id === "slope" ? "Slope" : activeMap.id === "roads" ? "Roads" : activeMap.id === "aspect" ? "Aspect" : activeMap.id === "tpi" ? "TPI" : null)) && (
                    <span style={{
                      fontSize: 10, padding: "4px 10px", borderRadius: 4,
                      background: "#0a120e", border: "1px solid #1e3028",
                      color: "#7dcea0", fontFamily: "'JetBrains Mono', monospace",
                    }}>
                      w = {weightsData.find((w) => w.short === (activeMap.id === "ghi" ? "GHI" : activeMap.id === "fire" ? "Fire" : activeMap.id === "peat" ? "Peat" : activeMap.id === "flood" ? "Flood" : activeMap.id === "slope" ? "Slope" : activeMap.id === "roads" ? "Roads" : activeMap.id === "aspect" ? "Aspect" : activeMap.id === "tpi" ? "TPI" : null))?.weight}
                    </span>
                  )}
                </div>
              </div>

              {/* The map image */}
              <div style={{
                borderRadius: 8, overflow: "hidden", border: "1px solid #1e3028",
                background: "#0a120e", position: "relative", minHeight: 200,
              }}>
                {!imgLoaded[layer] && (
                  <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", color: "#3a5a42", fontSize: 12 }}>
                    Loading map...
                  </div>
                )}
                <img
                  key={layer}
                  src={activeMap.img}
                  alt={activeMap.label}
                  style={{
                    width: "100%", display: "block",
                    opacity: imgLoaded[layer] ? 1 : 0,
                    transition: "opacity 0.4s ease",
                  }}
                  onLoad={() => setImgLoaded((p) => ({ ...p, [layer]: true }))}
                />
              </div>
            </div>

            {/* Map metadata strip */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(150px, 1fr))", gap: 8 }}>
              {[
                { l: "Projection", v: "WGS 84 / UTM 48S" },
                { l: "EPSG", v: "32748" },
                { l: "Cell Size", v: "30 m" },
                { l: "Software", v: "ArcGIS Pro" },
                { l: "Weighting", v: "AHP + WLC" },
                { l: "Classes", v: "4-class output" },
              ].map((m, i) => (
                <div key={i} style={{ background: "#0c1610", borderRadius: 8, padding: "10px 14px", border: "1px solid #152018" }}>
                  <div style={{ fontSize: 9, color: "#3a5a42", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 2 }}>{m.l}</div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: "#8aa88e" }}>{m.v}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* ── Footer ── */}
      <footer style={{
        borderTop: "1px solid #152018", padding: "14px 24px",
        display: "flex", justifyContent: "space-between", alignItems: "center",
        fontSize: 11, color: "#3a5a42", marginTop: 32, flexWrap: "wrap", gap: 8,
      }}>
        <span>Muaffan Alfaiz Wisaksono — Lincoln University</span>
        <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 10 }}>EPSG:32748 · 30 m · AHP-WLC · MIT License</span>
      </footer>
    </div>
  );
}
