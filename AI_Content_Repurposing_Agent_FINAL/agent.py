# agent.py
from gemini_client import make_client, generate_text
from content_extractors import extract_text_from_url, extract_text_from_pdf, extract_from_youtube
from prompts import LINKEDIN_PROMPT, TWEET_THREAD_PROMPT, YOUTUBE_PROMPT
import os
from dotenv import load_dotenv
import time  # ADD THIS

load_dotenv()

client = make_client()

# simple chunker: split into N-char pieces
def chunk_text(text, chunk_size=4000):
    for i in range(0, len(text), chunk_size):
        yield text[i:i+chunk_size]

def repurpose_full_text(text):
    # For long docs: summarize each chunk then combine
    if len(text) > 4000:
        chunk_summaries = []
        for i, c in enumerate(chunk_text(text, 3000)):
            print(f"Processing chunk {i+1}...")
            s = generate_text(client, f"Summarize this chunk in 5 bullets:\n\n{c}", max_output_tokens=300)
            chunk_summaries.append(s)
            time.sleep(7)  # ADD THIS - Wait 7 seconds between requests
        combined = "\n\n".join(chunk_summaries)
        source_for_generation = generate_text(client, f"Combine these chunk summaries into a concise article:\n\n{combined}", max_output_tokens=500)
        time.sleep(7)  # ADD THIS
    else:
        source_for_generation = text

    linkedin = generate_text(client, LINKEDIN_PROMPT.format(content=source_for_generation), max_output_tokens=400)
    time.sleep(7)  # ADD THIS
    
    tweets = generate_text(client, TWEET_THREAD_PROMPT.format(content=source_for_generation), max_output_tokens=400)
    time.sleep(7)  # ADD THIS
    
    youtube = generate_text(client, YOUTUBE_PROMPT.format(content=source_for_generation), max_output_tokens=600)

    return {"linkedin": linkedin, "tweets": tweets, "youtube": youtube}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--url")
    parser.add_argument("--pdf")
    parser.add_argument("--youtube")
    args = parser.parse_args()

    if args.url:
        text = extract_text_from_url(args.url)
    elif args.pdf:
        text = extract_text_from_pdf(args.pdf)
    elif args.youtube:
        text = extract_from_youtube(args.youtube)
    else:
        raise SystemExit("Provide --url or --pdf or --youtube")

    outputs = repurpose_full_text(text)
    for k, v in outputs.items():
        print(f"\n\n=== {k.upper()} ===\n{v}\n")