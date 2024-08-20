import requests

def fetch_coinbase_order_book():
    url = "https://api.exchange.coinbase.com/products/BTC-USD/book?level=2"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'YourAppName/1.0'
    }
    response = requests.get(url, headers=headers)
    order_book = response.json()
    
    bids = [{'price': float(price), 'quantity': float(quantity), 'exchange': 'coinbase'} for price, quantity, _ in order_book.get('bids', [])]
    asks = [{'price': float(price), 'quantity': float(quantity), 'exchange': 'coinbase'} for price, quantity, _ in order_book.get('asks', [])]
    
    return bids, asks

def fetch_gemini_order_book():
    url = "https://api.gemini.com/v1/book/btcusd?limit_bids=0&limit_asks=0"
    response = requests.get(url)
    order_book = response.json()
    
    bids = [{'price': float(order['price']), 'quantity': float(order['amount']), 'exchange': 'gemini'} for order in order_book.get('bids', [])]
    asks = [{'price': float(order['price']), 'quantity': float(order['amount']), 'exchange': 'gemini'} for order in order_book.get('asks', [])]
    
    return bids, asks

def fetch_kraken_order_book():
    url = 'https://api.kraken.com/0/public/Depth?pair=XBTUSD'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    
    order_book = response.json()
    
    bids = [{'price': float(price), 'quantity': float(quantity), 'exchange': 'kraken'}
            for price, quantity, _ in order_book['result']['XXBTZUSD']['bids']]
    asks = [{'price': float(price), 'quantity': float(quantity), 'exchange': 'kraken'}
            for price, quantity, _ in order_book['result']['XXBTZUSD']['asks']]
    
    return bids, asks
