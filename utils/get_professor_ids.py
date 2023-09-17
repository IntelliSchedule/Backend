import requests
import json
from bs4 import BeautifulSoup
import time

class RateMyProfessorAPI:
    def __init__(self, school_id="1322"):
        self.UniversityId = school_id

    def get_professor_ids_by_name(self, professor_names:list):

        response = requests.get(f'https://www.ratemyprofessors.com/search/professors/{self.UniversityId}?q=*', headers={'content-type': "text/html"})
        time.sleep(10)
        soup = BeautifulSoup(response.content, 'html.parser')
        html_content = soup.prettify()
        quotes = soup.find_all()

        print(html_content)

