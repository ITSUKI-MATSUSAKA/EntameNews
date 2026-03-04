import urllib.request
import json
import urllib.error

symbols = {
    '日経平均': '^N225',
    '日経平均先物': 'NIY=F',
    'NYダウ': '^DJI',
    'NASDAQ': '^IXIC',
    'S&P500': '^GSPC',
    'TOPIX': '^TOPX',
    'USD/JPY': 'JPY=X',
    'Bitcoin': 'BTC-JPY'
}

for name, sym in symbols.items():
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym)}?interval=1d"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            meta = data['chart']['result'][0]['meta']
            price = meta.get('regularMarketPrice')
            prev = meta.get('chartPreviousClose')
            if price and prev:
                change = price - prev
                change_pct = (change / prev) * 100
                print(f"{name}: {price} ({change_pct:.2f}%)")
            else:
                print(f"{name}: No data")
    except Exception as e:
        print(f"{name} ({sym}): Error {e}")
