import json
from typing import List, Dict, Any
from modules.ai_analyzer import _call_gemini_api
from utils.logger import setup_logger

logger = setup_logger(__name__)

def recommend_stocks(themes: List[str], news_context: str, markets: List[str] = ["KRX", "US"]) -> List[Dict[str, str]]:
    """
    Uses Gemini to recommend stocks based on themes and news context.
    Returns a list of dicts with keys: name, ticker, market, reason.
    """
    market_str = ", ".join(markets)
    prompt = f"""
    Based on the following news context and themes:
    News: {news_context}
    Themes: {', '.join(themes)}

    Recommend 3-5 stocks from the following markets: [{market_str}] that are most likely to benefit.
    Provide the Ticker, Market (one of {market_str}), Name, and a brief Reason (in Korean).

    Output JSON format ONLY:
    [
        {{
            "name": "Samsung Electronics",
            "ticker": "005930",
            "market": "KRX",
            "reason": "..."
        }}
    ]
    """
    
    try:
        raw_text = _call_gemini_api(prompt)
        if not raw_text:
            return []
            
        cleaned_text = raw_text.replace('`json', '').replace('`', '').strip()
        stocks = json.loads(cleaned_text)
        return stocks
    except Exception as e:
        logger.error(f"Error recommending stocks: {e}")
        return []
