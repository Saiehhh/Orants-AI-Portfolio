# prompts.py
LINKEDIN_PROMPT = """You are an expert writer. Given the article/transcript below, create:
- A LinkedIn post (max 200 words) with a 1-line hook, 2 takeaways, and a CTA "What do you think?"
Article:
{content}
"""

TWEET_THREAD_PROMPT = """Convert the content into a tweet thread of 5 tweets.
Number them 1/5 ... 5/5. Keep each tweet short and actionable.
Content:
{content}
"""

YOUTUBE_PROMPT = """Write a 2–3 minute YouTube script:
- 10s hook
- 3 main points (~30s each)
- Closing CTA
Content:
{content}
"""
