import streamlit as st
import pandas as pd
from ollama import chat

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Influencer Outreach",
    page_icon="🤝",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🤝 AI-Powered Micro-Influencer Outreach System")

st.write(
    "Discover, filter, score, enrich and generate personalized "
    "AI-powered collaboration messages for micro-influencers."
)

st.divider()

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv("influencers.csv")

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("🔎 Influencer Filters")

niches = ["All"] + sorted(df["niche"].unique().tolist())

selected_niche = st.sidebar.selectbox(
    "Select Niche",
    niches
)

min_followers = st.sidebar.number_input(
    "Minimum Followers",
    min_value=0,
    value=5000,
    step=1000
)

max_followers = st.sidebar.number_input(
    "Maximum Followers",
    min_value=0,
    value=100000,
    step=5000
)

min_engagement = st.sidebar.number_input(
    "Minimum Engagement (%)",
    min_value=0.0,
    value=4.0,
    step=0.5
)

# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

filtered = df[
    (df["followers"] >= min_followers)
    & (df["followers"] <= max_followers)
    & (df["engagement_rate"] >= min_engagement)
].copy()

if selected_niche != "All":
    filtered = filtered[
        filtered["niche"] == selected_niche
    ].copy()

# --------------------------------------------------
# SCORING
# --------------------------------------------------

def calculate_score(row):

    score = 0

    # Engagement score
    if row["engagement_rate"] >= 7:
        score += 40
    elif row["engagement_rate"] >= 5:
        score += 30
    else:
        score += 20

    # Audience size score
    if row["followers"] <= 25000:
        score += 40
    elif row["followers"] <= 50000:
        score += 30
    else:
        score += 20

    # Micro influencer bonus
    if row["followers"] <= 50000:
        score += 20

    return score


filtered["score"] = filtered.apply(
    calculate_score,
    axis=1
)

# --------------------------------------------------
# ENRICHMENT
# --------------------------------------------------

filtered["audience_category"] = filtered["followers"].apply(
    lambda x:
        "Nano" if x < 10000
        else "Micro" if x <= 100000
        else "Macro"
)

filtered["engagement_category"] = filtered[
    "engagement_rate"
].apply(
    lambda x:
        "High" if x >= 7
        else "Medium" if x >= 5
        else "Low"
)

filtered["priority"] = filtered["score"].apply(
    lambda x:
        "High" if x >= 80
        else "Medium" if x >= 60
        else "Low"
)

# --------------------------------------------------
# SORT
# --------------------------------------------------

filtered = filtered.sort_values(
    by="score",
    ascending=False
).reset_index(drop=True)

# --------------------------------------------------
# DASHBOARD METRICS
# --------------------------------------------------

st.subheader("📊 Campaign Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Influencers",
    len(df)
)

col2.metric(
    "Qualified",
    len(filtered)
)

col3.metric(
    "High Priority",
    len(
        filtered[
            filtered["priority"] == "High"
        ]
    )
)

col4.metric(
    "Avg Engagement",
    f"{filtered['engagement_rate'].mean():.2f}%"
    if len(filtered) > 0
    else "0%"
)

# Count generated messages
if "campaign_messages" not in st.session_state:
    st.session_state.campaign_messages = {}

col5.metric(
    "Messages Generated",
    len(st.session_state.campaign_messages)
)

st.divider()

# --------------------------------------------------
# QUALIFIED INFLUENCERS
# --------------------------------------------------

st.subheader("🎯 Qualified Influencers")

if len(filtered) > 0:

    display_columns = [
        "name",
        "platform",
        "niche",
        "followers",
        "engagement_rate",
        "score",
        "audience_category",
        "engagement_category",
        "priority"
    ]

    st.dataframe(
        filtered[display_columns],
        width="stretch",
        hide_index=True
    )

else:

    st.warning(
        "No influencers match the selected filters."
    )

# --------------------------------------------------
# EXPORT QUALIFIED INFLUENCERS
st.download_button(
    label="📥 Download Qualified Influencers",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="qualified_influencers.csv",
    mime="text/csv"
)
# --------------------------------------------------

if len(filtered) > 0:

    st.subheader("📥 Export Data")

    qualified_csv = filtered.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Qualified Influencers",
        data=qualified_csv,
        file_name="qualified_influencers.csv",
        mime="text/csv",
        width="stretch"
    )

# --------------------------------------------------
# AI MESSAGE GENERATOR
# --------------------------------------------------

st.divider()

st.subheader("🤖 AI Outreach Generator")

