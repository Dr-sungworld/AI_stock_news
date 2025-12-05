# API Key Setup Guide

This bot requires 3 API keys to function. Here is how to get each one:

## 1. Telegram Bot (Free)
You need a **Bot Token** (to control the bot) and a **Chat ID** (to know where to send messages).

### Step A: Get Bot Token
1.  Open Telegram and search for **@BotFather**.
2.  Send the message `/newbot`.
3.  Follow the instructions to name your bot (e.g., "MyStockBot" and username "MyStock_bot").
4.  BotFather will give you a **token** looking like: `123456789:ABCdefGhIJKlmNoPQR...`.
5.  **Copy this as `TELEGRAM_BOT_TOKEN`.**

### Step B: Get Chat ID
1.  Search for your new bot's username in Telegram and click **Start** or send "Hello".
2.  Open your web browser and visit this URL (replace `<YOUR_TOKEN>` with the token from Step A):
    `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3.  Look for a JSON result. Find `"chat":{"id": 123456789, ...}`.
4.  The number `123456789` is your Chat ID.
5.  **Copy this as `TELEGRAM_CHAT_ID`.**

---

## 2. Gemini API Key (Free Tier Available)
This powers the AI analysis.

1.  Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Sign in with your Google account.
3.  Click **Create API key**.
4.  Copy the key string.
5.  **Copy this as `GEMINI_API_KEY`.**

---

## 3. Serper API Key (Free Tier Available)
This powers the Google News search.

1.  Go to [serper.dev](https://serper.dev).
2.  Click **Sign Up** and create an account.
3.  Verify your email if requested.
4.  On the Dashboard, you will see your **API Key**.
5.  **Copy this as `SERPER_API_KEY`.**

---

## Where to put them?
Open the file `stock_news_alert_bot/.env` and paste them like this:

```text
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
TELEGRAM_CHAT_ID=123456789
GEMINI_API_KEY=AIzaSy...
SERPER_API_KEY=b29a...
```
