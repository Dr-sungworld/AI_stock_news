import FinanceDataReader as fdr
from typing import Dict, Any, Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)

def get_financial_summary(ticker: str, market: str) -> Dict[str, Any]:
    """
    Fetches financial summary (Price, PER, PBR, etc.) using FinanceDataReader.
    """
    try:
        # FDR uses 'KRX' for Korean stocks, 'NASDAQ', 'NYSE', 'AMEX' for US.
        # We might need to map 'US' to a specific exchange or just try 'NASDAQ'.
        # For simplicity, if market is 'US', we assume it's a valid ticker for FDR (e.g., 'AAPL', 'TSLA').
        
        # Get current price
        df = fdr.DataReader(ticker)
        if df.empty:
            return {}
            
        current_price = df['Close'].iloc[-1]
        change = df['Change'].iloc[-1]
        
        # Fundamental data is harder to get reliably with just FDR for all markets without specific extensions.
        # For MVP, we return Price and Change.
        # Ideally, we would scrape Naver Finance or Yahoo Finance for PER/PBR.
        
        return {
            "price": float(current_price),
            "change": float(change),
            "currency": "KRW" if market == "KRX" else "USD"
        }
    except Exception as e:
        logger.error(f"Error fetching financials for {ticker}: {e}")
        return {}
