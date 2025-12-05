import requests
import json
from typing import List, Dict, Any
from config import SERPER_API_KEY
from utils.logger import setup_logger

logger = setup_logger(__name__)

def fetch_news(query: str, n: int = 5) -> List[Dict[str, Any]]:
    """
    Fetches news from Serper Dev API.
    
    Args:
        query: Search query string.
        n: Number of results to return.
        
    Returns:
        List of news items (dictionaries).
    """
    url = "https://google.serper.dev/news"
    
    # Payload construction
    payload_dict = {
        "q": query,
        "num": n,
        "tbs": "qdr:d" # Last 24 hours
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

def search_past_reaction(query: str) -> List[Dict[str, Any]]:
    """
    Searches for historical context/past reactions using Serper Dev API.
    
    Args:
        query: Search query string.
        
    Returns:
        List of search results (dictionaries).
    """
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
