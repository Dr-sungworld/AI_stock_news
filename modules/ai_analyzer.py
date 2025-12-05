import google.generativeai as genai
import json
import os
from config import GEMINI_API_KEY
from modules.news_fetcher import search_past_reaction
from utils.logger import setup_logger

logger = setup_logger(__name__)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def analyze_news(news_item):
    """
    Analyzes news for importance, themes, and historical context.
    
    Args:
        news_item (dict): Contains 'title', 'snippet', 'link', 'date' from Serper.
        
    Returns:
        dict: {
            "importance": "High/Mid/Low",
            "reason": "...",
            "themes": ["Theme A", "Theme B"],
            "historical_reaction": "...",
            "original_news": news_item
        }
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
        
        Output JSON format:
        {{
            "importance": "High/Mid/Low",
            "reason": "Brief reason...",
            "themes": ["Theme1", "Theme2"],
            "search_query": "Query string..."
        }}
        """
        
        response_1 = model.generate_content(prompt_1)
        # Simple extraction - specialized JSON parsing might be needed for production
        # Assuming Gemini follows instruction well.
        cleaned_text = response_1.text.replace('`json', '').replace('`', '')
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
            
            response_2 = model.generate_content(prompt_2)
            historical_reaction = response_2.text
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
