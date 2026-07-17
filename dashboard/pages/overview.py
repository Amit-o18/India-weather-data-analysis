import streamlit as st
import pandas as pd


def show(filtered_df):

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

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "States & UTs",
        filtered_df["state_name"].nunique()
    )

    col2.metric(
        "Average Observation Rainfall (mm)",
        f"{filtered_df['rainfall'].mean():.2f} "
    )

    col3.metric(
        "Average Observation Temperature",
        f"{filtered_df['avg_temp'].mean():.2f} °C"
    )

    col4.metric(
        "Records",
        f"{len(filtered_df):,}"
    )
    st.divider()

    st.header("📌 Project Overview")

    st.markdown("""
    India experiences diverse weather conditions because of its varied geography and climate. This interactive dashboard analyzes historical rainfall and weather observations across Indian states and Union Territories from 2015 to 2025. It enables users to explore rainfall, temperature, seasonal variations, and climate patterns through interactive maps, charts, and statistical visualizations.
    """)

    st.divider()
    st.header("🌍 Real-World Applications")

    st.markdown("""
    ### ✈️ Tourism & Travel
    - Compare weather conditions across Indian states.
    - Identify regions with comfortable temperatures during different seasons.
    - Assist travelers in planning trips based on historical climate patterns.

    ### 🌾 Agriculture
    - Understand seasonal rainfall and temperature trends.
    - Support crop planning and irrigation decisions using historical weather data.
    - Help farmers anticipate seasonal climate variations.

    ### 🏛 Government & Disaster Planning
    - Identify regions experiencing extreme rainfall or high temperatures.
    - Support planning for floods, droughts, heatwaves, and water resource management.
    - Provide insights useful for climate adaptation and infrastructure planning.

    ### 🌱 Environmental Awareness
    - Analyze long-term weather and rainfall trends.
    - Support studies related to climate variability.
    - Encourage sustainable environmental planning such as afforestation and water conservation in vulnerable regions.
    """)

    st.divider()
    st.header("🎯 Objectives")

    st.markdown("""
    - Analyze rainfall and temperature patterns across India.
    - Compare weather conditions among different states.
    - Study monthly, seasonal, and yearly climate variations.
    - Discover relationships between rainfall, temperature, elevation, and air pressure.
    - Present weather insights through interactive charts, maps, and tables.
    """)


    st.divider()

    st.header("🧭 Dashboard Features")

    st.markdown("""
    - 🌧 **Rainfall Analysis**: Monthly, seasonal and yearly rainfall trends.
    - 🌡 **Temperature Analysis**: Hottest, coldest and seasonal temperature patterns.
    - 🗺 **Geographic Analysis**: Interactive rainfall map and state-wise climate summary.
    - 📈 **Relationship Analysis**: Correlation heatmap, pivot tables and weather relationships.
    - 📄 **Dataset**: Explore the cleaned weather dataset and data preparation details.
    """)

    st.success(
    "Use the navigation menu on the left to explore rainfall, temperature, geographic, relationship, and dataset analyses."
    )