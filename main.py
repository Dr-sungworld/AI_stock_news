import schedule
import time
import asyncio
from config import WATCHLIST, SCHEDULE_INTERVAL_MINUTES
from modules.news_fetcher import fetch_news
from modules.ai_analyzer import analyze_news
from modules.finance_data import get_stock_data
from modules.telegram_bot import send_alert
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Cache to prevent duplicate alerts for the same news
# Key: News Title or URL, Value: Timestamp
news_cache = {}

def job():
    logger.info("Starting scheduled job...")
    
    # In a real scenario, we might want to search for general market news or specific news for watchlist items.
    # For this bot, let's iterate through the watchlist to find specific news, 
    # OR we could just search for "Global Stock Market News" or "Korean Stock Market News".
    # Let's try a mix. For now, let's search for "Hottest Stock Market News" or similar.
    
    # Strategy: 
    # 1. Search for generic "Stock Market News"
    # 2. Search for news related to specific high-interest themes if needed (skipped for now)
    
    queries = ["주식 시장 주요 뉴스", "Stock Market Breaking News"]
    
    all_news = []
    for q in queries:
        items = fetch_news(q, n=3)
        all_news.extend(items)
        
    # Deduplicate
    unique_news = {item['link']: item for item in all_news}.values()
    
    for news_item in unique_news:
        link = news_item.get('link')
        title = news_item.get('title')
        
        if link in news_cache:
            continue
            
        logger.info(f"Analyzing news: {title}")
        
        # AI Analysis
        analysis = analyze_news(news_item)
        
        if not analysis:
            continue
            
        # Filter by Importance (Example: Only High/Mid)
        if analysis.get('importance') == 'Low':
            logger.info(f"Skipping Low importance news: {title}")
            news_cache[link] = time.time() # Mark as seen
            continue
            
        # If important, find related stocks
        # Theme extraction gives us string names. We need to map them to Tickers if possible.
        # For this MVP, we will just pass the strings in the message, 
        # BUT we can also check if any WATCHLIST items are mentioned or relevant.
        
        related_stocks_data = []
        themes = analysis.get('themes', [])
        
        # Simple string matching with Watchlist (Naive approach)
        for stock in WATCHLIST:
            # Check if stock name is in title or themes
            if stock['name'] in title or any(stock['name'] in t for t in themes):
                data = get_stock_data(stock['ticker'], stock['market'])
                if data:
                    data['name'] = stock['name']
                    related_stocks_data.append(data)
        
        # Construct Alert Data
        alert_data = {
            "news": news_item,
            "analysis": analysis,
            "related_stocks": related_stocks_data
        }
        
        # Send Alert (Async wrapper)
        asyncio.run(send_alert(alert_data))
        
        # Mark as seen
        news_cache[link] = time.time()

def main():
    logger.info("Bot started. Scheduling jobs...")
    
    # Run once immediately for testing/demo
    job()
    
    schedule.every(SCHEDULE_INTERVAL_MINUTES).minutes.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
