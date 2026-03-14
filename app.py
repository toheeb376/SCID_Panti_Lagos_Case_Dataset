# =============================================================================
# SCID PANTI LAGOS — CRIMINAL CASE INTELLIGENCE DASHBOARD
# =============================================================================
#
# SETUP INSTRUCTIONS
# ------------------
# 1. Install required libraries:
#       pip install streamlit pandas plotly openpyxl numpy
#
# 2. Place all three files in the SAME folder:
#       - SCID_Panti_Lagos_Case_Dataset.xlsx
#       - SCID_Panti_Lagos_Case_Dataset.png
#       - app.py
#
# 3. Open a terminal in that folder and run:
#       streamlit run app.py
#
# 4. The dashboard opens automatically at http://localhost:8501
#
# COLOR SCHEME GUIDE (every section has its own unique color)
# -----------------------------------------------------------
# App Background     : rgb(10, 14, 40)       — Deep Navy
# Sidebar            : rgb(1, 60, 28)         — Dark Forest Green
# KPI Cards          : rgb(14, 22, 74)        — Royal Navy
# KPI Values         : rgb(254, 246, 0)       — Bright Yellow
# KPI Labels         : rgb(160, 200, 255)     — Soft Ice Blue
# Section Banners    : rgb(30, 0, 134)        — Deep Purple
# H1 Headings        : rgb(254, 246, 0)       — Yellow
# H2/H3 Headings     : rgb(100, 220, 160)     — Mint Green
# Body Text          : rgb(210, 225, 255)     — Pale Periwinkle
# Chart Backgrounds  : rgb(18, 26, 60)        — Midnight Navy
# Chart Axis Text    : rgb(200, 215, 255)     — Ice Blue
# Chart Titles       : rgb(254, 246, 0)       — Yellow
# Table Headers      : rgb(14, 22, 74) bg / Yellow text
# Expander           : Yellow border / Dark Navy bg
# Footer             : rgb(130, 160, 255)     — Lavender Blue
# =============================================================================

import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SCID Panti Lagos | Case Intelligence Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── MASTER COLOR DICTIONARY ───────────────────────────────────────────────────
C = {
    "app_bg":       "rgb(10, 14, 40)",
    "sidebar_bg":   "rgb(1, 60, 28)",
    "card_bg":      "rgb(14, 22, 74)",
    "chart_bg":     "rgb(18, 26, 60)",
    "chart_paper":  "rgb(10, 14, 40)",
    "kpi_value":    "rgb(254, 246, 0)",
    "kpi_label":    "rgb(160, 200, 255)",
    "heading_h1":   "rgb(254, 246, 0)",
    "heading_h2":   "rgb(100, 220, 160)",
    "body_text":    "rgb(210, 225, 255)",
    "axis_text":    "rgb(200, 215, 255)",
    "chart_title":  "rgb(254, 246, 0)",
    "card_border":  "rgb(30, 0, 134)",
    "chart_grid":   "rgba(100, 130, 255, 0.15)",
    "danger":       "rgb(255, 60, 60)",
    "success":      "rgb(0, 200, 100)",
    "warning":      "rgb(255, 165, 0)",
    "info":         "rgb(80, 160, 255)",
    "neutral":      "rgb(140, 140, 160)",
    "yellow":       "rgb(254, 246, 0)",
    "green":        "rgb(1, 122, 55)",
    "deep_blue":    "rgb(30, 0, 134)",
    "white":        "rgb(255, 255, 255)",
    "black":        "rgb(0, 0, 0)",
}

CHART_COLORS = [
    "rgb(80, 160, 255)",
    "rgb(0, 200, 100)",
    "rgb(255, 165, 0)",
    "rgb(255, 60, 60)",
    "rgb(180, 100, 255)",
    "rgb(254, 246, 0)",
    "rgb(0, 210, 210)",
    "rgb(255, 120, 60)",
]

