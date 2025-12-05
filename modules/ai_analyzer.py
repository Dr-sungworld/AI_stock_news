import requests
import json
import os
from config import GEMINI_API_KEY
from modules.news_fetcher import search_past_reaction
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Use REST API directly to avoid Python 3.8 SDK compatibility issues
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def _call_gemini_api(prompt):
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY is missing.")
        return None
        
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Parse Response
        # Structure: candidates[0].content.parts[0].text
        if "candidates" in result and result["candidates"]:
            content = result["candidates"][0]["content"]["parts"][0]["text"]
            return content
        else:
            logger.warning(f"Empty or unexpected response from Gemini: {result}")
            return None
            
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        if response is not None:
             logger.error(f"Response: {response.text}")
        return None

def analyze_news(news_item):
    """
    Analyzes news for importance, themes, and historical context.
    """
    try:
        title = news_item.get('title', '')
        snippet = news_item.get('snippet', '')
        
        # Step 1: Initial Analysis & Search Query Generation
        prompt_1 = f"""
        Analyze the following stock market news:
        Title: {title}
        Snippet: {snippet}

        Tasks:
        1. Determine Importance (High, Mid, Low) for Korean/US markets.
        2. Extract 2-3 key Theme Stocks or Sectors.
        3. Formulate a search query to find similar PAST events and their market reaction (e.g., "Apple iPhone launch stock price history").
        
        Output JSON format ONLY:
        {{
            "importance": "High/Mid/Low",
            "reason": "Brief reason...",
            "themes": ["Theme1", "Theme2"],
            "search_query": "Query string..."
        }}
        """
        
        raw_text_1 = _call_gemini_api(prompt_1)
        if not raw_text_1:
            return None
            
        # Clean JSON
        cleaned_text = raw_text_1.replace('`json', '').replace('`', '').strip()
        analysis = json.loads(cleaned_text)
        
        if analysis.get('importance') == 'Low':
            return {
                "importance": "Low",
                "reason": analysis.get('reason'),
                "themes": analysis.get('themes'),
                "historical_reaction": "N/A (Low Importance)",
                "original_news": news_item
            }
            
        # Step 2: Historical Context Search
        search_query = analysis.get('search_query')
        past_results = []
        if search_query:
            past_results = search_past_reaction(search_query)
            
        # Step 3: Synthesis
        if past_results:
            past_context = "\n".join([f"- {r.get('title')}: {r.get('snippet')}" for r in past_results])
            
            prompt_2 = f"""
            Based on the current news: "{title}"
            And these search results about similar past events:
            {past_context}
            
            Briefly summarize how the market reacted to such events in the past.
            """
            
            historical_reaction = _call_gemini_api(prompt_2)
            if not historical_reaction:
                historical_reaction = "Failed to summarize history."
        else:
            historical_reaction = "No historical context found."
            
        return {
            "importance": analysis.get('importance'),
            "reason": analysis.get('reason'),
            "themes": analysis.get('themes'),
            "historical_reaction": historical_reaction,
            "original_news": news_item
        }

    except Exception as e:
        logger.error(f"Error analyzing news: {e}")
        return None
