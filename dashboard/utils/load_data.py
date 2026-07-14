import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\hiii\OneDrive\Desktop\O7\Python\Project\data\cleaned_weather_data.csv")
    return df