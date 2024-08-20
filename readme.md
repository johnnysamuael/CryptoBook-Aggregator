# Order Book Aggregator

This Python project aggregates order books from multiple cryptocurrency exchanges (CoinBase Pro, Gemini, and Kraken) to calculate the price to buy or sell a specified amount of Bitcoin (BTC). The program allows you to select the amount, action (buy or sell), and the exchanges to include in the calculation.

## Table of Contents

- [Features](#features)
- [Components](#components)
- [Approach](#approach)
- [Installation](#installation)
- [Usage](#usage)

## Features

- Fetches real-time order books from CoinBase Pro, Gemini, and Kraken exchanges.
- Aggregates bids and asks from multiple exchanges.
- Calculates the cost to buy or sell a specified amount of BTC.
- Supports exponential backoff to handle rate limits.
- Command-line interface for specifying trade details.

## Components

### 1. `main.py`
The main entry point of the application, which handles command-line arguments, invokes the order book aggregation, and prints the final price and orders used for the transaction.

### 2. `fetch_data.py`
Contains functions for fetching order books from the supported exchanges (CoinBase Pro, Gemini, and Kraken). Each function uses exponential backoff to handle network errors and rate limiting.

### 3. `process_data.py`
Handles the processing of fetched order books:
- `combine_order_books(exchanges)`: Merges order books from the specified exchanges, sorting bids in descending order and asks in ascending order.
- `calculate_price_for_quantity(order_book, quantity_needed)`: Calculates the total cost and identifies which orders were used to buy or sell the specified amount of BTC.

## Approach

1. **Fetching Order Books**: Order books from each exchange are fetched using REST APIs. Each order book contains bids (buy orders) and asks (sell orders).
2. **Exponential Backoff**: To ensure robustness against rate limiting and network issues, an exponential backoff strategy is employed in all network requests.
3. **Data Normalization**: The fetched data from different exchanges are normalized into a common format for easy aggregation.
4. **Order Book Aggregation**: The order books from the selected exchanges are combined into a single structure, with bids sorted in descending order and asks sorted in ascending order.
5. **Price Calculation**: The aggregated order book is used to calculate the total cost to buy or sell the specified amount of BTC by "taking" liquidity from the market.

## Installation

1. **Install latest python (Python 3.7+)
2. **Install requirements using `pip3 install -r requirements.txt`

## Usage

To run the program, use the command line to specify the trade amount, action, and exchanges:

```bash
python main.py <amount> <action> --exchanges <exchange1> <exchange2> ...
```

### Examples:

1. **Buy 10 BTC from all supported exchanges**:
    ```bash
    python main.py 10 buy --exchanges coinbase gemini kraken
    ```

2. **Sell 5 BTC using only CoinBase Pro and Gemini**:
    ```bash
    python main.py 5 sell --exchanges coinbase gemini
    ```

The output will display the total price and the detailed orders used to fulfill the transaction.
