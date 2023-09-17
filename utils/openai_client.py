import openai
import os
from dotenv import load_dotenv
from transformers import pipeline

# Load the environment variables for the API Keys
load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")
openai.organization = os.getenv("OPENAI_ORG")

def get_summary_and_sentiment(comments:list):
    sentiment_pipeline = pipeline("sentiment-analysis")
    # Concatenate comments into a single string, separated by new lines
    comments_text = "\n".join(comments)

    # Create a prompt for summarizing the comments
    summary_prompt = f"Please summarize all of the following comments into one paragraph:\n\n{comments_text}"
    # Generate a summary using the API
    summary_response = openai.Completion.create(
        engine="text-davinci-002",  # You can also use other engines
        prompt=summary_prompt,
        max_tokens=100
    )

    sentiment = sentiment_pipeline(comments_text)[0]['score']

    summary = summary_response.choices[0].text.strip()

    return summary, sentiment