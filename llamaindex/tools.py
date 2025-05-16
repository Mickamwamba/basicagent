from serpapi import GoogleSearch 
from smolagents import tool
import os
import json
import requests


class CustomTools:

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
    
    # @tool
    def matches()->str: 
        """ 
        Pulls Match Resources from footballdata.org 

            The Match Resource reflects a scheduled football game. A game belongs to a competition and a season. 
            It owns a stage and is typically played on a certain matchday. The latter two are only attributes of a match, whereas competition and season are annotated object-like.
        
            Args:
                q: The search query string.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.
            
            Returns:
                Pulled Matches.
        """
        footballDataToken="f1ec0b3537b840d3ae6ff4d972dfb2df"
        
        url = "https://v3.football.api-sports.io/fixtures?league=39&season=2021"

        payload={}
        headers = {
        'x-rapidapi-key': 'dc9254033319e4fa9377f93f732b47a1',
        'x-rapidapi-host': 'v3.football.api-sports.io'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()['response'][:5]
