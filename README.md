# Stock News Alert Bot 

A smart stock market news bot that:
1.  **Fetches News**: Uses Serper Dev to find latest market news.
2.  **Analyzes with AI**: Uses Google Gemini to determine importance, themes, and **find historical context (past market reactions)**.
3.  **Gets Finance Data**: Uses FinanceDataReader and Naver Finance to get real-time price & fundamentals (PER/PBR) for Korean (KRX) and US stocks.
4.  **Sends Alerts**: Delivers rich summaries to Telegram.

##  How to run on a new computer

Yes, this repository contains all the code you need. However, **API Keys are NOT included** for security.

### 1. Clone & Setup
`ash
git clone https://github.com/Dr-sungworld/AI_stock_news.git
cd AI_stock_news
pip install -r requirements.txt
`

### 2. Create .env file (Important!)
Create a file named .env in this directory and add your keys:
`	ext
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id
GEMINI_API_KEY=your_gemini_key
SERPER_API_KEY=your_serper_key
`
>  **How to get keys?** Read [API_GUIDE.md](API_GUIDE.md) included in this repo.

### 3. Run
`ash
python main.py
`

##  Features
*   **Automatic 10-minute Interval**: Scheduled in main.py.
*   **Watchlist**: Edit config.py to add your favorite stocks.
*   **AI History Search**: The bot autonomously searches for "How did stock X react to event Y in the past?" and summarizes it.
