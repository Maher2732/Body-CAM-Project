import pandas as pd
from dataset_builder import NUMERIC_COLUMNS


def train_model(df):
    df=df.copy()
    lookup={
        0:"low",
        1:"low",
        2:"medium",
        3:"medium",
        4:"high",
        5:"high"
    }
    df["risk_group"]=df["risk level"].map(lookup)
    
    
    group_shares=df["risk_group"].value_counts(normalize=True)
    baseline=group_shares.max()

    print("\n-------------Risk Groups-------------\n")
    print(group_shares.round(2))
    print(f"\nBaseline (always guess '{group_shares.idxmax()}'): {baseline:.2f}")
    