"""Helper functions for retrieving and processing CIAN offers."""

from cianparser import CianParser

MOSCOW_LOCATION = "Москва"


def fetch_offers(location: str, deal_type: str, price_to: int | None = None, pages: int = 1) -> list:
    """Fetch offers from CIAN using ``cianparser``.

    Parameters
    ----------
    location : str
        City name such as ``"Москва"``.
    deal_type : str
        Either ``"sale"`` or ``"rent"``.
    price_to : int | None, optional
        Maximum price filter for sale offers.
    pages : int
        How many pages to parse.

    Returns
    -------
    list
        List of offer dictionaries returned by cianparser.
    """

    parser = CianParser(location=location)
    settings = {"start_page": 1, "end_page": pages}
    if price_to and deal_type == "sale":
        settings["max_price"] = price_to

    dt = "rent_long" if deal_type == "rent" else deal_type
    return parser.get_flats(deal_type=dt, rooms="all", with_saving_csv=False, additional_settings=settings)


def extract_prices(offers: list, deal_type: str) -> list:
    """Extract price and address from offers returned by ``cianparser``."""
    results = []
    for item in offers:
        if deal_type == "sale":
            price = item.get("price")
        else:
            price = item.get("price_per_month")
        address_parts = [item.get("district"), item.get("street"), item.get("house_number")]
        address = ", ".join(part for part in address_parts if part)
        if price:
            results.append({"price": price, "address": address})
    return results


def compute_yield(sale_price: float, monthly_rent: float) -> float:
    """Calculate annual rental yield."""
    if not sale_price or not monthly_rent:
        return 0.0
    return (monthly_rent * 12) / sale_price
