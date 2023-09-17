import requests

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
        # 'Cookie': '__browsiUID=6675baf5-3fcb-47a3-bad9-1151d67a8cec; _pbjs_userid_consent_data=3524755945110770; _li_dcdm_c=.ratemyprofessors.com; _lc2_fpi=5ee24c8f6482--01haf3hzvt1qsee680ty7xqhw7; _lr_env_src_ats=false; ccpa-notice-viewed-02=true; trc_cookie_storage=taboola%2520global%253Auser-id%3Ddc1221a8-56f8-4156-beb6-16369d291072-tuctb3e18cb; __li_idex_cache_e30=%7B%22nonId%22%3A%22jJtf5Hcjs2Itm9sAQrBrSLPr-yT1xSUJADWUxQ%22%7D; panoramaId_expiry=1695476450781; _cc_id=c581b1c2de31bccfffc5622717c9017e; panoramaId=0946e6d3bff2df114bea9cca55e84945a702ebaea3f333a195c7e920db801a31; pjs-unifiedid=%7B%22TDID%22%3A%226f50ef44-c668-4419-8b4e-f63dbf6469d3%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222023-08-16T13%3A40%3A50%22%7D; panoramaId_expiry=1695476452052; _cc_id=c581b1c2de31bccfffc5622717c9017e; panoramaId=0946e6d3bff2df114bea9cca55e84945a702ebaea3f333a195c7e920db801a31; userSchoolId=U2Nob29sLTEzMjI=; userSchoolLegacyId=1322; userSchoolName=Florida%20International%20University; cid=Z5oiR6-sOQ-20230916; logglytrackingsession=c4542bfa-393f-47a6-b80c-4b4c49288742; _gid=GA1.2.1197125443.1694878605; _hjSessionUser_1667000=eyJpZCI6ImZlNzEzMDMxLWY4MTMtNTQ1Yy04YjU1LTQ4MjFiMmFmMjJlMyIsImNyZWF0ZWQiOjE2OTQ4NzE2NDkzMzksImV4aXN0aW5nIjp0cnVlfQ==; _au_1d=AU1D-0100-001694878613-CFRX2ZOE-Q51L; __qca=I0-2079882716-1694878763828; _gaexp=GAX1.2.KAQZFjLxQcG_20Lp80ZSnQ.19629.0; _au_last_seen_pixels=eyJhcG4iOjE2OTQ4Nzg2MTMsInR0ZCI6MTY5NDg3ODYxMywicHViIjoxNjk0ODc4NjEzLCJydWIiOjE2OTQ4Nzg2MTMsInRhcGFkIjoxNjk0ODc4NjEzLCJhZHgiOjE2OTQ4Nzg2MTMsImdvbyI6MTY5NDg3ODYxMywidGFib29sYSI6MTY5NDg3ODYxMywic21hcnQiOjE2OTQ4Nzg2MTMsInNvbiI6MTY5NDg3ODYxMywiaW1wciI6MTY5NDg4MTY2NiwiYWRvIjoxNjk0ODgxNjY2LCJwcG50IjoxNjk0ODgxNjY2LCJiZWVzIjoxNjk0ODgxNjY2LCJvcGVueCI6MTY5NDg4MTY2NiwiY29sb3NzdXMiOjE2OTQ4ODE2NjYsInVucnVseSI6MTY5NDg4MTY2NiwiYW1vIjoxNjk0ODgxNjY2fQ%3D%3D; _gat=1; _hjIncludedInSessionSample_1667000=0; _hjSession_1667000=eyJpZCI6ImNmYzZjOTAyLWY2MWYtNDRmMC1iODZiLTQyYTU4ZmFmMzY2OSIsImNyZWF0ZWQiOjE2OTQ5MDIxMjc4OTksImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; _lr_retry_request=true; __gads=ID=9a4059ce8d365319:T=1694871650:RT=1694902131:S=ALNI_MZaQy6ZMrEL1oK7Ryo1ghZfmsbIMA; __gpi=UID=000009fd0d635ec7:T=1694871650:RT=1694902131:S=ALNI_MZ7NaJySuio6MfDl2aoZ5L1_SxMsw; _ga=GA1.1.569440091.1694871649; _ga_J1PYGTS7GG=GS1.2.1694902128.2.1.1694902143.0.0.0; cto_bundle=7Lishl8zTldxMldtZHpkTTRnbTFHQWtjSHcwcEVxWHIlMkZjUkNYVmhIU09GelYlMkZQZ2dZUkIzRXJFT1RuSXpwVnRjdVVkQzRNZUtSOGslMkJxYkdJJTJCMnFrOWg5YVJvZnB2c09tMDVQT1RRNVJTbTliRmtlYiUyQmRjall1NWc2a0ZnaGtEY2FUVXpaa0xiWDVTZjlVWm82RE13U1VjOSUyRkRjcmc4UTQwRzVKZVJoTUlaM1NiaDglM0Q; cto_bidid=3D4H5V93RUlHZ1ZUWVBKdFhPUiUyQmtzVDN5cE9uWTVVeGpyVG9ld2szVzc5clE3Yjc5ZmdyU2FJcDdudDRoYUNvRmw2UDRTZzYlMkZhTEVQNGFwNlZwRHRUVnVGczd0ZjVHJTJGQ2Z2JTJCdXFCTjNHQ1E5UzhqbWk2YW5SekdWaThnWTdHRVVTUXB5; _ga_WET17VWCJ3=GS1.1.1694902128.5.1.1694902162.0.0.0',
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
    print(response.text)
