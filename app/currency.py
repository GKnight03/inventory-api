import requests
import logging

def convert_usd_to_eur(usd_amount: float) -> float:
    url = "https://api.exchangerate.host/convert"
    params = {
        "from": "USD",
        "to": "EUR",
        "amount": usd_amount
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "result" not in data or data["result"] is None:
            logging.error(f"Exchange API response missing result: {data}")
            raise ValueError("Could not retrieve exchange rate conversion.")
        return round(float(data["result"]), 2)
    except Exception as e:
        logging.error(f"Currency conversion failed: {e}")
        raise ValueError(f"Currency conversion failed: {e}")