import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

def show(filtered_df):

    st.title("📈 Relationship Analysis")
    st.subheader("📊 Correlation Between Weather Variables")

    corr = filtered_df[
        [
            "rainfall",
            "avg_temp",
            "min_temp",
            "max_temp",
            "wind_speed",
            "air_pressure",
            "elevation"
        ]
    ].corr()

    corr = corr.rename(
        columns={
            "rainfall": "Rainfall",
            "avg_temp": "Avg Temp",
            "min_temp": "Min Temp",
            "max_temp": "Max Temp",
            "wind_speed": "Wind Speed",
            "air_pressure": "Air Pressure",
            "elevation": "Elevation"
        },
        index={
            "rainfall": "Rainfall",
            "avg_temp": "Avg Temp",
            "min_temp": "Min Temp",
            "max_temp": "Max Temp",
            "wind_speed": "Wind Speed",
            "air_pressure": "Air Pressure",
            "elevation": "Elevation"
        }
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.index,
            text=corr.round(2).values,
            texttemplate="%{text}",
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            colorbar_title="Correlation"
        )
    )

    fig.update_layout(
        height=700,
        xaxis_title="Weather Variables",
        yaxis_title="Weather Variables"
    )

    fig.update_traces(
        hovertemplate=
        "<b>%{x}</b> vs <b>%{y}</b><br>"
        "Correlation: %{z:.2f}"
        "<extra></extra>"
    )

    fig.update_layout(
    height=700,
    xaxis_title="Weather Variables",
    yaxis_title="Weather Variables",
    yaxis=dict(autorange="reversed")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Average, minimum and maximum temperatures are strongly positively correlated. "
        "Air pressure shows a moderate negative relationship with temperature, while "
        "rainfall has relatively weak linear correlations with the selected weather variables."
    )

    st.subheader("📋 State-wise Seasonal Rainfall Summary")

    pivot = pd.pivot_table(
        filtered_df,
        index="state_name",
        columns="season",
        values="rainfall",
        aggfunc="mean"
    )

    season_order = [
        "Summer",
        "Monsoon",
        "Post-monsoon",
        "Winter"
    ]

    pivot = pivot.reindex(columns=season_order)
    pivot = pivot.round(1)

    

    pivot = pivot.style.format("{:.1f}") \
    .background_gradient(cmap="Blues", axis=0)

    st.dataframe(pivot, use_container_width=True)
    st.info(
    "This pivot table summarizes the average rainfall (mm) for each state across different seasons. "
    "Darker cells indicate higher average rainfall, making seasonal rainfall patterns easy to compare."
    )

    st.subheader("📋 State-wise Weather Summary")

    pivot = pd.pivot_table(
        filtered_df,
        index="state_name",
        values=[
           "rainfall",
           "avg_temp",
           "max_temp",
           "min_temp"
        ],
        aggfunc={
        "rainfall": "mean",
        "avg_temp": "mean",
        "max_temp": "max",
        "min_temp": "min"
        }
        ).round(1)

    pivot = pivot.rename(
    columns={
        "rainfall": "Avg Rainfall (mm)",
        "avg_temp": "Avg Temp (°C)",
        "max_temp": "Max Temp (°C)",
        "min_temp": "Min Temp (°C)"
    }
    )

    pivot = pivot.style.format("{:.1f}") \
    .background_gradient(cmap="ocean", axis=0)

    st.dataframe(
            pivot,
            use_container_width=True
        )

    st.info(
    "This summary table provides key weather statistics for each state. "
    "It includes average rainfall, average temperature, highest recorded maximum temperature, "
    "and lowest recorded minimum temperature, allowing quick comparison of long-term weather patterns across states."
    )

    st.subheader("🌧 Rainfall vs Average Temperature")

    scatter_df = (
    filtered_df
    .groupby("state_name", as_index=False)
    .agg(
        rainfall=("rainfall", "mean"),
        avg_temp=("avg_temp", "mean")
    )
    )

    scatter_df = scatter_df.round(2)

    fig = px.scatter(
    scatter_df,
    x="avg_temp",
    y="rainfall",
    text="state_name",
    trendline="ols",
    color="rainfall",
    color_continuous_scale="Blues",
    labels={
        "avg_temp": "Average Temperature (°C)",
        "rainfall": "Average Rainfall (mm)"
    }
    )

    fig.update_traces(
    textposition="top center",
    marker=dict(size=10),
    hovertemplate=
    "<b>%{text}</b><br>"
    "Average Temperature: %{x:.1f} °C<br>"
    "Average Rainfall: %{y:.1f} mm"
    "<extra></extra>"
    )

    fig.update_layout(
    height=600,
    xaxis_title="Average Temperature (°C)",
    yaxis_title="Average Rainfall (mm)",
    coloraxis_showscale=False
    )

    st.plotly_chart(
    fig,
    use_container_width=True
    )

    st.info(
    "Each point represents a state. The trend line indicates that average rainfall and average temperature have only a weak relationship, suggesting rainfall is influenced by multiple climatic factors rather than temperature alone."
    )