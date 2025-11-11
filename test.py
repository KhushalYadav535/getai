import requests
from urllib.parse import urlparse, urlunparse

def get_actual_url(url):
    response = requests.get(url)
    actual_url = response.url
    return actual_url

def remove_query_params(url):
    parsed_url = urlparse(url)
    cleaned_url = urlunparse(parsed_url._replace(query=''))
    return cleaned_url

# Usage example:
url = "https://gpte.ai/writing/copymatic/"
actual_url = get_actual_url(url)
cleaned_url = remove_query_params(actual_url)

