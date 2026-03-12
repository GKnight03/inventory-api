import requests


def convert_usd_to_eur(usd_amount: float) -> float:
    """
    Uses a public exchange rate API to convert USD to EUR.
    """
    url = "https://api.exchangerate.host/convert"
    params = {
        "from": "USD",
        "to": "EUR",
        "amount": usd_amount
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    if "result" not in data or data["result"] is None:
        raise ValueError("Could not retrieve exchange rate conversion.")

    return round(float(data["result"]), 2)