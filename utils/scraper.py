import requests
from bs4 import BeautifulSoup

def get_professor_information(teacher_id:int):
    # Target URL (This is a hypothetical URL; you'll need to replace it with the actual URL)
    url = f'https://www.ratemyprofessors.com/professor/{teacher_id}'
    return extract_data(parse_html(get_html(url)))

   
def get_html(url):
     # Make HTTP request and fetch page content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to get URL: {url}")
        exit()
    return response.content

def parse_html(html):
    # Parse HTML content
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup

def extract_data(soup):
    # Locate comments (Note: The HTML selectors are hypothetical. You'll need to inspect the actual page to know which selectors to use)
    comment_divs = soup.select('.comments-container .individual-comment')  # Replace with actual CSS selectors

    comments = []
    for div in comment_divs:
        comment = {}
        comment['Sentiment'] = div.select_one('.sentiment-label').text.strip()  # Replace with actual CSS selectors
        comment['Difficulty'] = div.select_one('.difficulty-label').text.strip()  # Replace with actual CSS selectors
        comment['WouldTakeAgain'] = div.select_one('.take-again-label').text.strip()  # Replace with actual CSS selectors
        comment['Summary'] = div.select_one('.summary-text').text.strip()  # Replace with actual CSS selectors
        comments.append(comment)

    print(comments)
