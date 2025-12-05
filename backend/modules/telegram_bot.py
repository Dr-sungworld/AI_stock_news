import telegram
import asyncio
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from utils.logger import setup_logger

logger = setup_logger(__name__)

async def send_alert(alert_data):
    """
    Sends a rich format message to Telegram.
    
    alert_data structure:
    {
        "news": {...},
        "analysis": {
            "importance": "High",
            "reason": "...",
            "themes": ["A", "B"],
            "historical_reaction": "..."
        },
        "finance": {
            "ticker": "005930",
            "price": 70000,
            "change": 0.5,
            "per": 10.0,
            "pbr": 1.1
        }, # Optional, if a specific stock is identified
        "related_stocks": [...] # List of finance data dicts
    }
    """
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    
    try:
        news = alert_data.get('news', {})
        analysis = alert_data.get('analysis', {})
        
        # Build Message
        importance_emoji = "" if analysis.get('importance') == 'High' else ""
        
        msg = f"{importance_emoji} *Stock News Alert* {importance_emoji}\n\n"
        msg += f" *{news.get('title')}*\n"
        msg += f"_{news.get('snippet')}_\n\n"
        
        msg += f" *AI Analysis*\n"
        msg += f" *Importance:* {analysis.get('importance')}\n"
        msg += f" *Reason:* {analysis.get('reason')}\n"
        msg += f" *Themes:* {', '.join(analysis.get('themes', []))}\n\n"
        
        msg += f" *Historical Context*\n"
        msg += f"{analysis.get('historical_reaction')}\n\n"
        
        # Financials loop
        related_stocks = alert_data.get('related_stocks', [])
        if related_stocks:
            msg += f" *Related Stocks*\n"
            for stock in related_stocks:
                ticker = stock.get('ticker')
                price = stock.get('price')
                change = stock.get('change')
                per = stock.get('per', 'N/A')
                pbr = stock.get('pbr', 'N/A')
                
                # Format change with arrow
                change_emoji = "" if change and change > 0 else "" if change and change < 0 else ""
                
                msg += f"*{stock.get('name', ticker)} ({ticker})*\n"
                msg += f"  Price: {price:,} {change_emoji} ({change})\n" # Formatting might need adjustment based on data type
                msg += f"  PER: {per} | PBR: {pbr}\n"
                msg += "\n"
                
        msg += f"[Read Article]({news.get('link')})"
        
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, parse_mode='Markdown')
        logger.info(f"Sent alert for {news.get('title')}")
        
    except Exception as e:
        logger.error(f"Error sending Telegram alert: {e}")
