import requests

def analyze_eurusd():
    url = "https://api.frankfurter.app/latest?from=EUR&to=USD"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    rate = response.json()["rates"]["USD"]

    return (
        "💶 EUR/USD\n"
        f"Последний доступный справочный курс: {rate}\n\n"
        "Это не торговый сигнал."
    )
