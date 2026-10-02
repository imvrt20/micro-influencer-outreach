# 🤝 AI-Powered Micro-Influencer Outreach System

An AI-powered automation system that helps identify, filter, score,
enrich and generate personalized collaboration messages for
micro-influencers.

## 🚀 Project Overview

Influencer marketing teams often spend significant time manually
finding suitable influencers and writing personalized outreach
messages.

This project automates the workflow using Python, Pandas, Streamlit
and a locally running Gemma AI model through Ollama.

## ✨ Features

- 🔎 Influencer discovery from structured dataset
- 🎯 Micro-influencer filtering
- 📊 Influencer scoring
- 🏷️ Audience and engagement classification
- ⭐ Priority classification
- 🤖 AI-powered personalized outreach
- 🚀 Bulk outreach message generation
- 📧 Email information included in campaigns
- 📥 CSV export
- 📈 Campaign statistics
- 🖥️ Interactive Streamlit dashboard
- 🔒 Local AI inference using Ollama

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core development |
| Pandas | Data processing |
| Streamlit | Web dashboard |
| Ollama | Local AI inference |
| Gemma | AI message generation |
| CSV | Influencer data storage |

## 🏗️ System Architecture

```text
                 Influencer Dataset
                         │
                         ▼
                ┌─────────────────┐
                │    Discovery    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    Filtering    │
                │ Followers +     │
                │ Engagement      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │     Scoring     │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Enrichment    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Streamlit UI    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Ollama + Gemma  │
                │ AI Personalize  │
                └────────┬────────┘
                         │
                         ▼
                Personalized Outreach
                         │
                         ▼
                    CSV Export