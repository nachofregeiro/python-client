import requests
import json
import time
import datetime

def post_data(endpoint, data, headers=None):
    response = requests.post(endpoint, data=data, headers=headers)

    if response.status_code != 200:
        print(response)
    
    return response


def get_data(endpoint, params={}, headers=None):
    response = requests.get(endpoint, params=params, headers=headers)

    if response.status_code != 200:
        print(response)
    
    return response


def get_data_field(response, data_field=None):
    data = response.json()

    if not data_field:
        return data

    fields = data_field.split(".")

    for field in fields:
        data = data[field]
    
    return data

def get_auth_token(url, token_field, data={}):
    response = post_data(url, data)

    return get_data_field(response, token_field)


def get_paged_results(url, page_param_name, page=1, data_field=None, params={}, headers=None):
    results = []
    while True:
        params[page_param_name] = page
        print(params)
        response = get_data(url, params=params, headers=headers)
        data = get_data_field(response, data_field)
        results = results + data
        page = page + 1

        if len(data) == 0:
            break

    return results

def get_paged_results_by_date(url, date_from_param_name, date_to_param_name, date_from, date_to, minutes_span=10, data_field=None, params={}, headers=None):
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

        response = get_data(url, params=params, headers=headers)
        data = get_data_field(response, data_field)
        results = results + data
        
        if partial_date_to >= date_to:
            break

    return results

    

if __name__=="__main__":
    # Get auth token
    data = {
        "username": "test",
        "password": "test"
    }

    token = get_auth_token("http://localhost:4000/users/authenticate", "token", data=data)

    print(token)

    # time.sleep(30)

    headers = {'Authorization': 'Bearer {}'.format(token)}

    # Get users paged by page and pageSize
    params = {
        "page": 1,
        "pageSize": 10
    }

    response = get_paged_results("http://localhost:4000/users", "page", params=params, headers=headers)
    
    print(response)

    # Get users paged by createdDate (params from and to)
    # today = datetime.datetime.now()
    # delta = datetime.timedelta(minutes=60)
    # date_from = today - delta 
    # date_to = today

    # response = get_paged_results_by_date("http://localhost:4000/users", "from", "to", date_from, date_to, minutes_span=20, headers=headers)

    # print(response)




# get access token
# refresh token
# get paged results
# write results to CSV
# get all pages and write CSV or one CSV per page?             