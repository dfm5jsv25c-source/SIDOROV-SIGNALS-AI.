
import requests
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD

def analyze_eurusd():
    url = "https://api.frankfurter.app/latest?from=EUR&to=USD"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    rate = response.json()["rates"]["USD"]

    return (
        f"💶 EUR/USD\n"
        f"Последний доступный курс: {rate}\n\n"
        f"Это справочный курс, не котировка для сделок."
    )

if __name__ == "__main__":
    print(analyze_eurusd())
