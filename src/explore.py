import pandas as pd

from dataset_builder import NUMERIC_COLUMNS


def show_risk_levels(df):
    risk_counts = df["risk level"].value_counts().sort_index()
    percentage = (risk_counts / len(df) * 100).round(1)
    print(pd.DataFrame({"rows": risk_counts, "percent": percentage}))


def show_missing(df):
    empty_cells = (df.isna().mean() * 100).round(1)
    empty_cells = empty_cells[empty_cells > 0].sort_values(ascending=False)
    print(empty_cells)


def show_rows_per_video(df):
    count_per_video = df.groupby("video ID").size().sort_values(ascending=False)
    print(count_per_video.head())
    print(count_per_video.describe())


def show_cat_risk(df):
    cols_list = ["type of instance", "location", "activity", "weapon", "role"]
    for col in cols_list:
        print(f"{col}:")
        print(
            df.groupby(col)["risk level"].agg(["size", "mean"]).round(2),
            "\n-----------------------------",
        )


def show_correlations(df):
    risk_corr = (
        df[NUMERIC_COLUMNS]
        .corrwith(df["risk level"], method="spearman")
        .drop("risk level")
        .sort_values(ascending=False)
        .round(2)
    )
    print(risk_corr)


def explore_data(df):
    df = df.copy()
    df["role"] = df["person"].str[0].map({"p": "police", "s": "suspect"})

    print("\n-------------Risk Levels-------------\n")
    show_risk_levels(df)

    print("\n-------------Missing Values-------------\n")
    show_missing(df)

    print("\n-------------Rows Per Video-------------\n")
    show_rows_per_video(df)

    print("\n-------------Correlations-------------\n")
    show_correlations(df)

    print("\n-------------Category Risk-------------\n")
    show_cat_risk(df)
