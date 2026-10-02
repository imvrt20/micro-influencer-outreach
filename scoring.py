import pandas as pd


def calculate_score(row):
    score = 0

    # Engagement score
    if row["engagement_rate"] >= 7:
        score += 40
    elif row["engagement_rate"] >= 5:
        score += 30
    else:
        score += 20

    # Follower score
    if row["followers"] <= 25000:
        score += 40
    elif row["followers"] <= 50000:
        score += 30
    else:
        score += 20

    # Micro-influencer bonus
    if row["followers"] <= 50000:
        score += 20

    return score


def score_influencers(df):
    df = df.copy()
    df["score"] = df.apply(calculate_score, axis=1)

    return df.sort_values("score", ascending=False)


if __name__ == "__main__":
    df = pd.read_csv("influencers.csv")

    # Apply the same filtering criteria
    filtered = df[
        (df["followers"] >= 5000)
        & (df["followers"] <= 100000)
        & (df["engagement_rate"] >= 4.0)
    ].copy()

    scored = score_influencers(filtered)

    print("\nScored Influencers:")
    print(
        scored[
            ["name", "platform", "niche",
             "followers", "engagement_rate", "score"]
        ].to_string(index=False)
    )