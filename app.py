from dashboard.utils.load_data import load_data
from dashboard.pages import geographic
import streamlit as st

st.set_page_config(
    page_title="Indian Weather & Rainfall Analysis",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open("dashboard/assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()
st.sidebar.title("Filters")


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



year = st.sidebar.slider(
    "Year",
    int(df["year"].min()),
    int(df["year"].max()),
    (
        int(df["year"].min()),
        int(df["year"].max())
    )
)


page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Overview",
        "🗺 Geographic Analysis",
        "🌧 Rainfall Analysis",
        "🌡 Temperature Analysis",
        "📈 Relationships",
        "📋 Dataset"
    ]
)


filtered_df = df[
    (df["state_name"].isin(state)) &
    (df["season"].isin(season)) &
    (df["year"].between(year[0], year[1]))
]

if page == "🏠 Overview":
    st.header("Overview")

elif page == "🗺 Geographic Analysis":
    geographic.show(filtered_df)

elif page == "🌧 Rainfall Analysis":
    st.header("Rainfall Analysis")






col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "States & UTs",
    df["state_name"].nunique()
)

col2.metric(
    "Average Rainfall (mm)",
    f"{filtered_df['rainfall'].mean()*100:.2f} "
)

col3.metric(
    "Average Temperature",
    f"{filtered_df['avg_temp'].mean():.2f} °C"
)

col4.metric(
    "Records",
    f"{len(filtered_df):,}"
)

st.markdown(
"""
<div class='main-title'>
🌦️ Indian Weather & Rainfall Analysis
</div>

<div class='sub-title'>
Interactive Dashboard built using Streamlit & Plotly
</div>
""",
unsafe_allow_html=True
)