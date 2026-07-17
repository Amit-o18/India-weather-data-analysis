import streamlit as st
import pandas as pd
import plotly.express as px
import json

from dashboard.utils.helpers import normalize_state_names

with open("dashboard/assets/india_states.geojson", "r", encoding="utf-8") as f:
    india_map = json.load(f)


def show(filtered_df):

    st.title("🗺 Geographic Analysis")

    st.markdown("### Average Rainfall Across India")

    st.divider()

    filtered_df = normalize_state_names(filtered_df)


    state_map = (
    filtered_df
    .groupby("state_name")
    .agg(
        Rainfall=("rainfall", "mean"),
        Temperature=("avg_temp", "mean"),
        Records=("state_name", "count")
    )
    .reset_index()
    )

    

    

    geo_states = []

    for feature in india_map["features"]:
        geo_states.append(feature["properties"]["NAME_1"])

    geo_df = pd.DataFrame({
        "state_name": geo_states
    })

    


    map_df = geo_df.merge(
    state_map,
    on="state_name",
    how="left"
    )

    map_df["display_name"] = map_df["state_name"]

    map_df.loc[
        map_df["display_name"] == "Dadra and Nagar Haveli and Daman and Diu",
        "display_name"
    ] = "Dadra and Nagar Haveli"


    

    missing = map_df[map_df["Rainfall"].isna()]

    

   

    map_df["Status"] = map_df["Rainfall"].apply(
    lambda x: "Available" if pd.notna(x) else "No Data"
    )

    
    map_df["Rainfall"] = map_df["Rainfall"].fillna(-1)

    map_df["Temperature"] = map_df["Temperature"].round(1)

    map_df["Records"] = map_df["Records"].fillna(0).astype(int)

    map_df["Rainfall"] = map_df["Rainfall"].round(1)


    
    
    map_df["Map_Color"] = map_df["Rainfall"]

    map_df.loc[
        map_df["Status"] == "No Data",
        "Map_Color"
    ] = 0

    map_df["Display_Name"] = map_df["state_name"].replace({
    "Uttaranchal": "Uttarakhand",
    "Orissa": "Odisha"
    })

    available_df = map_df[map_df["Status"] == "Available"]

    missing_df = map_df[map_df["Status"] == "No Data"]

    fig = px.choropleth(
    available_df,
    geojson=india_map,
    locations="state_name",
    featureidkey="properties.NAME_1",

    color="Map_Color",

    hover_name="display_name",

    hover_data={
    "Rainfall":":.1f",
    "Temperature":":.1f",
    "Records":":,",
    "Status":True
    },
    color_continuous_scale="Blues",

    range_color=(0, map_df["Rainfall"].max())
    )

    fig.update_geos(
    fitbounds="locations",
    visible=False
    )

    fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    coloraxis_colorbar=dict(
        title="Rainfall (mm)",
        thickness=18,
        len=0.7
        )
    )

    fig.update_geos(
    fitbounds="locations",
    visible=False,
    showcountries=False,
    showcoastlines=False,
    showframe=False
    )

    fig.update_traces(
    hovertemplate=
    "<b>%{hovertext}</b><br><br>"
    "🌧 Rainfall: %{customdata[0]:.1f} mm<br>"
    "🌡 Temperature: %{customdata[1]:.1f} °C<br>"
    "📄 Records: %{customdata[2]:,}<br>"
    "Status: %{customdata[3]}<extra></extra>"
    )
    

    fig.add_choropleth(
    geojson=india_map,
    locations=missing_df["state_name"],
    featureidkey="properties.NAME_1",

    z=[1] * len(missing_df),

    colorscale=[[0, "#BDBDBD"], [1, "#BDBDBD"]],
    showscale=False,

    hovertext=[
    f"<b>{'Uttarakhand' if s=='Uttaranchal' else 'Odisha' if s=='Orissa' else s}</b>"
    "<br><br>"
    "⚠ No weather data available"
    "<br>"
    "State exists in the map"
    "<br>"
    "but no matching records exist in the dataset."
    for s in missing_df["state_name"]
    ],
    hoverinfo="text"
    )


    st.plotly_chart(fig, use_container_width=True)


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🌧 Avg Rainfall",
            f"{map_df['Rainfall'].mean():.1f} mm"
        )

    with col2:
        st.metric(
            "🌡 Avg Temperature",
            f"{map_df['Temperature'].mean():.1f} °C"
        )

    with col3:
        st.metric(
            "🗺 States / UTs",
            map_df.shape[0]
        )

    with col4:
        st.metric(
            "📄 Records",
            f"{filtered_df.shape[0]:,}"
        )

    
    st.subheader("📋 State-wise Geographic Summary")

    geo_summary = (
    filtered_df
    .groupby("state_name", as_index=False)
    .agg(
        rainfall=("rainfall", "mean"),
        avg_temp=("avg_temp", "mean"),
        elevation=("elevation", "mean")
    )
    )

    geo_summary = geo_summary.round(1)

    geo_summary = geo_summary.rename(
    columns={
        "state_name": "State",
        "rainfall": "Avg Rainfall (mm)",
        "avg_temp": "Avg Temperature (°C)",
        "elevation": "Elevation (m)"
    }
    )

    geo_summary = geo_summary.sort_values(
    "Avg Rainfall (mm)",
    ascending=False
    )

    styled_table = (
    geo_summary.style
    .format({
        "Avg Rainfall (mm)": "{:.1f}",
        "Avg Temperature (°C)": "{:.1f}",
        "Elevation (m)": "{:.0f}"
    })
    .background_gradient(
        subset=["Avg Rainfall (mm)"],
        cmap="Blues"
    )
    .background_gradient(
        subset=["Avg Temperature (°C)"],
        cmap="Oranges"
    )
    .background_gradient(
        subset=["Elevation (m)"],
        cmap="Greens"
    )
    )

    st.dataframe(
    styled_table,
    use_container_width=True
    )

    st.info(
    "This table summarizes the average rainfall, average temperature, and average elevation for each state. "
    "It complements the choropleth map by allowing quick comparison of key geographic and climatic characteristics across India."
    )
    

    wettest = geo_summary.loc[
    geo_summary["Avg Rainfall (mm)"].idxmax()
    ]

    driest = geo_summary.loc[
        geo_summary["Avg Rainfall (mm)"].idxmin()
    ]

    highest = geo_summary.loc[
        geo_summary["Elevation (m)"].idxmax()
    ]

    lowest = geo_summary.loc[
        geo_summary["Elevation (m)"].idxmin()
    ]

    st.subheader("💡 Geographic Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"""
    ### 🌧 Rainfall Highlights

    **Wettest State:** {wettest['State']}
    ({wettest['Avg Rainfall (mm)']:.1f} mm)

    **Driest State:** {driest['State']}
    ({driest['Avg Rainfall (mm)']:.1f} mm)
    """
        )


    with col2:
        st.info(
            f"""
    ### ⛰ Geographic Highlights

    **Highest Elevation:** {highest['State']}
    ({highest['Elevation (m)']:.0f} m)

    **Lowest Elevation:** {lowest['State']}
    ({lowest['Elevation (m)']:.0f} m)
    """
        )