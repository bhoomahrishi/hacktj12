import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def analyze_portfolio(stock_investments, market_index, start_date, end_date):
    # Fetch historical data for stocks and the market index
    data = {stock: yf.download(stock, start=start_date, end=end_date) for stock in stock_investments.keys()}
    data[market_index] = yf.download(market_index, start=start_date, end=end_date)
    
    # Calculate the number of shares owned for each stock
    shares_owned = {}
    total_investment = sum(stock_investments.values())
    initial_market_price = data[market_index]['Open'].iloc[0]  # Price on the first trading day
    market_shares_owned = total_investment / initial_market_price

    for stock, investment in stock_investments.items():
        initial_price = data[stock]['Open'].iloc[0]  # Price on the first trading day
        shares_owned[stock] = investment / initial_price

    # Calculate daily portfolio value
    portfolio_value = pd.DataFrame(index=data[next(iter(stock_investments))].index)
    portfolio_value['Value'] = 0

    for stock in stock_investments.keys():
        stock_close = data[stock]['Close'].reindex(portfolio_value.index).fillna(0)  # Align index and fill missing values
        portfolio_value['Value'] += stock_close * shares_owned[stock]

    # Calculate daily market index value
    market_value = pd.DataFrame(index=data[market_index].index)
    market_value['Value'] = data[market_index]['Close'] * market_shares_owned

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(portfolio_value.index, portfolio_value['Value'], label='Portfolio Value')
    plt.plot(market_value.index, market_value['Value'], label='Market Index Value', linestyle='--')

    # Formatting the date axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))  # Month abbreviations
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Ensure each month is marked
    plt.gcf().autofmt_xdate()  # Auto-format to improve readability

    plt.title('Portfolio Value vs. Market Index Over Time')
    plt.xlabel('Month')
    plt.ylabel('Total Value in $')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Print the final values
    final_portfolio_value = portfolio_value['Value'].iloc[-1]
    final_market_value = market_value['Value'].iloc[-1]
    print(f'Final Portfolio Value on {end_date}: ${final_portfolio_value:.2f}')
    print(f'Final Market Index Value on {end_date}: ${final_market_value:.2f}')

if __name__ == '__main__':
    # Example usage
    stocks_and_investments_classical = {
        'MSFT': 0.0, 'CAT': 0.056019351802939106, 'GILD': 0.21302907153275075, 
        'ECL': 8.452770271197089e-17, 'DLR': 0.10472507700521203, 'EFX': 0.14965344625794894, 
        'TTWO': 0.08468199574469494, 'ARE': 0.0, 'DPZ': 0.24894483135237788, 
        'FFIV': 0.1429462263040763
    }
    market_index = '^GSPC'
    start_date = '2022-01-01'
    end_date = '2022-12-31'
    analyze_portfolio(stocks_and_investments_classical, market_index, start_date, end_date)