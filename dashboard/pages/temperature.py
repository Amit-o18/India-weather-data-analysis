import streamlit as st
import pandas as pd
import plotly.express as px

def show(filtered_df):


    state_summary = (
    filtered_df
    .groupby("state_name", as_index=False)
    .agg(
        max_temp=("max_temp", "max"),
        min_temp=("min_temp", "min"),
        avg_temp=("avg_temp", "mean")
    )
    )

    avg_temp = state_summary["avg_temp"].mean()
    max_temp = state_summary["avg_temp"].max()
    min_temp = state_summary["avg_temp"].min()

    st.title("🌡 Temperature Analysis")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🌡 Average Temperature",
        f"{avg_temp:.1f} °C"
    )

    col2.metric(
        "🔥 Maximum",
        f"{max_temp:.1f} °C"
    )

    col3.metric(
        "❄ Minimum",
        f"{min_temp:.1f} °C"
    )

    col4.metric(
        "🗺 States",
        state_summary.shape[0]
    )


    st.subheader("🔥 Top 10 Hottest States")

    top10 = state_summary.sort_values("max_temp", ascending=False).head(10)
    fig = px.bar(
    top10,
    x="max_temp",
    y="state_name",
    orientation="h",
    color="max_temp",
    color_continuous_scale="Reds",
    text="max_temp"
    )

    fig.update_layout(
    xaxis_title="Maximum Temperature (°C)",
    yaxis_title="State",
    height=500,
    coloraxis_showscale=False,
    yaxis={"categoryorder": "total ascending"}
    )

    fig.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
    )

    fig.update_traces(
    hovertemplate=
    "<b>%{y}</b><br>"
    "Highest Recorded Temperature: %{x:.1f} °C"
    "<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
    f"{top10.iloc[0]['state_name']} recorded the highest temperature "
    f"({top10.iloc[0]['max_temp']:.1f} °C) among all states."
    )

    st.subheader("❄ Top 10 Coldest States")

    bottom10 = (
    state_summary
    .sort_values("min_temp")
    .head(10)
    )
    fig = px.bar(
    bottom10,
    x="min_temp",
    y="state_name",
    orientation="h",
    color="min_temp",
    color_continuous_scale="Blues_r",
    text="min_temp"
    )

    fig.update_layout(
    xaxis_title="Minimum Temperature (°C)",
    yaxis_title="State",
    height=500,
    coloraxis_showscale=False,
    yaxis={"categoryorder": "total ascending"}
    )

    fig.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
    )

    fig.update_traces(
    hovertemplate=
    "<b>%{y}</b><br>"
    "Lowest Recorded Temperature: %{x:.1f} °C"
    "<extra></extra>"
    )


    fig.update_layout(
    yaxis={
        "categoryorder": "array",
        "categoryarray": bottom10["state_name"].tolist()[::-1]
    }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
    f"{bottom10.iloc[0]['state_name']} recorded the lowest observed temperature "
    f"of {bottom10.iloc[0]['min_temp']:.1f} °C in the selected dataset."
    )


    st.subheader("📅 Monthly Average Temperature")

    monthly_temp = (
    filtered_df
    .groupby(["month_no", "month"], as_index=False)
    .agg(
        avg_temp=("avg_temp", "mean")
    )
    .sort_values("month_no")
    )

    monthly_temp["avg_temp"] = monthly_temp["avg_temp"].round(1)


    fig = px.line(
    monthly_temp,
    x="month",
    y="avg_temp",
    markers=True,
    labels={
        "month": "Month",
        "avg_temp": "Average Temperature (°C)"
    }
    )

    fig.update_traces(
    line=dict(width=4),
    marker=dict(size=8),
    hovertemplate=
    "<b>%{x}</b><br>"
    "Average Temperature: %{y:.1f} °C"
    "<extra></extra>"
    )

    fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Average Temperature (°C)",
    height=500,
    hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)


    st.subheader("🌦 Season-wise Average Temperature")

    season_summary = (
    filtered_df
    .groupby("season", as_index=False)
    .agg(
        avg_temp=("avg_temp", "mean")
    )
    )

    season_summary["avg_temp"] = season_summary["avg_temp"].round(1)

    season_order = [
    "Summer",
    "Monsoon",
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
    y="avg_temp",
    color="avg_temp",
    color_continuous_scale="Reds",
    text="avg_temp"
    )

    fig.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside",
    hovertemplate=
    "<b>%{x}</b><br>"
    "Average Temperature: %{y:.1f} °C"
    "<extra></extra>"
    )

    fig.update_layout(
    xaxis_title="Season",
    yaxis_title="Average Temperature (°C)",
    height=500,
    coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 Year-wise Average Temperature Trend")

    year_summary = (
    filtered_df
    .groupby("year", as_index=False)
    .agg(
        avg_temp=("avg_temp", "mean")
    )
    )

    year_summary["avg_temp"] = year_summary["avg_temp"].round(1)

    year_summary = year_summary[
    year_summary["year"] != 2025
    ]

    fig = px.line(
    year_summary,
    x="year",
    y="avg_temp",
    markers=True,
    labels={
        "year": "Year",
        "avg_temp": "Average Temperature (°C)"
    }
    )

    fig.update_traces(
    hovertemplate=
    "<b>Year: %{x}</b><br>"
    "Average Temperature: %{y:.1f} °C"
    "<extra></extra>"
    )

    fig.update_traces(
    line=dict(width=3),
    marker=dict(size=7)
    )

    fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Average Temperature (°C)",
    height=500,
    hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info(
    "Data for 2025 has been excluded from the yearly temperature trend analysis because it contains significantly fewer observations. Including this incomplete year could produce misleading yearly averages and distort the long-term trend."
    )
    
    st.subheader("🌡 Temperature Distribution")

    fig = px.histogram(
    filtered_df,
    x="avg_temp",
    nbins=50,
    labels={
        "avg_temp": "Average Temperature (°C)",
        "count": "Number of Records"
    }
    )

    fig.update_layout(
    xaxis_title="Average Temperature (°C)",
    yaxis_title="Number of Records",
    bargap=0.05
    )

    fig.update_traces(
    hovertemplate=
    "<b>Temperature Range</b><br>"
    "%{x:.1f} °C<br>"
    "Records: %{y:,}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)

    hottest_state = state_summary.loc[state_summary["max_temp"].idxmax()]
    coldest_state = state_summary.loc[state_summary["min_temp"].idxmin()]

    monthly_summary = (
    filtered_df
    .groupby("month", as_index=False)
    .agg(avg_temp=("avg_temp", "mean"))
    )

    hottest_month = monthly_summary.loc[monthly_summary["avg_temp"].idxmax()]
    coldest_month = monthly_summary.loc[monthly_summary["avg_temp"].idxmin()]

    season_temp = (
    filtered_df
    .groupby("season", as_index=False)
    .agg(avg_temp=("avg_temp", "mean"))
    )

    hottest_season = season_temp.loc[season_temp["avg_temp"].idxmax()]
    coldest_season = season_temp.loc[season_temp["avg_temp"].idxmin()]

    st.subheader("💡 Temperature Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"""
    ### 🔥 Heat Highlights

    **Warmest State:** {hottest_state['state_name']}
    ({hottest_state['max_temp']:.1f} °C)

    **Warmest Month:** {hottest_month['month']}
    ({hottest_month['avg_temp']:.1f} °C)

    **Warmest Season:** {hottest_season['season']}
    ({hottest_season['avg_temp']:.1f} °C)
    """
        )

    with col2:
        st.info(
            f"""
    ### ❄ Cold Highlights

    **Coldest State:** {coldest_state['state_name']}
    ({coldest_state['min_temp']:.1f} °C)

    **Coldest Month:** {coldest_month['month']}
    ({coldest_month['avg_temp']:.1f} °C)

    **Coldest Season:** {coldest_season['season']}
    ({coldest_season['avg_temp']:.1f} °C)
    """
        )

    