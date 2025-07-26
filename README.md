# FlatProfit Telegram Bot

This repository contains a simple Telegram bot that searches apartment listings on CIAN,
compares them with rental prices in the same area and recommends listings where the
yield is higher than 8%.

## Running the bot

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Export your Telegram bot token in the `TELEGRAM_TOKEN` environment variable.
3. Run the bot:
   ```bash
   python bot.py
   ```

The bot supports the command `/recommend` that searches Moscow sale offers up to
40 million rubles and rental offers in the city. It replies with apartments where
the estimated yield is above 8%.

**Note**: The CIAN API is used via simple HTTP requests and may change at any time.
The scraper implementation in this repository is basic and might require updates if
the website structure changes.
