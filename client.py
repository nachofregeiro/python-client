import requests
import json
import time

def post_data(endpoint, data, headers=None):
    response = requests.post(endpoint, data=data, headers=headers)

    if response.status_code != 200:
        print(response)
    
    return response


def get_data(endpoint, params={}, headers=None):
    response = requests.get(endpoint, params=params, headers=headers)

    # if 401 retry

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

    

if __name__=="__main__":
    params = {
        'page': 1
    }

    # response = get_data("https://gorest.co.in/public/v1/users", params=params)
    # data = get_data_field(response)
    
    # results = get_paged_results("https://gorest.co.in/public/v1/users", "page", "limit", data_field="data")
    # print(len(results))

    data = {
        "username": "test",
        "password": "test"
    }

    response = post_data("http://localhost:4000/users/authenticate", data)

    token = get_data_field(response, "token")

    # time.sleep(30)

    params = {
        "page": 1,
        "pageSize": 5
    }

    headers = {'Authorization': 'Bearer {}'.format(token)}

    # response = get_data("http://localhost:4000/users", params=params, headers=headers)

    response = get_paged_results("http://localhost:4000/users", "page", params=params, headers=headers)
    
    print(response)




# get access token
# refresh token
# get paged results
# write results to CSV
# get all pages and write CSV or one CSV per page?             