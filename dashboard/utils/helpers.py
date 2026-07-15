import pandas as pd


def normalize_state_names(df):

    df = df.copy()

    df["state_name"] = df["state_name"].replace({

        "Andaman and Nicobar Islands": "Andaman and Nicobar",

        "Odisha": "Orissa",

        "Uttarakhand": "Uttaranchal"

    })

    return df