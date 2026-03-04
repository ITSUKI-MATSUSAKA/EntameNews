import urllib.request
import json
url = "https://query1.finance.yahoo.com/v8/finance/chart/1306.T?interval=1d"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read().decode())
        meta = data['chart']['result'][0]['meta']
        price = meta.get('regularMarketPrice')
        prev = meta.get('chartPreviousClose')
        print(f"TOPIX ETF: {price} ({((price-prev)/prev)*100:.2f}%)")
except Exception as e:
    print(f"Error {e}")