if len(filtered) > 0:

    influencer_name = st.selectbox(
        "Select an influencer",
        filtered["name"].tolist()
    )

    influencer = filtered[
        filtered["name"] == influencer_name
    ].iloc[0]

    st.write("### Influencer Profile")

    p1, p2, p3, p4 = st.columns(4)

    p1.metric(
        "Platform",
        influencer["platform"]
    )

    p2.metric(
        "Niche",
        influencer["niche"]
    )

    p3.metric(
        "Followers",
        f"{int(influencer['followers']):,}"
    )

    p4.metric(
        "Engagement",
        f"{influencer['engagement_rate']}%"
    )

    # ----------------------------------------------
    # GENERATE SINGLE MESSAGE
    # ----------------------------------------------

    if st.button(
        "✨ Generate Personalized Message",
        width="stretch"
    ):

        prompt = f"""
You are an experienced influencer marketing manager.

Create a highly personalized collaboration outreach message.

Influencer information:
Name: {influencer['name']}
Platform: {influencer['platform']}
Niche: {influencer['niche']}
Followers: {int(influencer['followers']):,}
Engagement Rate: {influencer['engagement_rate']}%
Priority: {influencer['priority']}

Brand:
FitBrand

Requirements:
- Address the influencer by first name.
- Mention their specific niche.
- Mention their platform naturally.
- Mention their audience size naturally.
- Explain why they are relevant to FitBrand.
- Sound human and professional.
- Do not sound like spam.
- Do not exaggerate.
- Keep it between 60 and 100 words.
- Include a clear collaboration invitation.
- Do not use emojis excessively.
- Return ONLY the outreach message.
"""

        with st.spinner(
            "🤖 AI is creating a personalized message..."
        ):

            response = chat(
                model="gemma4:e2b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                think=False,
                options={
                    "temperature": 0.7,
                    "num_predict": 300
                }
            )

        message = response.message.content.strip()

        st.session_state.campaign_messages[
            influencer["name"]
        ] = message

        st.success(
            "✅ Personalized message generated!"
        )

    # ----------------------------------------------
    # SHOW EXISTING MESSAGE
    # ----------------------------------------------

    if influencer_name in st.session_state.campaign_messages:

        st.subheader("✉️ Generated Outreach Message")

        st.text_area(
            "Message",
            st.session_state.campaign_messages[
                influencer_name
            ],
            height=200
        )

# --------------------------------------------------
# BULK OUTREACH
# --------------------------------------------------

st.divider()

st.subheader("🚀 Bulk Outreach Campaign")

st.write(
    "Generate personalized AI messages for all "
    "qualified influencers."
)

if len(filtered) > 0:

    if st.button(
        "🚀 Generate Messages for All Influencers",
        width="stretch"
    ):

        progress_bar = st.progress(0)

        status = st.empty()

        total = len(filtered)

        for index, (_, influencer) in enumerate(
            filtered.iterrows()
        ):

            status.write(
                f"Generating message for "
                f"**{influencer['name']}**..."
            )

            prompt = f"""
Create a professional personalized influencer
collaboration outreach message.

Influencer:
Name: {influencer['name']}
Platform: {influencer['platform']}
Niche: {influencer['niche']}
Followers: {int(influencer['followers']):,}
Engagement Rate: {influencer['engagement_rate']}%

Brand:
FitBrand

Requirements:
- Use the influencer's first name.
- Mention their niche.
- Mention their platform.
- Mention their audience size naturally.
- Explain why they fit the brand.
- Friendly and professional.
- Natural human tone.
- 60-100 words.
- Clear collaboration invitation.
- Return only the message.
"""

            response = chat(
                model="gemma4:e2b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                think=False,
                options={
                    "temperature": 0.7,
                    "num_predict": 300
                }
            )

            message = response.message.content.strip()

            st.session_state.campaign_messages[
                influencer["name"]
            ] = message

            progress = int(
                ((index + 1) / total) * 100
            )

            progress_bar.progress(progress)

        status.success(
            "✅ All outreach messages generated!"
        )

# --------------------------------------------------
# GENERATED CAMPAIGN
# --------------------------------------------------

if len(st.session_state.campaign_messages) > 0:

    st.divider()

    st.subheader("📨 Generated Outreach Campaign")

    campaign_rows = []

    for _, influencer in filtered.iterrows():

        name = influencer["name"]

        if name in st.session_state.campaign_messages:

            campaign_rows.append({

                "name":
                    name,

                "email":
                    influencer["email"],

                "platform":
                    influencer["platform"],

                "niche":
                    influencer["niche"],

                "followers":
                    influencer["followers"],

                "engagement_rate":
                    influencer["engagement_rate"],

                "score":
                    influencer["score"],

                "priority":
                    influencer["priority"],

                "outreach_message":
                    st.session_state
                    .campaign_messages[name]

            })

    campaign_df = pd.DataFrame(
        campaign_rows
    )

    st.dataframe(
        campaign_df,
        width="stretch",
        hide_index=True
    )

    # ----------------------------------------------
    # DOWNLOAD CAMPAIGN
    # ----------------------------------------------

    campaign_csv = campaign_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Complete Outreach Campaign",
        data=campaign_csv,
        file_name="ai_influencer_outreach_campaign.csv",
        mime="text/csv",
        width="stretch"
    )

    # ----------------------------------------------
    # CAMPAIGN STATISTICS
    # ----------------------------------------------

    st.subheader("📈 Campaign Statistics")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Messages Generated",
        len(campaign_df)
    )

    c2.metric(
        "High Priority Targets",
        len(
            campaign_df[
                campaign_df["priority"] == "High"
            ]
        )
    )

    c3.metric(
        "Average Engagement",
        f"{campaign_df['engagement_rate'].mean():.2f}%"
    )

else:

    st.info(
        "Generate outreach messages to see your "
        "campaign here."
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI-Powered Micro-Influencer Outreach System | "
    "Built with Python, Pandas, Streamlit, Ollama and Gemma"
)