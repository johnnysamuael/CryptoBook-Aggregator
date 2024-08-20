import argparse
from process_data import calculate_price_for_quantity, combine_order_books

def calculate_trade(amount, action, exchanges):
    combined_bids, combined_asks = combine_order_books(exchanges)
    
    if action == 'buy':
        price, orders = calculate_price_for_quantity(combined_asks, amount)
    elif action == 'sell':
        price, orders = calculate_price_for_quantity(combined_bids, amount)
    else:
        raise ValueError("Action must be 'buy' or 'sell'")

    return price, orders

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('amount', type=float)
    parser.add_argument('action', choices=['buy', 'sell'])
    parser.add_argument('--exchanges', nargs='+', choices=['coinbase', 'gemini', 'kraken'], default=['coinbase', 'gemini', 'kraken'])
    
    args = parser.parse_args()
    
    amount = args.amount
    action = args.action
    exchanges = args.exchanges
    
    price, orders = calculate_trade(amount, action, exchanges)
    
    print("\n")
    print(f"Price to {action} {amount} BTC: ${price}")
    print("\n")

    print(f"Orders used to {action} {amount} BTC:")
    for order in orders:
        print(f"Price: ${order['price']}, Quantity: {order['quantity']}, Exchange: {order['exchange']}")

if __name__ == "__main__":
    main()
