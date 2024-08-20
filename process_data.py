import pandas as pd


def combine_order_books(exchanges):
    from fetch_data import (fetch_coinbase_order_book, fetch_gemini_order_book,
                            fetch_kraken_order_book)

    fetch_funcs = {
        'coinbase': fetch_coinbase_order_book,
        'gemini': fetch_gemini_order_book,
        'kraken': fetch_kraken_order_book
    }

    all_bids, all_asks = [], []

    for exchange in exchanges:
        if exchange in fetch_funcs:
            bids, asks = fetch_funcs[exchange]()
            all_bids.extend(bids)
            all_asks.extend(asks)

    combined_bids = pd.DataFrame(all_bids).sort_values(by='price', ascending=False)
    combined_asks = pd.DataFrame(all_asks).sort_values(by='price', ascending=True)

    return combined_bids, combined_asks

def calculate_price_for_quantity(order_book, quantity_needed):
    total_quantity = 0
    total_cost = 0
    used_orders = []

    for _, order in order_book.iterrows():
        price = order['price']
        quantity = order['quantity']
        exchange = order['exchange']

        if total_quantity + quantity >= quantity_needed:
            remaining_quantity = quantity_needed - total_quantity
            total_cost += remaining_quantity * price
            used_orders.append({
                'price': price,
                'quantity': remaining_quantity,
                'exchange': exchange
            })
            break
        else:
            total_cost += quantity * price
            total_quantity += quantity
            used_orders.append({
                'price': price,
                'quantity': quantity,
                'exchange': exchange
            })

    return total_cost, used_orders