# ── CSS INJECTION ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: rgb(10, 14, 40) !important; }
    .main .block-container { background-color: rgb(10, 14, 40) !important; padding-top: 1.5rem; }

    .stApp, .stApp p, .stApp li, .stApp span { color: rgb(210, 225, 255); }

    h1 { color: rgb(254, 246, 0) !important; font-weight: 900 !important; font-size: 2rem !important; }
    h2, h3, h4 { color: rgb(100, 220, 160) !important; font-weight: 700 !important; }

    section[data-testid="stSidebar"] { background-color: rgb(1, 60, 28) !important; border-right: 2px solid rgba(254,246,0,0.3) !important; }
    section[data-testid="stSidebar"] * { color: rgb(255, 255, 255) !important; }
    section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] { background-color: rgb(30, 0, 134) !important; color: rgb(255,255,255) !important; }
    section[data-testid="stSidebar"] hr { border-color: rgba(254,246,0,0.35) !important; }

    div[data-testid="metric-container"] {
        background-color: rgb(14, 22, 74) !important;
        border: 2px solid rgb(30, 0, 134) !important;
        border-top: 4px solid rgb(254, 246, 0) !important;
        border-radius: 10px !important;
        padding: 14px 16px !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.5) !important;
    }
    div[data-testid="metric-container"] label,
    div[data-testid="metric-container"] p {
        color: rgb(160, 200, 255) !important;
        font-weight: 700 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: rgb(254, 246, 0) !important; font-size: 1.6rem !important; font-weight: 900 !important; }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] * { color: rgb(254, 246, 0) !important; }
    div[data-testid="metric-container"] > div > div > div > div { color: rgb(254, 246, 0) !important; }
    div[data-testid="metric-container"] > div > div > div { color: rgb(254, 246, 0) !important; }
    div[data-testid="metric-container"] span { color: rgb(254, 246, 0) !important; }

    .section-label {
        background-color: rgb(30, 0, 134);
        color: rgb(254, 246, 0);
        padding: 5px 16px;
        border-radius: 4px;
        font-weight: 800;
        font-size: 0.82rem;
        display: inline-block;
        margin-bottom: 12px;
        letter-spacing: 0.08em;
        border-left: 4px solid rgb(254, 246, 0);
    }

    hr { border-color: rgba(254,246,0,0.2) !important; margin: 1.2rem 0 !important; }

    .stDataFrame { border: 1px solid rgba(80,160,255,0.3) !important; border-radius: 8px !important; }
    .stDataFrame thead tr th { background-color: rgb(14,22,74) !important; color: rgb(254,246,0) !important; font-weight: 700 !important; }
    .stDataFrame tbody tr:nth-child(even) td { background-color: rgba(30,0,134,0.25) !important; }
    .stDataFrame tbody tr td { color: rgb(210,225,255) !important; font-size: 0.82rem !important; }

    details { background-color: rgb(14, 22, 74) !important; border: 1px solid rgb(254, 246, 0) !important; border-radius: 8px !important; padding: 4px 10px !important; }
    summary { color: rgb(254, 246, 0) !important; font-weight: 700 !important; font-size: 1rem !important; }
    details p, details li, details span { color: rgb(210, 225, 255) !important; }
    details h3 { color: rgb(100, 220, 160) !important; }
    details strong { color: rgb(254, 246, 0) !important; }

    .stCaption, small { color: rgb(130, 160, 255) !important; }
    .stAlert { background-color: rgb(14, 22, 74) !important; border-left: 4px solid rgb(80,160,255) !important; }
    .stPlotlyChart { border: 1px solid rgba(80,160,255,0.2) !important; border-radius: 10px !important; overflow: hidden !important; }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgb(10,14,40); }
    ::-webkit-scrollbar-thumb { background: rgb(30,0,134); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgb(80,160,255); }
