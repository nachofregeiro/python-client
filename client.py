import requests

def get_data(endpoint, params={}):
    # self.keep_alive()
    # headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
    # response = requests.get(endpoint, headers=headers, stream=True, params=params)
    response = requests.get(endpoint, params=params)

    if response.status_code != 200:
        print(response)
    #   self._raise_on_error(response)

    return response


def get_data_field(response, data_field=None):
    data = response.json()

    if not data_field:
        return data

    fields = data_field.split(".")

    for field in fields:
        data = data[field]
    
    return data


def get_paged_results(url, page_param_name, limit_param_name, page=1, limit=20, data_field=None):
    results = []
    while True:
        print(page)
        params = {
            page_param_name: page,
            limit_param_name: limit
        }
        response = get_data(url, params=params)
        data = get_data_field(response, data_field)
        results = results + data
        page = page + 1

        if len(data) < limit:
            break

    return results

    

if __name__=="__main__":
    params = {
        'page': 1
    }

    response = get_data("https://gorest.co.in/public/v1/users", params=params)
    data = get_data_field(response)
    
    results = get_paged_results("https://gorest.co.in/public/v1/users", "page", "limit", data_field="data")
    print(len(results))


# get access token
# refresh token
# get paged results
# write results to CSV
# get all pages and write CSV or one CSV per page?             