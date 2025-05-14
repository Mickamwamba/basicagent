from serpapi import GoogleSearch 
from smolagents import tool
import os


class GoogleSearchTool:
    
    def __init__(self):
        pass
    @tool
    def search(q:str)->str:
        """
        Perform a search operation.
    
        Args:
            q: The search query string.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        
        Returns:
            Search results.
        """

        params = {
        "engine": "google_light",
        "q": q,
        "google_domain": "google.com",
        "hl": "en",
        "gl": "us",
        "api_key": "7e3eff78aa7a2e58d11f9c0d1627db3c68d635012f4646b8011f503816d11469"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results["organic_results"]
        return organic_results