"""
Project FORESIGHT — Executive Retail Analytics Dashboard
Built with Streamlit + Plotly. Dark, glassmorphic, Power-BI-executive style.

DATA CONTRACT (do not invent columns, do not break this):
  data/processed/dashboard_monthly.csv    -> InvoiceDate, Revenue
  data/processed/dashboard_products.csv   -> Description, Revenue
  data/processed/dashboard_country.csv    -> Country, Revenue
  data/processed/dashboard_customers.csv  -> Customer ID, Revenue
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Project FORESIGHT | Executive Dashboard",
    page_icon="https://kommodo.ai/i/nIr8j3ZfwoC2uy8nvw7V",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 2. COLOR PALETTE / DESIGN TOKENS
# ============================================================
BG_DARK = "#0B0E14"
BG_PANEL = "#11151C"
GLASS_BG = "rgba(255, 255, 255, 0.04)"
GLASS_BORDER = "rgba(255, 255, 255, 0.08)"
TEXT_PRIMARY = "#F5F6FA"
TEXT_MUTED = "#8B93A7"
ACCENT_1 = "#6C63FF"   # indigo
ACCENT_2 = "#00D9FF"   # cyan
ACCENT_3 = "#FF6584"   # rose (for negative / alerts)
ACCENT_4 = "#2EE6A6"   # green (for positive)
GRADIENT_MAIN = f"linear-gradient(135deg, {ACCENT_1} 0%, {ACCENT_2} 100%)"
CHART_COLORWAY = [ACCENT_2, ACCENT_1, ACCENT_4, ACCENT_3, "#FFB84C", "#B892FF", "#4CC9F0", "#F72585"]

# ============================================================
# 3. GLOBAL CSS — dark theme, glassmorphism, typography, hides
#    Streamlit branding, hover animations, section dividers
# ============================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@600;700;800&display=swap');

/* ---------- Base ---------- */
html, body, [class*="css"]  {{
    font-family: 'Inter', sans-serif;
}}
.stApp {{
    background: radial-gradient(circle at 15% 0%, #131826 0%, {BG_DARK} 45%, #05070A 100%);
    color: {TEXT_PRIMARY};
}}

/* ---------- Hide Streamlit branding ---------- */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}
div[data-testid="stDecoration"] {{display: none;}}
div[data-testid="stToolbar"] {{display: none;}}
a[href*="streamlit.io"] {{display: none !important;}}
.viewerBadge_container__1QSob {{display: none !important;}}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0D1119 0%, #090B10 100%);
    border-right: 1px solid {GLASS_BORDER};
}}
section[data-testid="stSidebar"] * {{
    color: {TEXT_PRIMARY};
}}

/* ---------- Headings ---------- */
h1, h2, h3, h4 {{
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    letter-spacing: -0.02em;
}}

/* ---------- Glass card ---------- */
.glass-card {{
    background: {GLASS_BG};
    border: 1px solid {GLASS_BORDER};
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-radius: 16px;
    padding: 22px 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border 0.25s ease;
}}
.glass-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(108, 99, 255, 0.25);
    border: 1px solid rgba(108, 99, 255, 0.4);
}}

/* ---------- Header banner ---------- */
.hero-banner {{
    background: {GRADIENT_MAIN};
    border-radius: 20px;
    padding: 32px 36px;
    margin-bottom: 6px;
    box-shadow: 0 12px 40px rgba(108, 99, 255, 0.35);
}}
.hero-title {{
    font-family: 'Manrope', sans-serif;
    font-size: 34px;
    font-weight: 800;
    color: white;
    margin: 0;
}}
.hero-subtitle {{
    font-size: 15px;
    color: rgba(255,255,255,0.9);
    margin-top: 6px;
    font-weight: 500;
}}
.hero-meta {{
    font-size: 12.5px;
    color: rgba(255,255,255,0.75);
    margin-top: 10px;
}}

/* ---------- Section divider ---------- */
.section-divider {{
    height: 2px;
    border: none;
    margin: 34px 0 22px 0;
    background: linear-gradient(90deg, {ACCENT_1} 0%, {ACCENT_2} 50%, transparent 100%);
    opacity: 0.6;
}}
.section-label {{
    font-size: 13px;
    font-weight: 700;
    color: {TEXT_MUTED};
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 4px;
}}

/* ---------- Insight card ---------- */
.insight-card {{
    background: {GLASS_BG};
    border-left: 3px solid {ACCENT_2};
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 12px;
    font-size: 14.5px;
    color: {TEXT_PRIMARY};
    transition: border 0.2s ease, transform 0.2s ease;
}}
.insight-card:hover {{
    border-left: 3px solid {ACCENT_1};
    transform: translateX(4px);
}}
.insight-card b {{ color: {ACCENT_2}; }}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {{
    gap: 6px;
    background: {GLASS_BG};
    border-radius: 12px;
    padding: 6px;
    border: 1px solid {GLASS_BORDER};
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px;
    padding: 8px 18px;
    color: {TEXT_MUTED};
    font-weight: 600;
    font-size: 14px;
}}
.stTabs [aria-selected="true"] {{
    background: {GRADIENT_MAIN} !important;
    color: white !important;
}}

/* ---------- Buttons ---------- */
.stDownloadButton button, .stButton button {{
    background: {GRADIENT_MAIN};
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 8px 18px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.stDownloadButton button:hover, .stButton button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(108, 99, 255, 0.4);
}}

/* ---------- Footer ---------- */
.footer-box {{
    text-align: center;
    padding: 22px 0 10px 0;
    color: {TEXT_MUTED};
    font-size: 13px;
    border-top: 1px solid {GLASS_BORDER};
    margin-top: 30px;
}}
/* ---------- Left nav (anchor-scroll, not fake multi-page) ---------- */
.nav-link {{
    display: flex; align-items: center; gap: 10px;
    padding: 9px 14px; border-radius: 10px;
    color: {TEXT_MUTED} !important; text-decoration: none !important;
    font-weight: 600; font-size: 14px; margin-bottom: 4px;
    transition: background 0.2s ease, color 0.2s ease;
}}
.nav-link:hover {{ background: {GLASS_BG}; color: {TEXT_PRIMARY} !important; }}

/* ---------- Top bar (mockup-style header row) ---------- */
.top-bar {{
    display: flex; justify-content: space-between; align-items: flex-end;
    flex-wrap: wrap; gap: 16px; padding: 6px 2px 18px 2px;
}}
.top-bar-greeting {{ font-size: 14px; color: {TEXT_MUTED}; margin-bottom: 2px; }}
.top-bar-title {{
    font-family: 'Manrope', sans-serif; font-size: 30px; font-weight: 800; margin: 0;
}}
.top-bar-subtitle {{ font-size: 14px; color: {TEXT_MUTED}; margin-top: 2px; }}
.top-bar-meta {{ font-size: 12px; color: {TEXT_MUTED}; margin-top: 6px; }}

/* ---------- KPI delta text ---------- */
.kpi-delta-up {{ color: {ACCENT_4}; font-size: 12.5px; font-weight: 600; }}
.kpi-delta-down {{ color: {ACCENT_3}; font-size: 12.5px; font-weight: 600; }}

/* ---------- Badge-style insight card (matches mockup) ---------- */
.badge-card {{
    display: flex; gap: 14px; align-items: flex-start;
    background: {GLASS_BG}; border: 1px solid {GLASS_BORDER};
    border-radius: 14px; padding: 14px 16px; margin-bottom: 12px;
    transition: transform 0.2s ease, border 0.2s ease;
}}
.badge-card:hover {{ transform: translateX(4px); border: 1px solid rgba(108,99,255,0.4); }}
.badge-icon {{
    width: 38px; height: 38px; min-width: 38px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center; font-size: 18px;
}}
.badge-text {{ font-size: 13.5px; line-height: 1.4; }}
.badge-text b {{ display: block; color: {TEXT_PRIMARY}; font-size: 14.5px; margin-bottom: 2px; }}

/* ---------- Status indicator (live pulse) ---------- */
.status-pill {{
    display: inline-flex; align-items: center; gap: 7px;
    padding: 5px 12px; border-radius: 999px;
    background: rgba(46, 230, 166, 0.12); border: 1px solid rgba(46, 230, 166, 0.3);
    font-size: 12px; font-weight: 600; color: {ACCENT_4};
}}
.status-dot {{
    width: 7px; height: 7px; border-radius: 50%; background: {ACCENT_4};
    box-shadow: 0 0 0 0 rgba(46, 230, 166, 0.6);
    animation: pulse 2s infinite;
}}
@keyframes pulse {{
    0%   {{ box-shadow: 0 0 0 0 rgba(46, 230, 166, 0.55); }}
    70%  {{ box-shadow: 0 0 0 7px rgba(46, 230, 166, 0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(46, 230, 166, 0); }}
}}

/* ---------- Logo mark (header brand placeholder) ---------- */
.logo-mark {{
    width: 40px; height: 40px; border-radius: 11px;
    background: {GRADIENT_MAIN}; display: flex; align-items: center;
    justify-content: center; font-size: 19px; flex-shrink: 0;
    box-shadow: 0 6px 16px rgba(108, 99, 255, 0.4);
}}

/* ---------- Sidebar quick-stat blocks ---------- */
.quick-stat {{
    background: {GLASS_BG}; border: 1px solid {GLASS_BORDER}; border-radius: 10px;
    padding: 10px 12px; margin-bottom: 8px;
}}
.quick-stat-label {{ font-size: 11px; color: {TEXT_MUTED}; text-transform: uppercase; letter-spacing: 0.06em; }}
.quick-stat-value {{ font-size: 15px; font-weight: 700; color: {TEXT_PRIMARY}; margin-top: 2px; }}

/* ---------- Nicer "no time series" pill (was italic muted text) ---------- */
.kpi-delta-none {{
    display: inline-block; color: {TEXT_MUTED}; font-size: 11px; font-weight: 600;
    background: rgba(255,255,255,0.05); border-radius: 999px; padding: 3px 9px;
}}

/* ---------- Executive summary strip ---------- */
.exec-summary {{
    background: {GLASS_BG}; border: 1px solid {GLASS_BORDER}; border-radius: 14px;
    padding: 16px 20px; margin-bottom: 18px; font-size: 14px; line-height: 1.6;
    color: {TEXT_PRIMARY};
}}
.exec-summary b {{ color: {ACCENT_2}; }}

/* ---------- Footer link buttons ---------- */
.footer-links {{ display: flex; justify-content: center; gap: 10px; margin-top: 10px; flex-wrap: wrap; }}
.footer-link {{
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 14px; border-radius: 8px; font-size: 12.5px; font-weight: 600;
    background: {GLASS_BG}; border: 1px solid {GLASS_BORDER};
    color: {TEXT_PRIMARY} !important; text-decoration: none !important;
    transition: transform 0.2s ease, border 0.2s ease;
}}
.footer-link:hover {{ transform: translateY(-2px); border: 1px solid rgba(108,99,255,0.4); }}
.version-tag {{
    font-size: 11px; color: {TEXT_MUTED}; background: {GLASS_BG};
    border: 1px solid {GLASS_BORDER}; border-radius: 999px; padding: 2px 10px;
}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3b. SPARKLINE HELPER — inline SVG, no iframe, no JS dependency
# Only used for Revenue, because it's the only metric with a
# real underlying time series. Do NOT reuse this for
# Customers/Products/Countries — those are static totals with
# no time dimension, and a sparkline there would be fabricated.
# ============================================================
def make_sparkline_svg(values, color, width=110, height=32):
    values = [float(v) for v in values if pd.notna(v)]
    if len(values) < 2:
        return ""
    vmin, vmax = min(values), max(values)
    rng = (vmax - vmin) or 1
    step = width / (len(values) - 1)
    pts = " ".join(f"{i*step:.1f},{height - ((v - vmin) / rng * height):.1f}" for i, v in enumerate(values))
    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'xmlns="http://www.w3.org/2000/svg">'
        f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.2" '
        f'stroke-linecap="round" stroke-linejoin="round"/></svg>'
    )

# ============================================================
# 4. DATA LOADING (cached, read-only — no schema changes)
# ============================================================
REQUIRED_FILES = {
    "data/processed/dashboard_monthly.csv": ["InvoiceDate", "Revenue"],
    "data/processed/dashboard_products.csv": ["Description", "Revenue"],
    "data/processed/dashboard_country.csv": ["Country", "Revenue"],
    "data/processed/dashboard_customers.csv": ["Customer ID", "Revenue"],
}

def _fail(message: str):
    """Stop the app with a clear, actionable error instead of a raw traceback."""
    st.error(f"🚫 Dashboard failed to load\n\n{message}")
    st.stop()

@st.cache_data(show_spinner=False)
def load_data():
    frames = {}
    for path, required_cols in REQUIRED_FILES.items():
        if not os.path.exists(path):
            _fail(
                f"Missing file: `{path}`.\n\n"
                f"Check that your `data/processed/` folder exists and is populated "
                f"before running the dashboard."
            )
        try:
            df = pd.read_csv(path)
        except Exception as e:
            _fail(f"Could not read `{path}`: {e}")

        missing_cols = [c for c in required_cols if c not in df.columns]
        if missing_cols:
            _fail(
                f"File `{path}` is missing expected column(s): {missing_cols}.\n\n"
                f"Found columns: {list(df.columns)}.\n"
                f"This dashboard does not guess or invent columns — fix the source CSV."
            )
        frames[path] = df

    monthly = frames["data/processed/dashboard_monthly.csv"]
    products = frames["data/processed/dashboard_products.csv"]
    country = frames["data/processed/dashboard_country.csv"]
    customers = frames["data/processed/dashboard_customers.csv"]

    # Parse dates for trend/filter logic (does not alter Revenue/Description/etc.)
    monthly["InvoiceDate"] = pd.to_datetime(monthly["InvoiceDate"], errors="coerce")
    if monthly["InvoiceDate"].isna().any():
        st.sidebar.warning(
            f"⚠️ {monthly['InvoiceDate'].isna().sum()} row(s) in dashboard_monthly.csv "
            f"had an unparseable InvoiceDate and were excluded from trend charts."
        )
        monthly = monthly.dropna(subset=["InvoiceDate"])
    monthly = monthly.sort_values("InvoiceDate")

    # Customer ID arrives as float64 (e.g. 18102.0) because of a stray decimal in the
    # source CSV. Cast to nullable Int64 so it displays as "18102" everywhere — in the
    # chart, the data explorer table, and the sidebar CSV download — instead of "18102.0".
    if "Customer ID" in customers.columns:
        customers["Customer ID"] = customers["Customer ID"].astype("Int64")

    # Sort by Revenue descending so "Top 10" logic is correct everywhere
    products = products.sort_values("Revenue", ascending=False).reset_index(drop=True)
    country = country.sort_values("Revenue", ascending=False).reset_index(drop=True)
    customers = customers.sort_values("Revenue", ascending=False).reset_index(drop=True)

    return monthly, products, country, customers

with st.spinner("Loading Project FORESIGHT intelligence layer..."):
    monthly, products, country, customers = load_data()

if monthly.empty:
    _fail("dashboard_monthly.csv loaded but contains zero valid rows after date parsing.")

# ============================================================
# 4b. INSIGHT COMPUTATION — single source of truth.
# Returns a list of dicts so both the on-page badge panel and
# the PDF export render the SAME numbers. Computing insights
# twice in two places is how dashboards silently drift out of
# sync with their own exports — not doing that here.
# ============================================================
def compute_insights(monthly, products, country, customers):
    out = []  # each item: {"icon": str, "kind": "positive"/"negative"/"info"/"warning", "text": str}

    if not monthly.empty:
        best_row = monthly.loc[monthly["Revenue"].idxmax()]
        out.append({"icon": "🏆", "kind": "info", "text":
            f"Peak revenue month was <b>{best_row['InvoiceDate'].strftime('%B %Y')}</b> "
            f"with <b>${best_row['Revenue']:,.2f}</b> in sales."})

    if len(monthly) >= 2:
        last_two = monthly.tail(2)
        prev_rev, curr_rev = last_two["Revenue"].iloc[0], last_two["Revenue"].iloc[1]
        if prev_rev != 0:
            mom = ((curr_rev - prev_rev) / prev_rev) * 100
            out.append({"icon": "📈" if mom >= 0 else "📉", "kind": "positive" if mom >= 0 else "negative", "text":
                f"Latest month-over-month revenue {'growth' if mom >= 0 else 'decline'} is <b>{mom:+.1f}%</b> "
                f"({last_two['InvoiceDate'].iloc[0].strftime('%b %Y')} → {last_two['InvoiceDate'].iloc[1].strftime('%b %Y')})."})

    if not products.empty:
        top_p = products.iloc[0]
        pct = (top_p["Revenue"] / products["Revenue"].sum()) * 100
        out.append({"icon": "📦", "kind": "info", "text":
            f"Best-selling product is <b>{top_p['Description']}</b>, generating "
            f"<b>${top_p['Revenue']:,.2f}</b> (~{pct:.1f}% of tracked product revenue)."})

    if not country.empty:
        top_c = country.iloc[0]
        pct_c = (top_c["Revenue"] / country["Revenue"].sum()) * 100
        out.append({"icon": "🌍", "kind": "info", "text":
            f"<b>{top_c['Country']}</b> is the top revenue-generating market at "
            f"<b>${top_c['Revenue']:,.2f}</b> (~{pct_c:.1f}% of total country revenue)."})

    if not customers.empty:
        top10_rev = customers.head(10)["Revenue"].sum()
        total_cust_rev = customers["Revenue"].sum()
        conc = (top10_rev / total_cust_rev) * 100 if total_cust_rev else 0
        out.append({"icon": "⚠️" if conc > 40 else "👥", "kind": "warning" if conc > 40 else "info", "text":
            f"Top 10 customers contribute <b>{conc:.1f}%</b> of total customer revenue — "
            f"{'a high concentration risk worth monitoring.' if conc > 40 else 'a relatively diversified customer base.'}"})

    if len(monthly) >= 4:
        mean_rev, std_rev = monthly["Revenue"].mean(), monthly["Revenue"].std()
        if std_rev > 0:
            mz = monthly.copy()
            mz["z"] = (mz["Revenue"] - mean_rev) / std_rev
            anomalies = mz[mz["z"].abs() >= 2]
            if not anomalies.empty:
                for _, row in anomalies.iterrows():
                    direction = "spike" if row["z"] > 0 else "drop"
                    out.append({"icon": "🚨", "kind": "warning" if row["z"] < 0 else "positive", "text":
                        f"Statistical anomaly: <b>{row['InvoiceDate'].strftime('%B %Y')}</b> is a revenue {direction} "
                        f"at <b>{row['z']:+.1f} std devs</b> from the {len(monthly)}-month mean (${mean_rev:,.0f})."})
            else:
                out.append({"icon": "✅", "kind": "info", "text":
                    f"No statistically significant monthly outliers detected (all within ±2 std devs of ${mean_rev:,.0f})."})

    myr = monthly.copy()
    myr["Year"] = myr["InvoiceDate"].dt.year
    yearly = myr.groupby("Year")["Revenue"].sum().sort_index()
    if len(yearly) >= 2:
        yoy = ((yearly.iloc[-1] - yearly.iloc[-2]) / yearly.iloc[-2]) * 100
        out.append({"icon": "📅", "kind": "positive" if yoy >= 0 else "negative", "text":
            f"Year-over-year revenue {'grew' if yoy >= 0 else 'declined'} <b>{yoy:+.1f}%</b> "
            f"from {yearly.index[-2]} (${yearly.iloc[-2]:,.0f}) to {yearly.index[-1]} (${yearly.iloc[-1]:,.0f})."})
    else:
        out.append({"icon": "ℹ️", "kind": "warning", "text":
            f"Only {len(yearly)} year(s) of data present — YoY comparison isn't statistically meaningful yet."})

    return out

# ============================================================
# 4c. PDF REPORT BUILDER — a real export, not a renamed CSV.
# Requires reportlab (see requirements.txt).
# ============================================================
def build_pdf_report(monthly, products, country, customers, insights):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.pdfgen import canvas
    from io import BytesIO
    import re

    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    y = height - 25 * mm

    c.setFont("Helvetica-Bold", 18)
    c.drawString(20 * mm, y, "Project FORESIGHT — Executive Summary")
    y -= 8 * mm
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.grey)
    c.drawString(20 * mm, y, f"Generated {datetime.now().strftime('%d %b %Y, %H:%M')}")
    c.setFillColor(colors.black)
    y -= 12 * mm

    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, y, "Key Metrics")
    y -= 7 * mm
    c.setFont("Helvetica", 10)
    metrics = [
        f"Total Revenue: ${monthly['Revenue'].sum():,.2f}",
        f"Total Customers: {len(customers):,}",
        f"Total Products: {len(products):,}",
        f"Total Countries: {len(country):,}",
    ]
    for m in metrics:
        c.drawString(22 * mm, y, f"- {m}")
        y -= 6 * mm

    y -= 6 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, y, "Business Insights")
    y -= 7 * mm
    c.setFont("Helvetica", 9.5)

    for item in (insights or []):
        plain_text = re.sub("<[^<]+?>", "", item["text"])  # strip <b> tags for plain PDF text
        wrapped = []
        line = ""
        for word in plain_text.split():
            test = f"{line} {word}".strip()
            if c.stringWidth(test, "Helvetica", 9.5) > (width - 44 * mm):
                wrapped.append(line)
                line = word
            else:
                line = test
        if line:
            wrapped.append(line)
        for wline in wrapped:
            if y < 20 * mm:
                c.showPage()
                y = height - 20 * mm
                c.setFont("Helvetica", 9.5)
            c.drawString(22 * mm, y, f"- {wline}")
            y -= 5.5 * mm
        y -= 2 * mm

    c.save()
    buf.seek(0)
    return buf.getvalue()

insights = compute_insights(monthly, products, country, customers)

# ============================================================
# 5. SIDEBAR — real anchor-scroll nav + filters + downloads
# ------------------------------------------------------------
# NOTE: This is a single-page app backed by 4 flat CSVs with no
# time dimension except Revenue. A left nav with 7 items implying
# 7 separate pages (Analytics/Products/Customers/Geography/etc.)
# would be fake — clicking most of them would do nothing. These
# links instead jump to real sections that exist on this page.
# ============================================================
st.sidebar.markdown("## 📊 Project FORESIGHT")
st.sidebar.caption("AI-Powered Retail Sales Intelligence")
st.sidebar.markdown("---")

# Sidebar navigation
st.sidebar.markdown("### Navigation")

st.sidebar.markdown(
    """
    <a class="nav-link" href="#dashboard-top">🏠 &nbsp; Dashboard</a>
    <a class="nav-link" href="#world-map">🌍 &nbsp; Geography</a>
    <a class="nav-link" href="#insights">💡 &nbsp; Insights</a>
    <a class="nav-link" href="#analytics">📈 &nbsp; Analytics</a>
    <a class="nav-link" href="#data-explorer">🗃️ &nbsp; Reports</a>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Quick Stats")
