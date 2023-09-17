from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from models import professor_information
from utils import get_professor_information
app = Flask(__name__)
CORS(app=app, threaded=True, use_reloader=True)

@app.route('/queryProfessorResults', methods=['POST'])
def query_professor_results():
    # Get the request body data
    professor_names: list = ["richard whittaker", "robert hacker", "kianoosh boroojeni"]
    response = get_professor_information.query_graphQL(professor_names)
    # comments = get_reviews.get_professor_reviews(response)
    # summary, sentiment = openai_client.get_summary_and_sentiment(comments)
    # response['summary'] = summary
    # response['sentiment'] = sentiment

    return jsonify({"professorInformationList": response})

if __name__ == '__main__':
    app.run(debug=True)