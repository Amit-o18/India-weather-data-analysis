import streamlit as st
import pandas as pd


def show(raw_df, clean_df):

    st.title("📄 Dataset")

    st.markdown("""
    This page provides an overview of the original and cleaned weather datasets.
    It highlights the dataset structure, data quality, preprocessing steps,
    and a comparison before and after data cleaning.
    """)

    st.divider()

    st.header("📊 Dataset Comparison")

    tab1, tab2 = st.tabs(["📃 Raw Dataset", "✅ Clean Dataset"])

    with tab1:

        st.subheader("Raw Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Rows",
            f"{raw_df.shape[0]:,}"
        )

        col2.metric(
            "Columns",
            raw_df.shape[1]
        )

        col3.metric(
            "Missing Values",
            f"{raw_df.isnull().sum().sum():,}"
        )

        col4.metric(
            "Duplicate Records",
            raw_df.duplicated().sum()
        )

        st.markdown("### Dataset Preview")

        st.dataframe(
            raw_df.head(10),
            use_container_width=True
        )

    with tab2:

        st.subheader("Clean Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Rows",
            f"{clean_df.shape[0]:,}"
        )

        col2.metric(
            "Columns",
            clean_df.shape[1]
        )

        col3.metric(
            "Missing Values",
            f"{clean_df.isnull().sum().sum():,}"
        )

        col4.metric(
            "Duplicate Records",
            clean_df.duplicated().sum()
        )

        st.markdown("### Dataset Preview")

        st.dataframe(
            clean_df.head(10),
            use_container_width=True
        )

    st.divider()

    st.header("🧹 Data Cleaning Summary")

    cleaning_summary = pd.DataFrame(
        {
            "Step": [
                "Missing Value Handling",
                "Duplicate Records",
                "Data Type Conversion",
                "Feature Engineering",
                "State Information",
                "Outlier Treatment",
                "Dataset Validation"
            ],

            "Description": [
                "Filled missing rainfall, temperature, air pressure and wind speed values using appropriate median values.",
                "Checked for duplicate observations and verified dataset uniqueness.",
                "Converted date column to datetime format.",
                "Created new features: year and month number.",
                "Added full state names for better visualization and analysis.",
                "Removed unrealistic temperature values greater than 60°C.",
                "Verified the cleaned dataset before analysis."
            ]
        }
    )

    st.dataframe(
        cleaning_summary,
        use_container_width=True,
        hide_index=True
    )


    st.divider()

    st.header("📊 Before vs After Cleaning")

    comparison = pd.DataFrame(
        {
            "Feature": [
                "Rows",
                "Columns",
                "Missing Values",
                "Duplicate Records",
                "New Features Added"
            ],

            "Raw Dataset": [
                f"{raw_df.shape[0]:,}",
                raw_df.shape[1],
                f"{raw_df.isnull().sum().sum():,}",
                raw_df.duplicated().sum(),
                "-"
            ],

            "Clean Dataset": [
                f"{clean_df.shape[0]:,}",
                clean_df.shape[1],
                f"{clean_df.isnull().sum().sum():,}",
                clean_df.duplicated().sum(),
                "year, month_no, state_name"
            ]
        }
    )

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.header("📋 Feature Description")

    feature_info = pd.DataFrame(
        {
            "Feature": [
                "date_of_record",
                "state",
                "state_name",
                "district",
                "avg_temp",
                "max_temp",
                "min_temp",
                "rainfall",
                "wind_speed",
                "air_pressure",
                "elevation",
                "season",
                "month",
                "month_no",
                "year"
            ],

            "Description": [
                "Date of weather observation.",
                "State/UT code.",
                "Full name of the State or Union Territory.",
                "District where the observation was recorded.",
                "Average temperature (°C).",
                "Maximum recorded temperature (°C).",
                "Minimum recorded temperature (°C).",
                "Rainfall received (mm).",
                "Average wind speed.",
                "Atmospheric pressure (hPa).",
                "Elevation above mean sea level (m).",
                "Season corresponding to the observation.",
                "Month name.",
                "Month number (1–12).",
                "Year extracted from the observation date."
            ]
        }
    )

    st.dataframe(
        feature_info,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.header("👀 Clean Dataset Preview")

    rows = st.slider(
        "Select number of rows to display",
        min_value=5,
        max_value=100,
        value=10,
        step=5
    )

    st.dataframe(
        clean_df.head(rows),
        use_container_width=True
    )


    st.divider()

    st.success(
        """
        ✅ The dataset has been successfully cleaned, validated, and prepared for
        exploratory data analysis and interactive dashboard visualizations.
        """
    )