</style>
""", unsafe_allow_html=True)


# ── DATA LOADING ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)
    str_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()
    df.replace({"—": np.nan, "nan": np.nan}, inplace=True)
    for dcol in ["Report_Date", "Incident_Date", "Next_Hearing_Date"]:
        df[dcol] = pd.to_datetime(df[dcol], errors="coerce")
    df["Response_Lag_Days"] = (df["Report_Date"] - df["Incident_Date"]).dt.days.clip(lower=0)
    valid = df["Report_Date"].notna()
    df.loc[valid, "Report_Month"] = df.loc[valid, "Report_Date"].dt.to_period("M").astype(str)
    df["Suspect_Age"]  = pd.to_numeric(df["Suspect_Age"],  errors="coerce")
    df["Victim_Count"] = pd.to_numeric(df["Victim_Count"], errors="coerce").fillna(0)
    return df


# ── CHART HELPER ──────────────────────────────────────────────────────────────
def apply_brand(fig, title: str = "", height: int = 390) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(color=C["chart_title"], size=13, family="Arial Black, Arial"), x=0.01, xanchor="left"),
        paper_bgcolor=C["chart_paper"],
        plot_bgcolor=C["chart_bg"],
        font=dict(color=C["axis_text"], family="Arial, sans-serif", size=11),
        height=height,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(bgcolor="rgba(14,22,74,0.85)", bordercolor="rgba(80,160,255,0.4)", borderwidth=1, font=dict(size=10, color=C["body_text"])),
        xaxis=dict(gridcolor=C["chart_grid"], linecolor="rgba(80,160,255,0.3)", title=dict(font=dict(color=C["axis_text"])), tickfont=dict(color=C["axis_text"]), zerolinecolor="rgba(80,160,255,0.2)"),
        yaxis=dict(gridcolor=C["chart_grid"], linecolor="rgba(80,160,255,0.3)", title=dict(font=dict(color=C["axis_text"])), tickfont=dict(color=C["axis_text"]), zerolinecolor="rgba(80,160,255,0.2)"),
    )
    return fig


# ── FILE CHECK ────────────────────────────────────────────────────────────────
DATA_FILE = "SCID_Panti_Lagos_Case_Dataset.xlsx"
LOGO_FILE = "SCID_Panti_Lagos_Case_Dataset.png"

if not os.path.exists(DATA_FILE):
    st.error(f"❌ Data file **{DATA_FILE}** not found. Place it in the same folder as app.py.")
    st.stop()

df_raw = load_data(DATA_FILE)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=130)
    st.markdown("<h2 style='color:rgb(254,246,0)!important;font-size:1rem;'> Intelligence Filters</h2>", unsafe_allow_html=True)
    st.markdown("---")

    sel_case_type = st.multiselect("Case Type",          options=sorted(df_raw["Case_Type"].dropna().unique()),          default=sorted(df_raw["Case_Type"].dropna().unique()))
    sel_status    = st.multiselect("Case Status",        options=sorted(df_raw["Status"].dropna().unique()),             default=sorted(df_raw["Status"].dropna().unique()))
    sel_priority  = st.multiselect("Priority Level",     options=sorted(df_raw["Priority_Level"].dropna().unique()),     default=sorted(df_raw["Priority_Level"].dropna().unique()))
    sel_lga       = st.multiselect("LGA",                options=sorted(df_raw["LGA"].dropna().unique()),                default=sorted(df_raw["LGA"].dropna().unique()))
    sel_unit      = st.multiselect("Investigating Unit", options=sorted(df_raw["Investigating_Unit"].dropna().unique()), default=sorted(df_raw["Investigating_Unit"].dropna().unique()))
    sel_detention = st.multiselect("Detention Status",   options=sorted(df_raw["Detention_Status"].dropna().unique()),   default=sorted(df_raw["Detention_Status"].dropna().unique()))

    st.markdown("---")
    min_date = df_raw["Report_Date"].min().date() if df_raw["Report_Date"].notna().any() else None
    max_date = df_raw["Report_Date"].max().date() if df_raw["Report_Date"].notna().any() else None
    date_range = st.date_input("Report Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    st.markdown("---")
    st.markdown("<small style='color:rgba(255,255,255,0.6);'>SCID Panti Lagos · NPF<br/>Case Intelligence Portal v1.0</small>", unsafe_allow_html=True)


# ── APPLY FILTERS ─────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_case_type:  df = df[df["Case_Type"].isin(sel_case_type)]
if sel_status:     df = df[df["Status"].isin(sel_status)]
if sel_priority:   df = df[df["Priority_Level"].isin(sel_priority)]
if sel_lga:        df = df[df["LGA"].isin(sel_lga)]
if sel_unit:       df = df[df["Investigating_Unit"].isin(sel_unit)]
if sel_detention:  df = df[df["Detention_Status"].isin(sel_detention)]
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    s_dt, e_dt = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    df = df[df["Report_Date"].isna() | ((df["Report_Date"] >= s_dt) & (df["Report_Date"] <= e_dt))]


# ── KPIs ──────────────────────────────────────────────────────────────────────
total_cases         = len(df)
open_cases          = int((df["Status"] == "Open").sum())
under_investigation = int((df["Status"] == "Under Investigation").sum())
charged_to_court    = int((df["Status"] == "Charged to Court").sum())
closed_cases        = int((df["Status"] == "Closed").sum())
critical_cases      = int((df["Priority_Level"] == "Critical").sum())
in_custody          = int((df["Detention_Status"] == "In Custody").sum())
at_large            = int((df["Detention_Status"] == "At Large").sum())
total_victims       = int(df["Victim_Count"].sum())
avg_lag             = df["Response_Lag_Days"].mean()
avg_lag_str         = f"{avg_lag:.1f}" if pd.notna(avg_lag) else "N/A"
resolution_rate     = (charged_to_court / total_cases * 100) if total_cases > 0 else 0


# ── HEADER ────────────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([1, 8])
with col_logo:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=90)
with col_title:
    st.markdown(
        "<h1 style='margin-bottom:0;padding-bottom:0;color:rgb(254,246,0);'>"
        "SCID Panti Lagos — Case Intelligence Dashboard</h1>"
        "<p style='color:rgb(100,220,160);font-weight:600;margin-top:6px;font-size:0.95rem;'>"
        "State Criminal Investigation Department · Nigeria Police Force · Real-Time Operations View</p>",
        unsafe_allow_html=True,
    )
st.markdown("---")


# ── KPI CARDS ─────────────────────────────────────────────────────────────────
st.markdown('<span class="section-label"> KEY PERFORMANCE INDICATORS</span>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Cases",              f"{total_cases:,}")
k2.metric("Open Cases",               f"{open_cases:,}")
k3.metric("Under Investigation",      f"{under_investigation:,}")
k4.metric("Charged to Court",         f"{charged_to_court:,}")
k5.metric("Closed Cases",             f"{closed_cases:,}")

st.markdown("")

k6, k7, k8, k9, k10 = st.columns(5)
k6.metric("🔴 Critical Priority",     f"{critical_cases:,}")
k7.metric("Suspects In Custody",      f"{in_custody:,}")
k8.metric("🔴 Suspects At Large",     f"{at_large:,}")
k9.metric("Total Victims",            f"{total_victims:,}")
k10.metric("Avg Response Lag (Days)", avg_lag_str)

st.markdown("")
_, km, _ = st.columns([2, 1, 2])
km.metric("Case Resolution Rate (%)", f"{resolution_rate:.1f}%")
st.markdown("---")


# ── ROW 1: STATUS & TYPE ──────────────────────────────────────────────────────
st.markdown('<span class="section-label"> CASE STATUS & TYPE ANALYSIS</span>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    sc = df["Status"].value_counts().reset_index()
    sc.columns = ["Status", "Count"]
    scm = {"Open": C["danger"], "Under Investigation": C["info"], "Charged to Court": C["success"], "Closed": C["neutral"]}
    fig1 = px.bar(sc, x="Status", y="Count", color="Status", color_discrete_map=scm, text="Count")
    fig1.update_traces(textposition="outside", textfont=dict(color=C["kpi_value"], size=12))
    fig1 = apply_brand(fig1, "Case Status Distribution")
    fig1.update_layout(showlegend=False)
    fig1.update_xaxes(title=dict(text=""))
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    tc = df["Case_Type"].value_counts().reset_index()
    tc.columns = ["Case_Type", "Count"]
    tc = tc.sort_values("Count")
    fig2 = px.bar(tc, x="Count", y="Case_Type", orientation="h", text="Count", color_discrete_sequence=[C["info"]])
    fig2.update_traces(textposition="outside", textfont=dict(color=C["kpi_value"], size=11))
    fig2 = apply_brand(fig2, "Cases by Case Type")
    fig2.update_yaxes(title=dict(text=""))
    st.plotly_chart(fig2, use_container_width=True)


# ── ROW 2: TRENDS & PRIORITY ──────────────────────────────────────────────────
st.markdown('<span class="section-label"> TEMPORAL TRENDS & PRIORITY BREAKDOWN</span>', unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
    df_dated = df[df["Report_Date"].notna()].copy()
    if not df_dated.empty:
        monthly = df_dated.groupby("Report_Month").size().reset_index(name="Cases").sort_values("Report_Month")
        fig3 = px.line(monthly, x="Report_Month", y="Cases", markers=True, color_discrete_sequence=[C["kpi_value"]])
        fig3.update_traces(line=dict(width=2.5, color=C["kpi_value"]), marker=dict(size=8, color=C["success"], line=dict(width=2, color=C["kpi_value"])))
        fig3 = apply_brand(fig3, "Monthly Case Reporting Trend")
        fig3.update_xaxes(title=dict(text=""), tickangle=-45)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No date data available.")

with c4:
    pc = df["Priority_Level"].value_counts().reset_index()
    pc.columns = ["Priority", "Count"]
    pcm = {"Critical": C["danger"], "High": C["warning"], "Medium": C["info"], "Low": C["success"]}
    fig4 = px.pie(pc, names="Priority", values="Count", hole=0.50, color="Priority", color_discrete_map=pcm)
    fig4.update_traces(textinfo="label+percent", textfont=dict(size=12, color="rgb(255,255,255)"), marker=dict(line=dict(color=C["app_bg"], width=2)))
    fig4 = apply_brand(fig4, "Priority Level Breakdown")
    st.plotly_chart(fig4, use_container_width=True)


# ── ROW 3: OFFICERS & LGA ─────────────────────────────────────────────────────
st.markdown('<span class="section-label"> OFFICER PERFORMANCE & LGA DISTRIBUTION</span>', unsafe_allow_html=True)
c5, c6 = st.columns(2)

with c5:
    oc = df["Lead_Officer"].value_counts().head(10).reset_index()
    oc.columns = ["Lead_Officer", "Cases"]
    oc = oc.sort_values("Cases")
    fig5 = px.bar(oc, x="Cases", y="Lead_Officer", orientation="h", text="Cases", color_discrete_sequence=[C["success"]])
    fig5.update_traces(textposition="outside", textfont=dict(color=C["kpi_value"], size=10))
    fig5 = apply_brand(fig5, "Top 10 Lead Officers by Case Load")
    fig5.update_yaxes(title=dict(text=""))
    st.plotly_chart(fig5, use_container_width=True)

with c6:
    lc = df["LGA"].value_counts().reset_index()
    lc.columns = ["LGA", "Cases"]
    fig6 = px.bar(lc, x="LGA", y="Cases", text="Cases", color="Cases",
                  color_continuous_scale=[C["chart_bg"], "rgb(30,0,134)", C["info"], C["kpi_value"]])
    fig6.update_traces(textposition="outside", textfont=dict(color="rgb(255,255,255)", size=10))
    fig6.update_coloraxes(colorbar=dict(title=dict(text="Cases", font=dict(color=C["axis_text"])), tickfont=dict(color=C["axis_text"])))
    fig6 = apply_brand(fig6, "Cases by LGA (Local Government Area)")
    fig6.update_xaxes(tickangle=-35, title=dict(text=""))
    st.plotly_chart(fig6, use_container_width=True)


# ── ROW 4: OFFENSE & GENDER ───────────────────────────────────────────────────
st.markdown('<span class="section-label"> OFFENSE ANALYSIS & SUSPECT PROFILE</span>', unsafe_allow_html=True)
c7, c8 = st.columns(2)

with c7:
    ofc = df["Offense_Category"].value_counts().reset_index()
    ofc.columns = ["Offense_Category", "Count"]
    fig7 = px.treemap(ofc, path=["Offense_Category"], values="Count", color="Count",
                      color_continuous_scale=["rgb(14,22,74)", "rgb(30,0,134)", C["info"], C["kpi_value"]])
    fig7.update_traces(textinfo="label+value", textfont=dict(size=14, color="rgb(255,255,255)"))
    fig7.update_coloraxes(colorbar=dict(title=dict(text="Cases", font=dict(color=C["axis_text"])), tickfont=dict(color=C["axis_text"])))
    fig7 = apply_brand(fig7, "Offense Category Distribution (Treemap)")
    st.plotly_chart(fig7, use_container_width=True)

with c8:
    gd = df.groupby(["Case_Type", "Suspect_Gender"]).size().reset_index(name="Count")
    fig8 = px.bar(gd, x="Case_Type", y="Count", color="Suspect_Gender", barmode="group", text="Count",
                  color_discrete_map={"Male": C["info"], "Female": "rgb(255,100,180)"})
    fig8.update_traces(textposition="outside", textfont=dict(color="rgb(255,255,255)", size=9))
    fig8 = apply_brand(fig8, "Suspect Gender by Case Type")
    fig8.update_xaxes(tickangle=-30, title=dict(text=""))
    st.plotly_chart(fig8, use_container_width=True)


# ── ROW 5: EVIDENCE & OUTCOMES ────────────────────────────────────────────────
st.markdown('<span class="section-label"> EVIDENCE & OUTCOMES INTELLIGENCE</span>', unsafe_allow_html=True)
c9, _ = st.columns([2, 1])

with c9:
    eo = df.groupby(["Evidence_Type", "Case_Outcome"]).size().reset_index(name="Count")
    fig9 = px.bar(eo, x="Evidence_Type", y="Count", color="Case_Outcome", barmode="stack", text="Count",
                  color_discrete_sequence=CHART_COLORS)
    fig9.update_traces(textposition="inside", textfont=dict(color="rgb(255,255,255)", size=9))
    fig9 = apply_brand(fig9, "Evidence Type by Case Outcome")
    fig9.update_xaxes(tickangle=-25, title=dict(text=""))
    st.plotly_chart(fig9, use_container_width=True)


# ── 3D SCATTER ────────────────────────────────────────────────────────────────
st.markdown('<span class="section-label"> 3D INTELLIGENCE SCATTER — MULTI-VARIABLE CASE VIEW</span>', unsafe_allow_html=True)

df_3d = df.dropna(subset=["Report_Date", "Suspect_Age", "Victim_Count"]).copy()
if not df_3d.empty:
    df_3d["Date_Ordinal"] = df_3d["Report_Date"].map(pd.Timestamp.toordinal)
    p3dc = {"Critical": C["danger"], "High": C["warning"], "Medium": C["info"], "Low": C["success"]}
    fig_3d = go.Figure()
    for pv, grp in df_3d.groupby("Priority_Level"):
        fig_3d.add_trace(go.Scatter3d(
            x=grp["Date_Ordinal"], y=grp["Suspect_Age"], z=grp["Victim_Count"],
            mode="markers", name=pv,
            marker=dict(size=5, color=p3dc.get(pv, C["info"]), opacity=0.82,
                        line=dict(width=0.4, color="rgba(255,255,255,0.3)")),
            customdata=grp[["Case_ID","Case_Type","Lead_Officer","LGA","Detention_Status"]].values,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>Case Type: %{customdata[1]}<br>"
                "Lead Officer: %{customdata[2]}<br>LGA: %{customdata[3]}<br>"
                "Detention: %{customdata[4]}<br>Suspect Age: %{y}<br>Victims: %{z}<extra></extra>"
            ),
        ))
    sax = dict(tickfont=dict(color=C["axis_text"], size=9), gridcolor="rgba(80,160,255,0.15)",
               backgroundcolor=C["chart_bg"], showbackground=True)
    fig_3d.update_layout(
        height=560, paper_bgcolor=C["chart_paper"],
        scene=dict(
            bgcolor=C["chart_bg"],
            xaxis=dict(**sax, title=dict(text="Report Date (Ordinal)", font=dict(color=C["axis_text"], size=11))),
            yaxis=dict(**sax, title=dict(text="Suspect Age",           font=dict(color=C["axis_text"], size=11))),
            zaxis=dict(**sax, title=dict(text="Victim Count",          font=dict(color=C["axis_text"], size=11))),
        ),
        title=dict(text="3D Intelligence Scatter: Report Date · Suspect Age · Victim Count  (Color = Priority Level)",
                   font=dict(color=C["chart_title"], size=13, family="Arial Black, Arial"), x=0.01),
        font=dict(color=C["axis_text"]),
        legend=dict(bgcolor="rgba(14,22,74,0.9)", bordercolor="rgba(80,160,255,0.4)",
                    borderwidth=1, font=dict(size=10, color=C["body_text"])),
        margin=dict(l=0, r=0, t=55, b=0),
    )
    st.plotly_chart(fig_3d, use_container_width=True)
else:
    st.info("Insufficient data for 3D scatter with current filters.")

st.markdown("---")


# ── DATA TABLE ────────────────────────────────────────────────────────────────
st.markdown('<span class="section-label"> FILTERED CASE RECORDS</span>', unsafe_allow_html=True)

display_cols = ["Case_ID","Case_Type","Offense_Category","Report_Date","LGA",
                "Lead_Officer","Rank","Status","Priority_Level","Detention_Status","Case_Outcome","Victim_Count"]
st.dataframe(df[display_cols].reset_index(drop=True), use_container_width=True, height=290)
st.caption(f"Showing {len(df):,} of {len(df_raw):,} cases based on current filters.")
st.markdown("---")


# ── EXECUTIVE INSIGHT ─────────────────────────────────────────────────────────
with st.expander(" Executive Insight Summary — SCID Panti Lagos"):
    st.markdown("""
    ### Strategic Intelligence Overview

    **1. Monthly Case Reporting Trends — Crime Seasonality & Workload**
    Monthly aggregation of reported cases reveals crime seasonality patterns across Lagos.
    Persistent spikes in particular months may indicate seasonal crime drivers — such as festive
    periods or economic stress cycles — requiring SCID to pre-position investigative units
    and increase patrol deployments ahead of predicted surges.

    **2. Priority & LGA Concentration — Geographic Hotspot Intelligence**
    Concentrations of *Critical* and *High* priority cases within specific LGAs expose geographic
    crime hotspots demanding immediate resource redeployment. Command leadership can use the
    LGA distribution chart to direct additional officers, forensic teams, and surveillance
    assets to the highest-risk local government areas in real time.

    **3. Detention Status Ratios — Arrest Effectiveness & Bail Enforcement**
    The ratio of *In Custody* to *At Large* suspects is a direct measure of operational
    effectiveness. A high *At Large* figure signals gaps in arrest execution, bail enforcement,
    or suspect tracing. Units should cross-reference *At Large* cases with their case type and
    priority level to triage re-arrest operations by risk.

    **4. Case Type & Offense Category — Unit Specialisation & Training**
    The distribution of Cybercrime, Fraud, Homicide, and Armed Robbery cases guides
    unit specialisation decisions and officer training budgets. A rising proportion of
    digital offenses validates investment in Cybercrime and Forensic units, while sustained
    violent crime volumes justify dedicated Anti-Robbery task forces.

    **5. Average Response Lag — Detection & Reporting Speed**
    Average days between incident occurrence and formal reporting measure how quickly incidents
    surface through intelligence networks and community reporting. Reducing response lag —
    through community policing and digital tip-off channels — compresses the window available
    to suspects and improves forensic evidence preservation.

    **6. Court Assignment & Hearing Schedules — Case Tracking**
    The distribution across Special Offences Court, Ikeja High Court, and Magistrate Court Yaba
    signals judicial workload and potential bottlenecks. Monitoring *Next_Hearing_Date*
    distributions allows case managers to anticipate hearing clusters, prepare officer attendance
    rosters, and ensure documentation is submitted within legal deadlines.

    **7. Evidence Type & Case Outcomes — Forensic Strategy**
    Cross-referencing evidence types with case outcomes (Convicted, Acquitted, Dismissed, Pending)
    reveals which evidence categories produce the strongest prosecution results. CCTV and
    Forensic evidence correlated with higher conviction rates should anchor standard evidence
    collection protocols across all investigating units.

    ---
    *This dashboard is designed for daily briefings, command performance reviews, inter-unit
    coordination, and strategic resource planning across SCID Panti, Lagos State.*
    """)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(
    "<hr><center><small style='color:rgb(130,160,255);'>"
    "SCID Panti Lagos &nbsp;·&nbsp; Nigeria Police Force &nbsp;·&nbsp; "
    "Case Intelligence Portal v1.0 &nbsp;·&nbsp; Built with Streamlit &amp; Plotly"
    "</small></center>",
    unsafe_allow_html=True,
)
