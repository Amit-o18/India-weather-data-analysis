import pandas as pd


def normalize_state_names(df):

    mapping = {
        "Odisha": "Orissa",
    }

    df = df.copy()
    df["state"] = df["state"].replace(mapping)

    return df