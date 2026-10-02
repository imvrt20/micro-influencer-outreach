from ollama import chat

MODEL = "gemma4:e2b"

prompt = """
Write a short, professional collaboration message.

Influencer:
Name: Rahul
Platform: YouTube
Niche: Fitness
Followers: 18,500
Engagement Rate: 4.8%

Brand: FitBrand
Collaboration: Product Promotion

Requirements:
- Professional and friendly
- Personalized
- Under 80 words
- Mention why the influencer is relevant
- Include a clear collaboration invitation
- Return only the message
"""

print("Generating AI message...")

response = chat(
    model=MODEL,
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

print("\nAI MESSAGE:")
print(response.message.content)