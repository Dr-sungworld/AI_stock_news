import FinanceDataReader as fdr
import requests
from bs4 import BeautifulSoup
from config import MARKET_KRX, MARKET_US
from utils.logger import setup_logger

logger = setup_logger(__name__)

def _scrape_naver_finance(ticker):
    url = f"https://finance.naver.com/item/main.nhn?code={ticker}"
    data = {}
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        per_tag = soup.select_one('#_per')
        pbr_tag = soup.select_one('#_pbr')
        
        if per_tag:
            data['per'] = per_tag.text.strip()
        if pbr_tag:
            data['pbr'] = pbr_tag.text.strip()
            
    except Exception as e:
        logger.warning(f"Error scraping Naver Finance for {ticker}: {e}")
        
    return data

def get_stock_data(ticker, market=MARKET_KRX):
    try:
        data = {"market": market, "ticker": ticker}
        
        if market == MARKET_KRX:
            # Price via FDR
            df = fdr.DataReader(ticker)
            if not df.empty:
                latest = df.iloc[-1]
                data["price"] = int(latest['Close'])
                data["change"] = latest['Change']
                
                # Fundamentals via Scraping
                fundamentals = _scrape_naver_finance(ticker)
                data.update(fundamentals)
                
        elif market == MARKET_US:
            # FDR supports US stocks
            df = fdr.DataReader(ticker)
            if not df.empty:
                latest = df.iloc[-1]
                data["price"] = float(latest['Close'])
                # Fundamentals not easily available via FDR for US without yfinance
                data["per"] = "N/A"
                data["pbr"] = "N/A"
            
        return data
            
    except Exception as e:
        logger.error(f"Error fetching finance data for {ticker}: {e}")
        return None
