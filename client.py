import requests
import json
import time
import datetime

token = None

def get_response_field(response, data_field=None):
    data = response.json()

    if not data_field:
        return data

    fields = data_field.split(".")

    for field in fields:
        data = data[field]
    
    return data


def get_auth_token(auth_info):
    print("get_auth_token")
    response = requests.post(auth_info["url"], data=auth_info["data"])

    if response.status_code != 200:
        print(response)
    
    return get_response_field(response, auth_info["token_field"])


def post_data(endpoint, data, headers={}, retry_get_auth_token=True):
    print("post_data")
    global token
    if token == None:
        token = get_auth_token(auth_info)
    headers["Authorization"] = 'Bearer {}'.format(token)
    response = requests.post(endpoint, data=data, headers=headers)

    if response.status_code == 401 and retry_get_auth_token:
        # token expired, refresh token and retry
        print("token expired")
        token = None
        return post_data(endpoint, auth_info, params=params, headers=headers, retry_get_auth_token=False)

    if response.status_code != 200:
        print(response)
    
    return response

def get_data(endpoint, auth_info, params={}, headers={}, retry_get_auth_token=True):
    print("get_data")
    global token
    if token == None:
        token = get_auth_token(auth_info)
    headers["Authorization"] = 'Bearer {}'.format(token)
    response = requests.get(endpoint, params=params, headers=headers)        
    
    if response.status_code == 401 and retry_get_auth_token:
        # token expired, refresh token and retry
        print("token expired")
        token = None
        return get_data(endpoint, auth_info, params=params, headers=headers, retry_get_auth_token=False)

    if response.status_code != 200:
        print(response)
    
    return response


def get_paged_results(url, auth_info, page_param_name, page=1, data_field=None, params={}, headers={}):
    results = []

    while True:
        params[page_param_name] = page
        print(params)
        response = get_data(url, auth_info, params=params, headers=headers)
        data = get_response_field(response, data_field)
        results = results + data
        page = page + 1

        time.sleep(4)

        if len(data) == 0:
            break

    return results

def get_paged_results_by_date(url, auth_info, date_from_param_name, date_to_param_name, date_from, date_to, minutes_span=10, data_field=None, params={}, headers={}):
    results = []
    time_delta = datetime.timedelta(minutes=minutes_span)
    partial_date_to = date_from
    while True:
        partial_date_from = partial_date_to
        partial_date_to = partial_date_to + time_delta
        if (partial_date_to > date_to):
            partial_date_to = date_to

        params[date_from_param_name] = partial_date_from.strftime("%m/%d/%Y, %H:%M:%S")
        params[date_to_param_name] = partial_date_to.strftime("%m/%d/%Y, %H:%M:%S")
        print(params)

        response = get_data(url, auth_info, params=params, headers=headers)
        data = get_response_field(response, data_field)
        results = results + data
        
        time.sleep(4)

        if partial_date_to >= date_to:
            break

    return results

    
if __name__=="__main__":
    # Init auth info
    auth_info = {
        "url": "http://localhost:4000/users/authenticate",
        "data": {
            "username": "test",
            "password": "test"
        },
        "token_field": "token",
    }

    # Get users paged by page and pageSize
    params = {
        "page": 1,
        "pageSize": 10
    }

    response = get_paged_results("http://localhost:4000/users", auth_info, "page", params=params)
    
    print(response)

    # Get users paged by createdDate (params from and to)
    today = datetime.datetime.now()
    delta = datetime.timedelta(minutes=60)
    date_from = today - delta 
    date_to = today

    response = get_paged_results_by_date("http://localhost:4000/users", auth_info, "from", "to", date_from, date_to, minutes_span=20)

    print(response)        