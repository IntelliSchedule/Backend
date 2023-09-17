import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.get_professor_information import query_graphQL
from utils.openai_client import get_summary_and_sentiment
from utils.retrieve_reviews import get_professor_reviews

app = Flask(__name__)
CORS(app=app, threaded=True, use_reloader=True)

CACHE_FILENAME = 'response_cache.json'

# Function to load cached data
def load_cache():
    if os.path.exists(CACHE_FILENAME):
        with open(CACHE_FILENAME, 'r') as f:
            return json.load(f)
    return {}

# Function to save data to cache
def save_cache(data):
    with open(CACHE_FILENAME, 'w') as f:
        json.dump(data, f)

def compare_payload_and_cache(payload):
    response = dict()
    # Load the cache
    cache = load_cache()  # Assuming load_cache is a function that returns a dictionary
    
    # Get the list of professor names from the payload
    professor_names = payload.get('professorNames', [])
    
    remaining_professor_names = []
    
    for name in professor_names:
        lowered_name = name.lower()
        if '\n' in lowered_name:
            continue

        if lowered_name in cache:
            response[lowered_name] = cache[lowered_name]
        else:
            remaining_professor_names.append(name)
    
    return response, remaining_professor_names


@app.route('/queryProfessorResults', methods=['POST'])
def query_professor_results():
    # Get the request body data
    payload = request.json
    print(f"Received payload: {payload}")

    if not isinstance(payload, dict):
        return jsonify({"error": "Invalid payload structure, expecting a dictionary"}), 400

    response, professor_names = compare_payload_and_cache(payload=payload)

    if not professor_names:
         return jsonify({"professorInformationList": response})

    print(professor_names)
    response = query_graphQL(professor_names)
    comments = get_professor_reviews(response)
    response = get_summary_and_sentiment(comments)
    save_cache(response)
    print(response)
    return jsonify({"professorInformationList": response})

if __name__ == '__main__':
    app.run(debug=True)