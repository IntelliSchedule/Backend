from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from models import professor_information
from utils import get_professor_information
app = Flask(__name__)
CORS(app=app)

@app.route('/queryProfessorResults', methods=['POST'])
def query_professor_results():
    # Get the request body data
    professor_names = ["richard whittaker", "robert hacker", "Antonio Hernandez"]

    response = get_professor_information.query_graphQL(professor_names)
    

    return jsonify({"professorInformationList": response})

if __name__ == '__main__':
    app.run(debug=True)