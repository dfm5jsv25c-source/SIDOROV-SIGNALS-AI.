
import requests

def get_candles(interval):
    url = "https://biquote.io/api/EURUSD/ohlc"
    response = requests.get(
        url,
        params={"interval": interval, "limit": 200},
        timeout=15
    )
    response.raise_for_status()

    bars = response.json()["bars"]
    bars = [b for b in bars if not b.get("isOpen", False)]
    bars.sort(key=lambda b: b["openTime"])

    if len(bars) < 40:
        raise ValueError("Недостаточно закрытых свечей")

    return [float(b["close"]) for b in bars]


def ema(values, period):
    result = [values[0]]
    multiplier = 2 / (period + 1)

    for price in values[1:]:
        result.append(
            price * multiplier +
            result[-1] * (1 - multiplier)
        )

    return result


def calculate_rsi(values, period=14):
    changes = [
        values[i] - values[i - 1]
        for i in range(1, len(values))
    ]

    recent = changes[-period:]
    gains = [max(x, 0) for x in recent]
    losses = [max(-x, 0) for x in recent]

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    if avg_loss == 0:
        return 100.0

    return 100 - (100 / (1 + avg_gain / avg_loss))


def analyze_interval(interval):
    prices = get_candles(interval)

    ema9 = ema(prices, 9)
    ema21 = ema(prices, 21)

    macd_line = [
        a - b for a, b in zip(
            ema(prices, 12),
            ema(prices, 26)
        )
    ]

    signal_line = ema(macd_line, 9)

    rsi = calculate_rsi(prices)

    direction = "НЕЙТРАЛЬНО"

    if (
        prices[-1] > ema21[-1]
        and macd_line[-1] > signal_line[-1]
        and 50 < rsi < 70
    ):
        direction = "ВОСХОДЯЩЕЕ ДВИЖЕНИЕ"

    elif (
        prices[-1] < ema21[-1]
        and macd_line[-1] < signal_line[-1]
        and 30 < rsi < 50
    ):
        direction = "НИСХОДЯЩЕЕ ДВИЖЕНИЕ"

    return (
        f"⏱ Таймфрейм: {interval}\n"
        f"💶 Цена: {prices[-1]:.5f}\n"
        f"📊 RSI(14): {rsi:.2f}\n"
        f"📈 EMA(9): {ema9[-1]:.5f}\n"
        f"📈 EMA(21): {ema21[-1]:.5f}\n"
        f"MACD: {macd_line[-1]:.6f}\n"
        f"Signal: {signal_line[-1]:.6f}\n"
        f"🔎 Оценка: {direction}"
    )


def analyze_eurusd():
    results = []

    for interval in ("1m", "5m"):
        try:
            results.append(analyze_interval(interval))
        except Exception as error:
            results.append(
                f"⏱ {interval}: ошибка получения данных"
            )

    return (
        "💶 EUR/USD — УЧЕБНЫЙ АНАЛИЗ\n\n"
        + "\n\n".join(results)
        + "\n\n⚠️ Это техническая оценка, "
          "не прогноз и не торговая рекомендация."
    )

