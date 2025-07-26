import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from cian import fetch_offers, extract_prices, compute_yield, MOSCOW_REGION_ID

TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN environment variable not set")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Use /recommend to receive Moscow listings with yield above 8%"
    )


async def recommend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    BUDGET_RUB = 40_000_000

    try:
        sale_offers_raw = fetch_offers(MOSCOW_REGION_ID, "sale", price_to=BUDGET_RUB)
        rent_offers_raw = fetch_offers(MOSCOW_REGION_ID, "rent")
    except Exception as exc:
        await update.message.reply_text(f"Failed to fetch offers: {exc}")
        return

    sale_offers = extract_prices(sale_offers_raw)
    rent_offers = extract_prices(rent_offers_raw)

    if not sale_offers or not rent_offers:
        await update.message.reply_text("No offers found")
        return

    avg_rent = sum(o["price"] for o in rent_offers) / len(rent_offers)

    results = []
    for offer in sale_offers:
        yld = compute_yield(offer["price"], avg_rent)
        if yld >= 0.08:
            results.append(f"{offer['address']}: yield {yld*100:.2f}%")

    if results:
        await update.message.reply_text("\n".join(results))
    else:
        await update.message.reply_text("No listings with yield above 8%")


def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("recommend", recommend))
    application.run_polling()


if __name__ == "__main__":
    main()
