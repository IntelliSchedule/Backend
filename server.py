from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from models import professor_information
from utils import get_professor_ids, openai_client, graphQL

app = Flask(__name__)
CORS(app=app)

@app.route('/queryProfessorResults', methods=['POST'])
def query_professor_results():
    # Assume you get the list of ProfessorInformation objects somehow.
    # For demonstration purposes, let's create some sample data.
    professor1 = professor_information.ProfessorInformation("Professor 1", 4.5, 0.8, 100, 100, "This is a summary.")

    professors = [professor1]

    response_list = [prof.to_dict() for prof in professors]

    # rateMyProfessorAPI = get_professor_ids.RateMyProfessorAPI(school_id="1322")
    # professor_ids = rateMyProfessorAPI.get_professor_ids_by_name(["richard whittaker"])
    # print(openai_client.get_summary_and_sentiment(["I love this product!"]))
    graphQL.query_graphQL()

    return jsonify({"professorInformationList": response_list})

if __name__ == '__main__':
    app.run(debug=True)