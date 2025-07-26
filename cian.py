CIAN_SEARCH_URL = "https://api.cian.ru/search-offers/v2/search-offers-desktop/"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
}


def fetch_offers(region_id: int, deal_type: str) -> list:
    """Fetch offers from CIAN.

    Parameters
    ----------
    region_id : int
        Numerical region identifier used by CIAN.
    deal_type : str
        Either ``"sale"`` or ``"rent"``.

    Returns
    -------
    list
        List of raw offer dictionaries returned by the CIAN API.
    """
    import requests  # imported here to allow running tests without the package

    query = {
        "jsonQuery": {
            "_type": "flats",
            "engine_version": {
                "type": "term",
                "value": 2
            },
            "region": {
                "type": "terms",
                "value": [region_id]
            },
            "deal_type": {
                "type": "term",
                "value": deal_type
            }
        }
    }
    resp = requests.post(CIAN_SEARCH_URL, json=query, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data.get("offersSerialized", [])


def extract_prices(offers: list) -> list:
    """Extract price and address from offers."""
    results = []
    for item in offers:
        terms = item.get("bargainTerms", {})
        price = terms.get("price")
        address = item.get("geo", {}).get("userInput")
        if price:
            results.append({"price": price, "address": address})
    return results


def compute_yield(sale_price: float, monthly_rent: float) -> float:
    """Calculate annual rental yield."""
    if not sale_price or not monthly_rent:
        return 0.0
    return (monthly_rent * 12) / sale_price