_qs_revenue = monthly["Revenue"].sum()
st.sidebar.markdown(
    f'<div class="quick-stat"><div class="quick-stat-label">Total Revenue</div>'
    f'<div class="quick-stat-value">${_qs_revenue:,.0f}</div></div>'
    f'<div class="quick-stat"><div class="quick-stat-label">Tracked Entities</div>'
    f'<div class="quick-stat-value">{len(customers):,} customers · {len(products):,} products · {len(country):,} countries</div></div>',
    unsafe_allow_html=True,
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔎 Filters")

# Year filter — legitimate because InvoiceDate lives in the monthly table
years_available = sorted(monthly["InvoiceDate"].dt.year.dropna().unique().tolist())
selected_years = st.sidebar.multiselect(
    "Year (applies to trend charts)",
    options=years_available,
    default=years_available,
)

country_options = ["All"] + country["Country"].tolist()
selected_country = st.sidebar.selectbox("Country (Country chart only)", country_options)
st.sidebar.caption(
    "⚠️ Products & Customers CSVs have no Country column — "
    "this filter only scopes the Country Revenue chart, by design."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⬇️ Raw Data Export")
st.sidebar.download_button("Monthly CSV", monthly.to_csv(index=False).encode("utf-8"), "monthly.csv", "text/csv")
st.sidebar.download_button("Products CSV", products.to_csv(index=False).encode("utf-8"), "products.csv", "text/csv")
st.sidebar.download_button("Country CSV", country.to_csv(index=False).encode("utf-8"), "country.csv", "text/csv")
st.sidebar.download_button("Customers CSV", customers.to_csv(index=False).encode("utf-8"), "customers.csv", "text/csv")

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About")
st.sidebar.caption(
    "Project FORESIGHT — Zidio Internship\n\n"
    "Built with Streamlit, Plotly & pandas. "
    "Data is read-only from 4 processed CSVs; nothing is fabricated or fetched live."
)

# Apply year filter to a working copy of monthly data
monthly_f = monthly[monthly["InvoiceDate"].dt.year.isin(selected_years)] if selected_years else monthly.copy()

# ============================================================
# 6. TOP BAR — welcome text, title, date range, real PDF export
# ============================================================
st.markdown('<div id="dashboard-top"></div>', unsafe_allow_html=True)
last_updated = datetime.now().strftime("%d %b %Y, %H:%M")
date_range_label = (
    f"{monthly['InvoiceDate'].min().strftime('%b %Y')} – {monthly['InvoiceDate'].max().strftime('%b %Y')}"
    if not monthly.empty else "N/A"
)

col_title, col_export = st.columns([3, 1])
with col_title:
    st.markdown(
        f'<div style="display:flex; align-items:center; gap:14px;">'
        f'<div class="logo-mark">📊</div>'
        f'<div>'
        f'<div class="top-bar-greeting">Welcome back, Gauri 👋</div>'
        f'<p class="top-bar-title">Project FORESIGHT</p>'
        f'<p class="top-bar-subtitle">Executive Retail Sales Intelligence &amp; Revenue Analytics</p>'
        f'</div></div>'
        f'<p class="top-bar-meta">'
        f'<span class="status-pill"><span class="status-dot"></span>Live</span>'
        f'&nbsp;&nbsp;🕒 Last updated {last_updated} &nbsp;•&nbsp; Data range: {date_range_label}'
        f'</p>',
        unsafe_allow_html=True,
    )

with col_export:
    st.write("")  # vertical alignment spacer
    st.download_button(
        "⬇️ Export Summary Report (PDF)",
        data=build_pdf_report(monthly, products, country, customers, insights=insights),
        file_name="foresight_summary_report.pdf",
        mime="application/pdf",
    )
    st.caption("Exports KPIs + insights as a PDF. Not a pixel copy of the on-screen charts.")

# ============================================================
# 7. KPI CARDS — native HTML (no iframe), fully responsive
# ------------------------------------------------------------
# NOTE: An earlier version used components.html() with a JS
# count-up animation. That approach uses a fixed-height iframe
# that does NOT auto-resize, so on narrow screens where the 4
# cards wrap to 2 rows, the bottom row gets clipped. Animation
# was dropped in favor of a layout that is actually correct on
# mobile — requirement #25 said "if possible," and it isn't,
# without breaking responsiveness.
# ============================================================
total_revenue = float(monthly["Revenue"].sum())
total_customers = int(len(customers))
total_products = int(len(products))
total_countries = int(len(country))

# Real trend sparkline — only possible for Revenue, since it's the only
# metric backed by a time series in the source data.
revenue_spark = make_sparkline_svg(monthly["Revenue"].tolist(), ACCENT_2)

# Real period-over-period delta for Revenue (first half vs second half of
# the loaded date range) — NOT fabricated like the other 3 metrics would be.
if len(monthly) >= 2:
    midpoint = len(monthly) // 2
    first_half_rev = monthly.iloc[:midpoint]["Revenue"].sum()
    second_half_rev = monthly.iloc[midpoint:]["Revenue"].sum()
    if first_half_rev > 0:
        rev_delta = ((second_half_rev - first_half_rev) / first_half_rev) * 100
        rev_delta_html = (
            f'<span class="kpi-delta-up">▲ {rev_delta:+.1f}% vs earlier period</span>' if rev_delta >= 0
            else f'<span class="kpi-delta-down">▼ {rev_delta:+.1f}% vs earlier period</span>'
        )
    else:
        rev_delta_html = '<span class="kpi-delta-none">no prior baseline</span>'
else:
    rev_delta_html = '<span class="kpi-delta-none">insufficient history</span>'

no_baseline = '<span class="kpi-delta-none">no time series in source data</span>'

kpi_data = [
    ("💰", "Total Revenue", f"${total_revenue:,.2f}", revenue_spark, rev_delta_html),
    ("👥", "Customers", f"{total_customers:,}", "", no_baseline),
    ("📦", "Products", f"{total_products:,}", "", no_baseline),
    ("🌍", "Countries", f"{total_countries:,}", "", no_baseline),
]

def _kpi_card_html(icon, label, value, spark, delta):
    # NOTE: built as a single unindented line on purpose. Streamlit's markdown
    # renderer (CommonMark) treats a blank line followed by 4+ spaces of
    # indentation as an INDENTED CODE BLOCK, not raw HTML. The previous
    # multi-line/indented f-string joined across 4 cards hit exactly that
    # rule: card 1 rendered fine (no blank line before it yet), but every
    # card after it got dumped as literal escaped text. Keeping each card on
    # one line with zero leading whitespace sidesteps the rule entirely.
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-icon">{icon}</div>'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div style="margin-top:6px;">{spark}</div>'
        f'<div style="margin-top:4px;">{delta}</div>'
        f'</div>'
    )

cards_html = "".join(_kpi_card_html(*row) for row in kpi_data)

st.markdown(f"""
<style>
  .kpi-row {{ display:flex; gap:18px; flex-wrap:wrap; margin-bottom: 8px; }}
  .kpi-card {{
      flex:1; min-width:200px;
      background: {GLASS_BG};
      border: 1px solid {GLASS_BORDER};
      border-radius:16px;
      padding:20px 22px;
      box-shadow: 0 8px 28px rgba(0,0,0,0.4);
      transition: transform .25s ease, box-shadow .25s ease;
  }}
  .kpi-card:hover {{ transform: translateY(-5px); box-shadow: 0 16px 36px rgba(108,99,255,0.3); }}
  .kpi-icon {{ font-size:22px; margin-bottom:8px; }}
  .kpi-label {{ font-size:12.5px; color:{TEXT_MUTED}; text-transform:uppercase; letter-spacing:.08em; font-weight:600; }}
  .kpi-value {{
      font-family:'Manrope',sans-serif; font-size:28px; font-weight:800;
      background: {GRADIENT_MAIN};
      -webkit-background-clip:text; -webkit-text-fill-color:transparent;
      margin-top:4px;
  }}
  @media (max-width: 640px) {{
      .kpi-card {{ min-width: 100%; }}
  }}
</style>
<div class="kpi-row">{cards_html}</div>
""", unsafe_allow_html=True)

# ============================================================
# 7b. EXECUTIVE SUMMARY — one-glance synthesis for leadership.
# Built entirely from numbers already computed above (total_revenue,
# products, country) — no new computation, no fabricated figures.
# ============================================================
_top_product_row = products.iloc[0] if not products.empty else None
_top_country_row = country.iloc[0] if not country.empty else None

_exec_bits = [f"Tracked revenue across the loaded period totals <b>${total_revenue:,.2f}</b>"]
if _top_country_row is not None:
    _exec_bits.append(f"led by <b>{_top_country_row['Country']}</b> (${_top_country_row['Revenue']:,.2f})")
if _top_product_row is not None:
    _exec_bits.append(f"with <b>{_top_product_row['Description']}</b> as the top-selling product")
_exec_summary_text = ", ".join(_exec_bits) + f", across {total_customers:,} tracked customers in {total_countries:,} countries."

st.markdown(
    f'<div class="exec-summary">📋 <b>Executive Summary</b> — {_exec_summary_text}</div>',
    unsafe_allow_html=True,
)

# ============================================================
# 8. WORLD MAP — real choropleth from Country revenue data
# ------------------------------------------------------------
# FIX: Plotly's built-in choropleth matches on exact country NAME.
# Several rows in dashboard_country.csv use aliases that don't match
# Plotly's naming ("EIRE", "USA", "RSA", "Korea"), so their revenue
# was silently dropped from the map (shown as blank). This alias map
# is used ONLY for the map's `locations` — it does not touch the
# `country` DataFrame itself, so the bar chart, KPIs, insights, and
# CSV export still show the original names exactly as sourced.
# "Channel Islands", "Unspecified", and "West Indies" are left
# unmapped on purpose: they aren't single countries, so plotting them
# on a country choropleth would mean guessing — not fixing.
# ============================================================
st.markdown('<div id="world-map"></div>', unsafe_allow_html=True)
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<p class="section-label">Geography</p>', unsafe_allow_html=True)
st.markdown("### 🌍 Revenue by Country")

COUNTRY_NAME_ALIASES = {
    "EIRE": "Ireland",
    "USA": "United States",
    "RSA": "South Africa",
    "Korea": "South Korea",
}
map_locations = country["Country"].replace(COUNTRY_NAME_ALIASES)

fig_map = go.Figure(go.Choropleth(
    locations=map_locations,
    locationmode="country names",
    z=country["Revenue"],
    colorscale=[[0, ACCENT_1], [1, ACCENT_2]],
    marker_line_color=BG_PANEL,
    marker_line_width=0.5,
    colorbar_title="Revenue ($)",
    hovertemplate="<b>%{location}</b><br>Revenue: $%{z:,.2f}<extra></extra>",
))
fig_map.update_geos(
    bgcolor="rgba(0,0,0,0)", showframe=False, showcoastlines=False,
    landcolor="#1a1f2b", oceancolor="#05070A", lakecolor="#05070A",
)
fig_map.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=13),
    margin=dict(l=0, r=0, t=10, b=0),
    height=420,
)
st.plotly_chart(fig_map, use_container_width=True)

