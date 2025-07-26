# FlatProfit Telegram Bot

This repository contains a simple Telegram bot that searches apartment listings
on CIAN using the [cianparser](https://github.com/lenarsaitov/cianparser)
scraper, compares them with rental prices in the same area and recommends
listings where the yield is higher than 8%.

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

The bot relies on `cianparser`, which scrapes the public CIAN website. Be aware
that the site layout might change at any time, which could require updates to
the parser.
