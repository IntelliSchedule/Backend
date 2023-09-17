import requests
from bs4 import BeautifulSoup
import re

def get_professor_reviews(professor_information):
    for key, value in professor_information.items():
    # Fetch the web page
        professorId = value['legacyId']
        url = f"https://www.ratemyprofessors.com/professor/{professorId}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the ul containing all reviews
        reviews_ul = soup.find('ul', {'id': 'ratingsList'})

        # Initialize an empty list to hold review objects
        reviews_list = []

        # Loop through each li (review) in the ul
        if reviews_ul:  # Check if reviews_ul is not None
            for li in reviews_ul.find_all('li'):
                # Using CSS selector to find the review comment directly
                comment_elem_by_selector = li.select_one('div > div > div.Rating__RatingInfo-sc-1rhvpxz-3.kEVEoU > div.Comments__StyledComments-dzzyvm-0.gRjWel')
                
                # Update the review_object dictionary if the comment element is found
                if comment_elem_by_selector:
                    reviews_list.append(comment_elem_by_selector.text.strip())
                
        professor_information[key]['reviews'] = reviews_list
    return professor_information

    