# ============================================================
# 9. AUTO-GENERATED BUSINESS INSIGHTS — badge-style cards
# (data already computed once in compute_insights() above —
# rendering only, not recomputing, to avoid drift vs the PDF)
# ============================================================
st.markdown('<div id="insights"></div>', unsafe_allow_html=True)
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<p class="section-label">Intelligence Summary</p>', unsafe_allow_html=True)
st.markdown("### 🧠 Business Insights")

KIND_COLORS = {
    "positive": ACCENT_4,
    "negative": ACCENT_3,
    "warning": "#FFB84C",
    "info": ACCENT_2,
}

for item in insights:
    badge_color = KIND_COLORS.get(item["kind"], ACCENT_2)
    st.markdown(
        f'<div class="badge-card">'
        f'<div class="badge-icon" style="background: {badge_color}22; color: {badge_color};">{item["icon"]}</div>'
        f'<div class="badge-text">{item["text"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ============================================================
# 10. MAIN CHARTS — organized into tabs (no long raw tables)
# ============================================================
st.markdown('<div id="analytics"></div>', unsafe_allow_html=True)
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<p class="section-label">Analytics</p>', unsafe_allow_html=True)
st.markdown("### 📈 Performance Deep-Dive")

tab_overview, tab_products, tab_country, tab_customers, tab_data = st.tabs(
    ["📈 Revenue Trend", "📦 Top Products", "🌍 Country Revenue", "👥 Top Customers", "🗃️ Data Explorer"]
)

# Shared Plotly dark template
PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=13),
    colorway=CHART_COLORWAY,
    margin=dict(l=20, r=20, t=60, b=20),
    hoverlabel=dict(bgcolor=BG_PANEL, font_size=13, font_family="Inter", bordercolor=ACCENT_1),
    bargap=0.35,
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", zeroline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
)

