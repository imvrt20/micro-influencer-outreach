import pandas as pd


def filter_influencers(
    df,
    min_followers=5000,
    max_followers=100000,
    min_engagement=4.0
):
    filtered = df[
        (df["followers"] >= min_followers)
        & (df["followers"] <= max_followers)
        & (df["engagement_rate"] >= min_engagement)
    ].copy()

    return filtered


if __name__ == "__main__":
    df = pd.read_csv("influencers.csv")

    filtered = filter_influencers(df)

    print("\nQualified Micro-Influencers:")
    print(filtered.to_string(index=False))