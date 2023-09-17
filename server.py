import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.get_professor_information import query_graphQL
from utils.openai_client import get_summary_and_sentiment
from utils.retrieve_reviews import get_professor_reviews

app = Flask(__name__)
CORS(app=app, threaded=True, use_reloader=True)


@app.route('/queryProfessorResults', methods=['POST'])
def query_professor_results():
    # Get the request body data
    payload = request.json
    print(f"Received payload: {payload}")

    if not isinstance(payload, dict):
        return jsonify({"error": "Invalid payload structure, expecting a dictionary"}), 400

    professor_names = payload.get('professorNames', [])

    response = query_graphQL(professor_names)
    comments = get_professor_reviews(response)
    response = get_summary_and_sentiment(comments)
    print(response)
    return jsonify({"professorInformationList": response})

if __name__ == '__main__':
    app.run(debug=True)