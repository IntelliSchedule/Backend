from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from models import professor_information

app = Flask(__name__)
CORS(app=app)

@app.route('/queryProfessorResults', methods=['POST'])
def create_professors():
    # Assume you get the list of ProfessorInformation objects somehow.
    # For demonstration purposes, let's create some sample data.
    professor1 = professor_information.ProfessorInformation("Professor 1", 4.5, 0.8, 100, 100, "This is a summary.")

    professors = [professor1]

    response_list = [prof.to_dict() for prof in professors]

    return jsonify({"professorInformationList": response_list})

if __name__ == '__main__':
    app.run(debug=True)