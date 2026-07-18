from dashboard.utils.load_data import load_data
from dashboard.pages import geographic, rainfall, temperature, relationship, overview, dataset
import pandas as pd
import streamlit as st


raw_df = pd.read_csv("data/india_weather_rainfall_data.csv")
clean_df = pd.read_csv("data/cleaned_weather_data.csv")


st.set_page_config(
    page_title="Indian Weather & Rainfall Analysis",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<link rel="stylesheet"
href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
""", unsafe_allow_html=True)

# Load CSS
with open("dashboard/assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()

st.sidebar.markdown("""
    <div style="
    background:linear-gradient(135deg,#2563eb,#0ea5e9);
    padding:18px;
    border-radius:16px;
    text-align:center;
    margin-bottom:20px;
    box-shadow:0 4px 12px rgba(0,0,0,.25);
    ">

    <i class="bi bi-cloud-sun-fill"
    style="
    font-size:40px;
    color:white;
    "></i>

    <h2 style="
    margin:8px 0 0 0;
    color:white;
    font-weight:700;
    ">
    Weather Dashboard
    </h2>

    <p style="
    margin:5px 0 0 0;
    color:#dbeafe;
    font-size:14px;
    ">
    Indian Weather & Rainfall Analysis
    </p>

    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<h3 style="margin-bottom:8px;">
<i class="bi bi-compass-fill"></i> Navigation
</h3>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    [
        "🏠 Overview",
        "📋 Dataset",
        "🗺 Geographic Analysis",
        "🌧 Rainfall Analysis",
        "🌡 Temperature Analysis",
        "📈 Relationships"
    ]
)

year = st.sidebar.slider(
    "Year",
    int(df["year"].min()),
    int(df["year"].max()),
    (
        int(df["year"].min()),
        int(df["year"].max())
    )
)



st.sidebar.markdown("---")

st.sidebar.markdown("""
<h3 style="margin-bottom:8px;">
<i class="bi bi-funnel-fill"></i> Filters
</h3>
""", unsafe_allow_html=True)

state = st.sidebar.multiselect(
    "Select State",
    sorted(df["state_name"].unique()),
    default=sorted(df["state_name"].unique())
)


season = st.sidebar.multiselect(
    "Select Season",
    sorted(df["season"].unique()),
    default=sorted(df["season"].unique())
)

st.sidebar.markdown("---")

st.sidebar.markdown(f"""
<div style="
background:#1e293b;
padding:15px;
border-radius:14px;
border-left:5px solid #3b82f6;
">

<h4 style="margin-top:0;">
<i class="bi bi-database-fill"></i>
Dataset Summary
</h4>

<p>
<i class="bi bi-geo-alt-fill"></i>
<b>States</b>: {df["state_name"].nunique()}
</p>

<p>
<i class="bi bi-calendar-range-fill"></i>
<b>Years</b>: {df["year"].min()} - {df["year"].max()}
</p>

<p style="margin-bottom:0;">
<i class="bi bi-file-earmark-bar-graph-fill"></i>
<b>Records</b>: {len(df):,}
</p>

</div>
""", unsafe_allow_html=True)



filtered_df = df[
    (df["state_name"].isin(state)) &
    (df["season"].isin(season)) &
    (df["year"].between(year[0], year[1]))
]

if page == "🏠 Overview":
    overview.show(filtered_df)
    
elif page == "🗺 Geographic Analysis":
    geographic.show(filtered_df)

elif page == "🌧 Rainfall Analysis":
    rainfall.show(filtered_df)

elif page == "🌡 Temperature Analysis":
    temperature.show(filtered_df)

elif page == "📈 Relationships":
    relationship.show(filtered_df)

elif page == "📋 Dataset":
    dataset.show(raw_df, clean_df, filtered_df)






