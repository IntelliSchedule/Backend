import requests
import json

def get_cookies():
    response = requests.get(f'https://www.ratemyprofessors.com/search/professors/1322?q=*', headers={'content-type': "text/html"})
    # return the cookies as a dictionary
    return response.cookies.get_dict()

def query_graphQL():
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

    json_data = {
        'query': 'query TeacherSearchResultsPageQuery(\n  $query: TeacherSearchQuery!\n  $schoolID: ID\n) {\n  search: newSearch {\n    ...TeacherSearchPagination_search_1ZLmLD\n  }\n  school: node(id: $schoolID) {\n    __typename\n    ... on School {\n      name\n    }\n    id\n  }\n}\n\nfragment TeacherSearchPagination_search_1ZLmLD on newSearch {\n  teachers(query: $query, first: 8, after: "") {\n    didFallback\n    edges {\n      cursor\n      node {\n        ...TeacherCard_teacher\n        id\n        __typename\n      }\n    }\n    pageInfo {\n      hasNextPage\n      endCursor\n    }\n    resultCount\n    filters {\n      field\n      options {\n        value\n        id\n      }\n    }\n  }\n}\n\nfragment TeacherCard_teacher on Teacher {\n  id\n  legacyId\n  avgRating\n  numRatings\n  ...CardFeedback_teacher\n  ...CardSchool_teacher\n  ...CardName_teacher\n  ...TeacherBookmark_teacher\n}\n\nfragment CardFeedback_teacher on Teacher {\n  wouldTakeAgainPercent\n  avgDifficulty\n}\n\nfragment CardSchool_teacher on Teacher {\n  department\n  school {\n    name\n    id\n  }\n}\n\nfragment CardName_teacher on Teacher {\n  firstName\n  lastName\n}\n\nfragment TeacherBookmark_teacher on Teacher {\n  id\n  isSaved\n}\n',
        'variables': {
            'query': {
                'text': '',
                'schoolID': 'U2Nob29sLTEzMjI=',
                'fallback': True,
                'departmentID': None,
            },
            'schoolID': 'U2Nob29sLTEzMjI=',
        },
    }

    response = requests.post('https://www.ratemyprofessors.com/graphql', cookies=cookies, headers=headers, json=json_data)
    # Convert the JSON string to a Python dictionary
    parsed_data = json.loads(response.text)
    professor_information = dict()

    # Extract and display the necessary information
    for edge in parsed_data["data"]["search"]["teachers"]["edges"]:
        node = edge["node"]
        professor_information[node["firstName"] + " " + node["lastName"]] = {
            "legacyId": node["legacyId"],
            "avgDifficulty": node["avgDifficulty"],
            "avgRating": node["avgRating"],
            "wouldTakeAgainPercent": node["wouldTakeAgainPercent"] if node["wouldTakeAgainPercent"] > 0 else None,
        }

        # Loop through all other keys and print them out
        for key, value in node.items():
            if key not in ["legacyId", "firstName", "lastName"]:
                print(f"{key}: {value}")
        
        print("-----")
        return professor_information
