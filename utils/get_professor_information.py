import requests
import json
import os

CACHE_FILENAME = 'professor_cache.json'

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

def get_cookies():
    response = requests.get(f'https://www.ratemyprofessors.com/search/professors/1322?q=*', headers={'content-type': "application/json"})
    # return the cookies as a dictionary
    return response.cookies.get_dict()

def query_graphQL(professor_names:list):
    # Load cache
    cache = load_cache()
    
    # Check if the result is already in cache
    for name in professor_names:
        if name in cache:
            professor_information[name] = cache[name]
            professor_names.remove(name)

    # If all names were found in cache, return
    if not professor_names:
        return professor_information
    cookies = get_cookies();

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
        'Authorization': 'Basic dGVzdDp0ZXN0',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://www.ratemyprofessors.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.ratemyprofessors.com/search/professors/1322?q=*',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    professor_information = dict()
    cache = dict()
    after_cursor = ""
    while True:
        json_data = {
            'query': 'query TeacherSearchResultsPageQuery(\n  $query: TeacherSearchQuery!\n  $schoolID: ID, $after: String\n) {\n  search: newSearch {\n    ...TeacherSearchPagination_search_1ZLmLD\n  }\n  school: node(id: $schoolID) {\n    __typename\n    ... on School {\n      name\n    }\n    id\n  }\n}\n\nfragment TeacherSearchPagination_search_1ZLmLD on newSearch {\n  teachers(query: $query, first: 100, after: $after) {\n    didFallback\n    edges {\n      cursor\n      node {\n        ...TeacherCard_teacher\n        id\n        __typename\n      }\n    }\n    pageInfo {\n      hasNextPage\n      endCursor\n    }\n    resultCount\n    filters {\n      field\n      options {\n        value\n        id\n      }\n    }\n  }\n}\n\nfragment TeacherCard_teacher on Teacher {\n  id\n  legacyId\n  avgRating\n  numRatings\n  ...CardFeedback_teacher\n  ...CardSchool_teacher\n  ...CardName_teacher\n  ...TeacherBookmark_teacher\n}\n\nfragment CardFeedback_teacher on Teacher {\n  wouldTakeAgainPercent\n  avgDifficulty\n}\n\nfragment CardSchool_teacher on Teacher {\n  department\n  school {\n    name\n    id\n  }\n}\n\nfragment CardName_teacher on Teacher {\n  firstName\n  lastName\n}\n\nfragment TeacherBookmark_teacher on Teacher {\n  id\n  isSaved\n}\n',
            'variables': {
                'query': {
                    'text': '',
                    'schoolID': 'U2Nob29sLTEzMjI=',
                    'fallback': True,
                    'departmentID': None, 
                },
                'schoolID': 'U2Nob29sLTEzMjI=',
                'after': after_cursor
            },
        }

        response = requests.post('https://www.ratemyprofessors.com/graphql', cookies=cookies, headers=headers, json=json_data)
        if response.status_code != 200:
            print("Error fetching data")
            break

        # Convert the JSON string to a Python dictionary
        parsed_data = json.loads(response.text)
        if 'errors' in parsed_data:
            print("GraphQL errors:", parsed_data['errors'])
            break

        # Extract and display the necessary information
        for edge in parsed_data["data"]["search"]["teachers"]["edges"]:
            node = edge["node"]
            cache[node["firstName"].lower() + " " + node["lastName"].lower()] = {
                    "legacyId": node["legacyId"],
                    "avgDifficulty": node["avgDifficulty"],
                    "avgRating": node["avgRating"],
                    "wouldTakeAgainPercent": node["wouldTakeAgainPercent"] if node["wouldTakeAgainPercent"] > 0 else None,
                }
            
            if node["firstName"].lower() + " " + node["lastName"].lower() in professor_names:
                professor_information[node["firstName"].lower() + " " + node["lastName"].lower()] = {
                    "legacyId": node["legacyId"],
                    "avgDifficulty": node["avgDifficulty"],
                    "avgRating": node["avgRating"],
                    "wouldTakeAgainPercent": node["wouldTakeAgainPercent"] if node["wouldTakeAgainPercent"] > 0 else None,
                }
                professor_names.remove(node["firstName"].lower() + " " + node["lastName"].lower())

        # Check if there are more pages
        if not parsed_data["data"]["search"]["teachers"]["pageInfo"]["hasNextPage"]:
            break

        # Update the cursor for the next iteration
        after_cursor = parsed_data["data"]["search"]["teachers"]["pageInfo"]["endCursor"]

    # Save new results to cache
    cache.update(cache)
    save_cache(cache)
    return professor_information
