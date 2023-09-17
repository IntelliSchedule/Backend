import openai
import os
from dotenv import load_dotenv
from transformers import pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Load the environment variables for the API Keys
load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")
openai.organization = os.getenv("OPENAI_ORG")

def get_summary_and_sentiment(professor_information):
    model_name = "distilbert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    for key, value in professor_information.items():
        reviews = professor_information[key].get('reviews', [])
        
        if not reviews:
            print(f"No reviews found for key: {key}")
            continue

        comments_text = "\n".join(reviews)

        # Create a prompt for summarizing the comments
        summary_prompt = f"Please summarize all of the following comments into one paragraph:\n"
        # Generate a summary using the API
        #make an openai call to summarize the comments
        summary_response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo-0613",
              messages=[{"role": "system", "content": summary_prompt},
                        {"role": "user", "content": comments_text}
              ],
              max_tokens=50,
              temperature=0.2)
        
        # Tokenize the comments to get the number of tokens
        tokens = tokenizer.tokenize(comments_text)
        token_ids = tokenizer.convert_tokens_to_ids(tokens)  # Convert tokens to IDs
        
        # Truncate or split tokens if they exceed the limit
        if len(tokens) > 512:
            token_ids = token_ids[:500]  # Truncating the tokens
            comments_text = tokenizer.decode(token_ids)  # Convert tokens back to text

        sentiment = sentiment_pipeline(comments_text)[0]['score']
        summary = summary_response.choices[0]["message"]["content"]
        professor_information[key]['summary'] = summary
        professor_information[key]['sentiment'] = sentiment

    return professor_information