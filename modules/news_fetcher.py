import requests
import json
from config import SERPER_API_KEY
from utils.logger import setup_logger

logger = setup_logger(__name__)

def fetch_news(query, n=5):
    url = "https://google.serper.dev/news"
    payload = json.dumps({
        "q": query,
        "num": n,
        "tbs": "qdr:h" # Last hour ? Or day? Planning says periodic (every 10 mins). Let's use 24h or sorted by date.
    })
    # If 10 mins, maybe qdr:h (last hour) is better to avoid dupes? Or handled by logic.
    # Plan doesn't specify window. "d" (day) is safer to catch context.
    
    # Actually, payload can't have comments in json.dumps dict.
    # Fixing that.
    payload_dict = {
        "q": query,
        "num": n,
        "tbs": "qdr:d"
    }
    
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload_dict))
        response.raise_for_status()
        results = response.json().get("news", [])
        return results
    except Exception as e:
        logger.error(f"Error fetching news for {query}: {e}")
        return []

def search_past_reaction(query):
    # Search for historical context
    search_query = f"{query} stock price reaction history"
    url = "https://google.serper.dev/search"
    payload_dict = {
        "q": search_query,
        "num": 3
    }
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload_dict))
        response.raise_for_status()
        results = response.json().get("organic", [])
        return results
    except Exception as e:
        logger.error(f"Error searching past reaction for {query}: {e}")
        return []
