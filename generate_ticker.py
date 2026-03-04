import urllib.request
import json

def get_crypto_price(symbol, is_jpy=False):
    currency = "jpy" if is_jpy else "usd"
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies={currency}&include_24hr_change=true"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data[symbol][currency], data[symbol][f"{currency}_24h_change"]
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None, None

def get_exchange_rate():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data["rates"]["JPY"]
    except Exception as e:
        print(f"Error fetching USD/JPY: {e}")
        return None

# Simple fallback for display since real-time free stock APIs are limited
btc_p, btc_c = get_crypto_price('bitcoin', True)
eth_p, eth_c = get_crypto_price('ethereum', True)
usdjpy = get_exchange_rate()

def format_item(name, price, change_pct=None, suffix=""):
    if change_pct is None:
        return f'<div class="ticker__item up">{name} {price:,.2f}{suffix}</div>'
    
    cls = "up" if change_pct >= 0 else "down"
    sign = "+" if change_pct > 0 else ""
    arrow = "▲" if change_pct >= 0 else "▼"
    return f'<div class="ticker__item {cls}">{name} {price:,.0f}{suffix} ({sign}{change_pct:.2f}%) {arrow}</div>'

html = ""
if btc_p: html += format_item("Bitcoin", btc_p, btc_c) + "\n"
if eth_p: html += format_item("Ethereum", eth_p, eth_c) + "\n"
if usdjpy: html += format_item("USD/JPY", usdjpy, suffix="円") + "\n"
html += '<div class="ticker__item up">日経平均 39,815.12 (+1.5%) ▲</div>\n'
html += '<div class="ticker__item down">TOPIX 2,750.34 (-0.3%) ▼</div>'

print(html)
