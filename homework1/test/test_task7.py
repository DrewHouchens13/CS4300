'''
Implement pytest test cases to verify the correctness of your code 
when using the requests package.
'''

from src import task7
import pytest


'''
test_fetch_post_mocked(monkeypatch)
Purpose: Verify that fetch_post returns expected JSON data
using mocking with monkeypatch to avoid real HTTP requests.
'''
def test_fetch_post_mocked(monkeypatch):

    # Mock response object
    class MockResponse:
        def raise_for_status(self): pass
        def json(self):
            return {"id": 1, "title": "Mock Title"}

    # Mock requests.get to return MockResponse
    def mock_get(url):
        return MockResponse()

    monkeypatch.setattr("src.task7.requests.get", mock_get)

    data = task7.fetch_post(1)
    assert data["id"] == 1
    assert data["title"] == "Mock Title"
