
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
        raise ValueError("Недостаточно свечей")

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
        return 100.0 if avg_gain > 0 else 50.0

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


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

    bullish = (
        prices[-1] > ema21[-1]
        and ema9[-1] > ema21[-1]
        and macd_line[-1] > signal_line[-1]
        and 50 < rsi < 70
    )

    bearish = (
        prices[-1] < ema21[-1]
        and ema9[-1] < ema21[-1]
        and macd_line[-1] < signal_line[-1]
        and 30 < rsi < 50
    )

    if bullish:
        direction = "ВОСХОДЯЩАЯ ТЕНДЕНЦИЯ 🟢"
        explanation = "Большинство показателей указывают вверх."

    elif bearish:
        direction = "НИСХОДЯЩАЯ ТЕНДЕНЦИЯ 🔴"
        explanation = "Большинство показателей указывают вниз."

    else:
        direction = "НЕТ ЧЁТКОГО СИГНАЛА ⚪"
        explanation = "Показатели не дают согласованной картины."

    return (
        f"⏱ Таймфрейм: {interval}\n"
        f"💶 Цена: {prices[-1]:.5f}\n"
        f"📊 RSI(14): {rsi:.2f}\n"
        f"📈 EMA(9): {ema9[-1]:.5f}\n"
        f"📈 EMA(21): {ema21[-1]:.5f}\n"
        f"MACD: {macd_line[-1]:.6f}\n"
        f"Signal: {signal_line[-1]:.6f}\n\n"
        f"🔎 Оценка: {direction}\n"
        f"💬 Объяснение: {explanation}"
    )


def analyze_eurusd():
    results = []

    for interval in ("1m", "5m"):
        try:
            results.append(analyze_interval(interval))
        except Exception:
            results.append(
                f"⏱ {interval}: не удалось получить данные."
            )

    return (
        "💶 SIDOROV SIGNALS AI\n"
        "📊 УЧЕБНЫЙ АНАЛИЗ EUR/USD\n\n"
        + "\n\n".join(results)
        + "\n\n⚠️ Это техническая оценка, "
          "а не прогноз или гарантия движения цены."
    )
