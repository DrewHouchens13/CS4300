''' 
task7.py
Demonstrates using the requests package to fetch JSON data from an API.
'''


import requests


"""
fetch_post(post_id)
Fetches a JSON placeholder post by ID from the public test API.
"""
def fetch_post(post_id):

    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response = requests.get(url)
    response.raise_for_status()  # Raise error if request failed
    return response.json()
