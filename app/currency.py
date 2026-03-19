import requests

def convert_usd_to_eur(usd_amount: float) -> float:
    url = "https://api.frankfurter.dev/v1/latest"
    params = {
        "amount": usd_amount,
        "from": "USD",
        "to": "EUR"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "rates" not in data or "EUR" not in data["rates"]:
        raise Exception(f"Unexpected API response: {data}")

    return round(data["rates"]["EUR"], 2)