# ---------- Tab 1: Revenue Trend + Monthly Growth ----------
with tab_overview:
    col_a, col_b = st.columns([1.4, 1])

    with col_a:
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_f["InvoiceDate"], y=monthly_f["Revenue"],
            mode="lines+markers",
            # smoothing kept low (0.3) on purpose: high spline smoothing can overshoot
            # between two similar-value points and visually imply a dip/spike that
            # never happened in the real data — misleading on an executive dashboard.
            line=dict(shape="spline", smoothing=0.3, width=3, color=ACCENT_2),
            marker=dict(size=7, color=ACCENT_1, line=dict(width=1, color="white")),
            fill="tozeroy",
            fillcolor="rgba(0, 217, 255, 0.12)",
            hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: $%{y:,.2f}<extra></extra>",
            name="Revenue",
        ))
        fig_trend.update_layout(
            title="Monthly Revenue Trend",
            xaxis_title="Month", yaxis_title="Revenue ($)",
            **PLOTLY_LAYOUT
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_b:
        growth = monthly_f.copy()
        growth["MoM %"] = growth["Revenue"].pct_change() * 100
        fig_growth = go.Figure()
        fig_growth.add_trace(go.Bar(
            x=growth["InvoiceDate"], y=growth["MoM %"],
            marker_color=[
                TEXT_MUTED if pd.isna(v) else (ACCENT_4 if v >= 0 else ACCENT_3)
                for v in growth["MoM %"]
            ],
            hovertemplate="<b>%{x|%b %Y}</b><br>MoM Change: %{y:.1f}%<extra></extra>",
            name="MoM Growth",
        ))
        fig_growth.update_layout(
            title="Month-over-Month Growth (%)",
            xaxis_title="Month", yaxis_title="Change (%)",
            **PLOTLY_LAYOUT
        )
        st.plotly_chart(fig_growth, use_container_width=True)

# ---------- Tab 2: Top Products ----------
with tab_products:
    top_products = products.head(10).sort_values("Revenue")
    fig_products = go.Figure(go.Bar(
        x=top_products["Revenue"], y=top_products["Description"],
        orientation="h",
        marker=dict(
            color=top_products["Revenue"],
            colorscale=[[0, ACCENT_1], [1, ACCENT_2]],
            line=dict(width=0),
        ),
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>",
    ))
    fig_products.update_layout(
        title="Top 10 Products by Revenue",
        xaxis_title="Revenue ($)", yaxis_title="",
        **PLOTLY_LAYOUT
    )
    st.plotly_chart(fig_products, use_container_width=True)

# ---------- Tab 3: Country Revenue ----------
with tab_country:
    country_view = country.copy()
    if selected_country != "All":
        country_view = country_view[country_view["Country"] == selected_country]
    top_country = country_view.head(10)

    fig_country = go.Figure(go.Bar(
        x=top_country["Country"], y=top_country["Revenue"],
        marker=dict(
            color=top_country["Revenue"],
            colorscale=[[0, ACCENT_1], [1, ACCENT_4]],
        ),
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>",
    ))
    country_chart_title = (
        f"Revenue — {selected_country}" if selected_country != "All"
        else "Top 10 Countries by Revenue"
    )
    fig_country.update_layout(
        title=country_chart_title,
        xaxis_title="Country", yaxis_title="Revenue ($)",
        **PLOTLY_LAYOUT
    )
    st.plotly_chart(fig_country, use_container_width=True)

# ---------- Tab 4: Top Customers ----------
with tab_customers:
    top_customers = customers.head(10).sort_values("Revenue")
    fig_customers = go.Figure(go.Bar(
        x=top_customers["Revenue"], y=top_customers["Customer ID"].astype(str),
        orientation="h",
        marker=dict(
            color=top_customers["Revenue"],
            colorscale=[[0, ACCENT_2], [1, ACCENT_3]],
        ),
        hovertemplate="<b>Customer %{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>",
    ))
    fig_customers.update_layout(
        title="Top 10 Customers by Revenue",
        xaxis_title="Revenue ($)", yaxis_title="Customer ID",
        **PLOTLY_LAYOUT
    )
    st.plotly_chart(fig_customers, use_container_width=True)

# ---------- Tab 5: Data Explorer (replaces long static tables) ----------
with tab_data:
    st.markdown('<div id="data-explorer"></div>', unsafe_allow_html=True)
    st.caption("Compact data explorer — top 10 rows per dataset. Full data available via sidebar download.")

    _rev_col = st.column_config.NumberColumn("Revenue", format="$%.2f")
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("**Monthly Revenue**")
        st.dataframe(
            monthly.tail(10), use_container_width=True, height=250,
            column_config={
                "InvoiceDate": st.column_config.DateColumn("Month", format="MMM YYYY"),
                "Revenue": _rev_col,
            },
        )
        st.markdown("**Top Products**")
        st.dataframe(products.head(10), use_container_width=True, height=250, column_config={"Revenue": _rev_col})
    with d2:
        st.markdown("**Top Countries**")
        st.dataframe(country.head(10), use_container_width=True, height=250, column_config={"Revenue": _rev_col})
        st.markdown("**Top Customers**")
        st.dataframe(customers.head(10), use_container_width=True, height=250, column_config={"Revenue": _rev_col})

# ============================================================
# 10. FOOTER
# ============================================================
# NOTE: GitHub/LinkedIn URLs below are placeholders — replace
# "your-username" / "your-linkedin" with your real profile links.
st.markdown(
    f'<div class="footer-box">'
    f'<b>Project FORESIGHT</b> — Executive Retail Sales Analytics Dashboard'
    f'<span class="version-tag" style="margin-left:8px;">v1.1.0</span><br>'
    f'Built with Streamlit &amp; Plotly &nbsp;•&nbsp; Built by Yash &nbsp;•&nbsp; {datetime.now().year}'
    f'<div class="footer-links">'
    f'<a class="footer-link" href="https://github.com/Yashr4635" target="_blank">⌗ GitHub</a>'
    f'<a class="footer-link" href="https://www.linkedin.com/in/ds-yashaswi-662533318/" target="_blank">in LinkedIn</a>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True,
)