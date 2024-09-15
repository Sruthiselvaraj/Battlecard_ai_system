import requests
from typing import List, Dict


API_KEYS = {
    "scrapingbee": "WVMSHMXV3XW6T2CWFNBHYS1XHZ8T24Z5NPULUBMUOZ3TYOJ72LSZSVIYJQRZI4HFDBTMO1H2UW7CKS7A",
    "google": "AIzaSyCXQZRjlMyH2-4Em380n6TQCSQOx45Pwus",
    "newsapi": "a6a28e2332334b1295b953a9b5075c9b",
}


def fetch_scrapingbee_data(url: str) -> Dict:
    headers = {"Authorization": f"Bearer {API_KEYS['scrapingbee']}"}
    response = requests.get(url, headers=headers)
    return response.json()


def fetch_google_data(query: str) -> Dict:
    api_key = API_KEYS['google']
    cx = "c3f776553e5254952"  
    response = requests.get(
        f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}"
    )
    return response.json()


def fetch_newsapi_data(query: str) -> Dict:
    api_key = API_KEYS['newsapi']
    response = requests.get(
        f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    )
    return response.json()


def collect_data(competitors: List[str], industry: str) -> Dict:
    data = {}
    
    for competitor in competitors:
  
        search_results_google = fetch_google_data(competitor)
        data[f"{competitor}_google"] = search_results_google

        
        search_results_newsapi = fetch_newsapi_data(competitor)
        data[f"{competitor}_newsapi"] = search_results_newsapi

   
    industry_info_google = fetch_google_data(industry)
    data[f"industry_{industry}_google"] = industry_info_google

    industry_info_newsapi = fetch_newsapi_data(industry)
    data[f"industry_{industry}_newsapi"] = industry_info_newsapi

    return data
