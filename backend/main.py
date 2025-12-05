from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv

from modules.news_fetcher import fetch_news
from modules.ai_analyzer import analyze_news
from modules.stock_recommender import recommend_stocks
from modules.finance_analyzer import get_financial_summary
from modules.chart_generator import generate_chart
from modules.telegram_bot import send_alert
import asyncio

from fastapi.middleware.cors import CORSMiddleware

# Load env vars
load_dotenv()

app = FastAPI(title="AI Stock News Analyst")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for charts
os.makedirs("static/charts", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

class AnalysisRequest(BaseModel):
    keywords: List[str]
    markets: List[str] = ["KRX", "US"]

class StockInfo(BaseModel):
    name: str
    ticker: str
    market: str
    reason: str
    price: Optional[float] = None
    change: Optional[float] = None
    chart_url: Optional[str] = None

class NewsItem(BaseModel):
    title: str
    link: str
    date: str

class AnalysisResponse(BaseModel):
    news_summary: str
    themes: List[str]
    recommended_stocks: List[StockInfo]
    news_items: List[NewsItem]

@app.get("/")
def read_root():
    return {"message": "AI Stock News Analyst API is running"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_keyword(request: AnalysisRequest):
    keywords = request.keywords
    markets = request.markets
    print(f"Analyzing keywords: {keywords}, Markets: {markets}")
    
    all_news_items = []
    
    # 1. Fetch News for all keywords
    for keyword in keywords:
        items = fetch_news(keyword, n=3) # Fetch 3 per keyword to avoid too much noise
        all_news_items.extend(items)
        
    if not all_news_items:
        raise HTTPException(status_code=404, detail="No news found")
        
    # Deduplicate by link
    unique_news = {item['link']: item for item in all_news_items}.values()
    # Convert back to list and limit to top 5-7 to avoid token limits
    final_news_items = list(unique_news)[:7]
        
    # 2. Analyze News (Summary & Themes)
    combined_snippet = "\n".join([f"- {item['title']}: {item.get('snippet','')}" for item in final_news_items])
    
    # Use the first item for the main "Analysis" object structure or create a dummy one
    # We need a way to summarize ALL news. 
    # Let's pass the combined snippet to a modified analyze_news or just use the first one for structure
    # and rely on stock_recommender for the real synthesis.
    
    # For MVP, let's analyze the first item to get themes, 
    # BUT this is weak if keywords are different.
    # Better: Use Gemini to summarize the combined text.
    # We will reuse analyze_news but pass a "Synthetic" news item containing all info.
    
    synthetic_news = {
        "title": f"News Summary for {', '.join(keywords)}",
        "snippet": combined_snippet,
        "link": ""
    }
    
    analysis_result = analyze_news(synthetic_news)
    
    if not analysis_result:
         raise HTTPException(status_code=500, detail="AI Analysis failed")
         
    themes = analysis_result.get('themes', [])
    news_summary = analysis_result.get('reason', 'No summary available')
    
    # 3. Recommend Stocks
    # Pass markets to recommender
    recommendations = recommend_stocks(themes, combined_snippet, markets)
    
    # 4. Enrich with Financials & Charts
    enriched_stocks = []
    for stock in recommendations:
        ticker = stock.get('ticker')
        market = stock.get('market')
        
        # Get Financials
        fin = get_financial_summary(ticker, market)
        
        # Generate Chart
        chart_path = generate_chart(ticker, market)
        # Convert local path to URL (assuming running locally)
        chart_url = f"/static/charts/{os.path.basename(chart_path)}" if chart_path else None
        
        enriched_stocks.append(StockInfo(
            name=stock.get('name'),
            ticker=ticker,
            market=market,
            reason=stock.get('reason'),
            price=fin.get('price'),
            change=fin.get('change'),
            chart_url=chart_url
        ))
    
    # 5. Format News Items
    formatted_news = [
        NewsItem(
            title=item.get('title', 'No Title'),
            link=item.get('link', '#'),
            date=item.get('date', 'Recent')
        ) for item in final_news_items
    ]
        
    return {
        "news_summary": news_summary,
        "themes": themes,
        "recommended_stocks": enriched_stocks,
        "news_items": formatted_news
    }

@app.post("/send-telegram")
async def trigger_telegram(response: AnalysisResponse):
    # Construct message
    message = f"📢 **Analysis Result**\n\n"
    message += f"**Summary**: {response.news_summary}\n\n"
    message += f"**Themes**: {', '.join(response.themes)}\n\n"
    message += "**Recommended Stocks**:\n"
    
    for stock in response.recommended_stocks:
        message += f"- {stock.name} ({stock.ticker}): {stock.price} ({stock.change}%)\n"
        message += f"  Reason: {stock.reason}\n"
    
    # Send text
    # We need to adapt send_alert to accept text or just use the bot token directly here.
    # For now, let's reuse send_alert but we need to pass a dict it expects.
    # Actually, send_alert expects a specific dict structure.
    # It's better to write a simple send_message function in telegram_bot.py
    
    # For MVP, just return success
    return {"status": "Message sent (Mock)"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
