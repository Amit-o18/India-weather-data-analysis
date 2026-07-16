import streamlit as st
import pandas as pd
import plotly.express as px

def show(filtered_df):
    
    state_summary = (
        filtered_df
        .groupby("state_name", as_index=False)
        .agg({
            "rainfall": "mean"
        })
    )

    avg_rainfall = state_summary["rainfall"].mean()
    max_rainfall = state_summary["rainfall"].max()
    min_rainfall = state_summary["rainfall"].min()
    st.title("🌧 Rainfall Analysis")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
    "🌧 Average Rainfall",
    f"{avg_rainfall:.1f} mm"
    )

    col2.metric(
        "⬆ Maximum",
        f"{max_rainfall:.1f} mm"
    )

    col3.metric(
        "⬇ Minimum",
        f"{min_rainfall:.1f} mm"
    )

    col4.metric(
        "🗺 States",
        state_summary.shape[0]
    )

    st.subheader("🌧 Top 10 Wettest States")
    state_summary["rainfall"] = state_summary["rainfall"].round(2)
    top10 = (
        state_summary
        .sort_values("rainfall", ascending=False)
        .head(10)
    )
    top10["Rainfall_mm"] = top10["rainfall"].round(2)


    fig = px.bar(
    top10,
    x="rainfall",
    y="state_name",
    orientation="h",
    color="rainfall",
    color_continuous_scale="Blues",
    text="rainfall",
    hover_data={
        "Rainfall_mm": True,
        "rainfall": False
    }
    )

    fig.update_layout(
        xaxis_title="Average Rainfall (mm)",
        yaxis_title="State",
        height=500,
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False
    )

    fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
    )

    fig.update_traces(
    hovertemplate=
    "<b>%{y}</b><br>" +
    "Average Rainfall: %{customdata[0]} mm<extra></extra>"
    )


    st.plotly_chart(fig, use_container_width=True)


    st.subheader("🏜 Top 10 Driest States")

    
    bottom10 = (
    state_summary
    .sort_values("rainfall")
    .head(10)
    )
    
    bottom10["Rainfall_mm"] = bottom10["rainfall"].round(2)
    
    fig = px.bar(
    bottom10,
    x="rainfall",
    y="state_name",
    orientation="h",
    color="rainfall",
    color_continuous_scale="Oranges_r",
    text="rainfall",
    hover_data={
        "Rainfall_mm": True,
        "rainfall": False
    }
    )

    fig.update_layout(
        xaxis_title="Average Rainfall (mm)",
        yaxis_title="State",
        height=500,
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False
    )

    fig.update_layout(
    yaxis={
        "categoryorder": "array",
        "categoryarray": bottom10["state_name"].tolist()[::-1]
    }
    )

    fig.update_traces(
    hovertemplate=
    "<b>%{y}</b><br>" +
    "Average Rainfall: %{customdata[0]} mm<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info(
    f"Rajasthan recorded the lowest average rainfall ({bottom10.iloc[0]['rainfall']:.2f} mm) "
    f"while Jammu and Kashmir was the highest among the 10 driest states ({bottom10.iloc[-1]['rainfall']:.2f} mm)."
    )

    st.subheader("📅 Monthly Average Rainfall")

    monthly_rainfall = (
        filtered_df
        .groupby(["month_no", "month"], as_index=False)
        .agg({
            "rainfall": "mean"
        })
        .sort_values("month_no")
    )

    monthly_rainfall["rainfall"] = (
    monthly_rainfall["rainfall"]
    ).round(1)

    fig = px.line(
    monthly_rainfall,
    x="month",
    y="rainfall",
    markers=True
)

    fig.update_traces(
        line=dict(width=4),
        marker=dict(size=8),
        hovertemplate=
        "<b>%{x}</b><br>"
        "Average Rainfall: %{y:.1f} mm"
        "<extra></extra>"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Average Rainfall (mm)",
        height=500,
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)



    st.subheader("🌦 Season-wise Average Rainfall")

    season_summary = (
        filtered_df
        .groupby("season", as_index=False)
        .agg({
            "rainfall": "mean"
        })
        
    )

    season_summary["rainfall"] = season_summary["rainfall"].round(1)

    season_order = [
    "Monsoon",
    "Summer",
    "Post-monsoon",
    "Winter"
    ]

    season_summary["season"] = pd.Categorical(
        season_summary["season"],
        categories=season_order,
        ordered=True
    )

    season_summary = season_summary.sort_values("season")

    fig = px.bar(
    season_summary,
    x="season",
    y="rainfall",
    color="rainfall",
    color_continuous_scale="Blues",
    text="rainfall"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
        hovertemplate=
        "<b>%{x}</b><br>"
        "Average Rainfall: %{y:.1f} mm"
        "<extra></extra>"
    )

    fig.update_layout(
        xaxis_title="Season",
        yaxis_title="Average Rainfall (mm)",
        height=500,
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🌧 Year-wise Average Rainfall Trend")

    year_summary = (
    filtered_df
    .groupby("year", as_index=False)
    .agg(rainfall=("rainfall", "mean"))
    )

    
    year_summary["rainfall"] = year_summary["rainfall"].round(1)
    year_summary = year_summary[year_summary["year"] != 2025]

    fig=px.line(
    year_summary,
    x="year",
    y="rainfall",
    markers=True,
    labels={
        'year':'Year',
        'rainfall':'Average Rainfall (mm)'
    }
    )
    
    fig.update_traces(
    hovertemplate=
    "<b>Year: %{x}</b><br>"
    "Average Rainfall: %{y:.1f} mm"
    "<extra></extra>"
    )

    fig.update_traces(
    line=dict(width=3),
    marker=dict(size=7)
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info("Data for 2025 has been excluded from the yearly rainfall trend analysis because it contains significantly fewer observations (16,773 records) compared to previous years (approximately 148,000 records per year). Including this incomplete year could produce misleading yearly averages and distort the trend.")


    st.subheader("🌧 Rainfall Distribution")

    fig = px.histogram(
        filtered_df,
        x="rainfall",
        nbins=60,
        labels={
            "rainfall": "Rainfall (mm)",
            "count": "Number of Records"
        }
    )

    
    fig.update_layout(
        xaxis_title="Rainfall (mm)",
        yaxis_title="Number of Records",
        bargap=0.05
    )

    fig.update_traces(
        hovertemplate=
        "<b>Rainfall Range</b><br>"
        "%{x:.1f} mm<br>"
        "Records: %{y:,}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)
    
    
    wettest_state = state_summary.loc[state_summary["rainfall"].idxmax()]
    driest_state = state_summary.loc[state_summary["rainfall"].idxmin()]

    wettest_month = monthly_rainfall.loc[monthly_rainfall["rainfall"].idxmax()]
    driest_month = monthly_rainfall.loc[monthly_rainfall["rainfall"].idxmin()]

    wettest_season = season_summary.loc[season_summary["rainfall"].idxmax()]
    driest_season = season_summary.loc[season_summary["rainfall"].idxmin()]



    st.subheader("💡 Rainfall Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"""
    **Wettest State:** {wettest_state['state_name']}
    ({wettest_state['rainfall']:.1f} mm)

    **Wettest Month:** {wettest_month['month']}
    ({wettest_month['rainfall']:.1f} mm)

    **Wettest Season:** {wettest_season['season']}
    ({wettest_season['rainfall']:.1f} mm)
    """
        )

    with col2:
        st.warning(
            f"""
    **Driest State:** {driest_state['state_name']}
    ({driest_state['rainfall']:.1f} mm)

    **Driest Month:** {driest_month['month']}
    ({driest_month['rainfall']:.1f} mm)

    **Driest Season:** {driest_season['season']}
    ({driest_season['rainfall']:.1f} mm)
    """
    )