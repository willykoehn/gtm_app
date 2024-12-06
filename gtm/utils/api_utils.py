import requests

def make_api_request(url, headers, params):
    """
    Make a GET request to an API and return the JSON response.

    Args:
        url (str): The API endpoint.
        headers (dict): Request headers.
        params (dict): Query parameters.

    Returns:
        dict: Parsed JSON response.
    """
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise ValueError(f"API request failed with status code {response.status_code}: {response.text}")
    return response.json()

