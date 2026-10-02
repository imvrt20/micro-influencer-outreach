import pandas as pd


def discover_influencers(file_path="influencers.csv"):
    df = pd.read_csv(file_path)

    print(f"Discovered {len(df)} influencers")

    return df


if __name__ == "__main__":
    influencers = discover_influencers()

    print("\nInfluencers:")
    print(influencers.to_string(index=False))