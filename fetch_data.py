import requests
import time
from requests.exceptions import RequestException

def fetch_with_backoff(url, headers=None, max_retries=5, base_delay=1):
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except RequestException as e:
            wait_time = base_delay * (2 ** retries)  # exponential backoff
            print(f"Error fetching data: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            retries += 1
    
    raise Exception(f"Failed to fetch data after {max_retries} retries")

def fetch_coinbase_order_book():
    url = "https://api.exchange.coinbase.com/products/BTC-USD/book?level=2"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'YourAppName/1.0'
    }
    response = fetch_with_backoff(url, headers=headers)
    order_book = response.json()
    
    bids = [{'price': float(price), 'quantity': float(quantity), 'exchange': 'coinbase'} for price, quantity, _ in order_book.get('bids', [])]
    asks = [{'price': float(price), 'quantity': float(quantity), 'exchange': 'coinbase'} for price, quantity, _ in order_book.get('asks', [])]
    
    return bids, asks

def fetch_gemini_order_book():
    url = "https://api.gemini.com/v1/book/btcusd?limit_bids=0&limit_asks=0"
    response = fetch_with_backoff(url)
    order_book = response.json()
    
    bids = [{'price': float(order['price']), 'quantity': float(order['amount']), 'exchange': 'gemini'} for order in order_book.get('bids', [])]
    asks = [{'price': float(order['price']), 'quantity': float(order['amount']), 'exchange': 'gemini'} for order in order_book.get('asks', [])]
    
    return bids, asks

def fetch_kraken_order_book():
    url = 'https://api.kraken.com/0/public/Depth?pair=XBTUSD'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
    response = fetch_with_backoff(url, headers=headers)
    order_book = response.json()
    
    bids = [{'price': float(price), 'quantity': float(quantity), 'exchange': 'kraken'}
            for price, quantity, _ in order_book['result']['XXBTZUSD']['bids']]
    asks = [{'price': float(price), 'quantity': float(quantity), 'exchange': 'kraken'}
            for price, quantity, _ in order_book['result']['XXBTZUSD']['asks']]
    
    return bids, asks
