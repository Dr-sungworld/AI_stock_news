import FinanceDataReader as fdr
import mplfinance as mpf
import os
from datetime import datetime, timedelta
from utils.logger import setup_logger

logger = setup_logger(__name__)

CHART_DIR = "static/charts"
os.makedirs(CHART_DIR, exist_ok=True)

def generate_chart(ticker: str, market: str) -> str:
    """
    Generates a candlestick chart for the given ticker and saves it as an image.
    Returns the path to the saved image.
    """
    try:
        # Fetch data for last 6 months
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        
        df = fdr.DataReader(ticker, start_date, end_date)
        if df.empty:
            return ""
            
        filename = f"{ticker}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        filepath = os.path.join(CHART_DIR, filename)
        
        # Plot
        mpf.plot(
            df, 
            type='candle', 
            style='charles', 
            title=f"{ticker} Daily Chart",
            savefig=filepath,
            volume=True
        )
        
        return filepath
    except Exception as e:
        logger.error(f"Error generating chart for {ticker}: {e}")
        return ""
