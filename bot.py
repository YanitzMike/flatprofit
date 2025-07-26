import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from cian import fetch_offers, extract_prices, compute_yield

TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN environment variable not set")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Use /recommend <region_id> to receive listings with yield above 8%"
    )


async def recommend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /recommend <region_id>")
        return

    try:
        region_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Region id must be an integer")
        return

    try:
        sale_offers_raw = fetch_offers(region_id, "sale")
        rent_offers_raw = fetch_offers(region_id, "rent")
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
