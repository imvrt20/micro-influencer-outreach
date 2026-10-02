# 🤝 AI-Powered Micro-Influencer Outreach System

An AI-powered system for discovering, filtering, scoring, enriching, and generating personalized outreach messages for micro-influencers.

## 🚀 Project Overview

This project automates the initial stages of influencer marketing outreach.

The system:

1. 📊 Loads influencer data
2. 🔎 Filters influencers based on predefined criteria
3. ⭐ Scores influencers based on engagement and audience size
4. 🧠 Enriches influencer profiles with additional categories
5. 🤖 Generates personalized collaboration messages using a local AI model
6. 🖥️ Provides an interactive Streamlit dashboard

## ✨ Features

- Influencer discovery from CSV data
- Follower and engagement filtering
- Influencer scoring system
- Audience classification
- Engagement classification
- Priority classification
- Collaboration type recommendation
- AI-generated personalized outreach
- Interactive Streamlit dashboard

## 🛠️ Tech Stack

- **Python**
- **Pandas**
- **Streamlit**
- **Ollama**
- **Gemma AI**
- **BeautifulSoup**
- **Requests**
- **python-dotenv**
- **Git & GitHub**

## 🧠 AI Personalization

The project uses a locally running **Gemma model through Ollama** to generate personalized collaboration messages.

The AI considers:

- Influencer name
- Platform
- Niche
- Followers
- Engagement rate
- Recommended collaboration type

Example:

> Hi Rahul, we love your fitness content and your engaged YouTube audience. We'd love to explore a product collaboration with you. Let us know if you'd be interested in discussing the opportunity!

## 📊 Influencer Qualification

The default filtering criteria are:

| Criteria | Requirement |
|---|---|
| Followers | 5,000 – 100,000 |
| Engagement Rate | ≥ 4% |
| Priority | Based on calculated score |

## 🏗️ Project Structure

```text
micro-influencer-outreach/
│
├── app.py
├── discovery.py
├── filtering.py
├── scoring.py
├── enrichment.py
├── personalization.py
├── influencers.csv
├── requirements.txt
├── README.md
└── .gitignore