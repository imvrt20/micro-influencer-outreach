import pandas as pd


def enrich_influencers(df):
    df = df.copy()

    # Audience category
    df["audience_category"] = df["followers"].apply(
        lambda x: "Nano" if x < 10000
        else "Micro" if x <= 100000
        else "Macro"
    )

    # Engagement category
    df["engagement_category"] = df["engagement_rate"].apply(
        lambda x: "High" if x >= 7
        else "Medium" if x >= 5
        else "Low"
    )

    # Outreach priority
    df["priority"] = df["score"].apply(
        lambda x: "High" if x >= 80
        else "Medium" if x >= 60
        else "Low"
    )

    # Collaboration suggestion
    df["collaboration_type"] = df["niche"].apply(
        lambda niche:
            "Product Review" if niche in ["Technology", "Fintech"]
            else "Sponsored Post" if niche in ["Fashion", "Beauty"]
            else "Product Promotion"
    )

    return df


if __name__ == "__main__":
    df = pd.read_csv("influencers.csv")

    # Apply filtering
    df = df[
        (df["followers"] >= 5000)
        & (df["followers"] <= 100000)
        & (df["engagement_rate"] >= 4.0)
    ].copy()

    # Apply scoring
    def calculate_score(row):
        score = 0

        if row["engagement_rate"] >= 7:
            score += 40
        elif row["engagement_rate"] >= 5:
            score += 30
        else:
            score += 20

        if row["followers"] <= 25000:
            score += 40
        elif row["followers"] <= 50000:
            score += 30
        else:
            score += 20

        if row["followers"] <= 50000:
            score += 20

        return score

    df["score"] = df.apply(calculate_score, axis=1)

    enriched = enrich_influencers(df)

    print("\nEnriched Influencer Data:\n")

    print(
        enriched[
            [
                "name",
                "niche",
                "followers",
                "engagement_rate",
                "score",
                "audience_category",
                "engagement_category",
                "priority",
                "collaboration_type"
            ]
        ].to_string(index=False)
    )