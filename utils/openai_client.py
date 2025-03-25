import openai
import os
from dotenv import load_dotenv
from transformers import pipeline

# Load the environment variables for the API Keys
load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")
openai.organization = os.getenv("OPENAI_ORG")

def get_summary_and_sentiment(professor_information):
    for key, value in professor_information.items():
        reviews = professor_information[key].get('reviews', [])
        professor_information[key].pop('reviews', None)
        
        if not reviews:
            print(f"No reviews found for key: {key}")
            continue

        comments_text = "\n".join(reviews)

        # Create a prompt for summarizing the comments
        summary_prompt = f"Please summarize all of the following comments into one paragraph, keep the response within 50 words:\n"
        # Generate a summary using the API
        #make an openai call to summarize the comments
        summary_response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo-0613",
              messages=[{"role": "system", "content": summary_prompt},
                        {"role": "user", "content": comments_text}
              ],
              temperature=0.2)
        
        # Create a prompt for summarizing the comments
        sentiment_prompt = f"ONLY Generate a real number between 0 and 1 that expresses the positive sentiment of the text.\n"
        sentiment_response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo-0613",
              messages=[{"role": "system", "content": sentiment_prompt},
                        {"role": "user", "content": comments_text}
              ],
              temperature=0.2)

        summary = summary_response.choices[0]["message"]["content"]
        sentiment = sentiment_response.choices[0]["message"]["content"]
        professor_information[key]['summary'] = summary
        professor_information[key]['sentiment'] = sentiment

    return professor_information