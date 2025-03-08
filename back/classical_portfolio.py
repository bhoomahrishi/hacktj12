
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.optimize import minimize

def get_optimal_portfolio_weights(tickers, user_risk_factor):
    # Calculating desired volatility based on user risk factor
    desired_volatility = .05 + (.3 - .05) * (user_risk_factor - 1) / 9

    adj_close_df = pd.DataFrame()
    for ticker in tickers:
        data = yf.download(ticker, start="2020-01-01", end="2021-12-31")['Adj Close']
        adj_close_df[ticker] = data
    
    log_returns = np.log(adj_close_df / adj_close_df.shift(1))
    log_returns = log_returns.dropna()
    cov_matrix = log_returns.cov() * 252

    def standard_deviation(weights, cov_matrix):
        variance = weights.T @ cov_matrix @ weights
        return np.sqrt(variance)

    def expected_return(weights, log_returns):
        return np.sum(log_returns.mean()*weights)*252

    def sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate, desired_volatility, risk_aversion=50):
        port_return = expected_return(weights, log_returns)
        port_volatility = standard_deviation(weights, cov_matrix)
        # Penalty for deviation from desired volatility
        penalty = risk_aversion * (port_volatility - desired_volatility) ** 2
        return (port_return - risk_free_rate) / port_volatility - penalty

    risk_free_rate = .02

    def objective_function(weights, log_returns, cov_matrix, risk_free_rate, desired_volatility):
        return -sharpe_ratio(weights, log_returns, cov_matrix, risk_free_rate, desired_volatility)


    constraints = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}
    bounds = [(0, 0.5) for _ in range(len(tickers))]
    initial_weights = np.array([1/len(tickers)]*len(tickers))

    optimized_results = minimize(objective_function, initial_weights, args=(log_returns, cov_matrix, risk_free_rate, desired_volatility), method='SLSQP', constraints=constraints, bounds=bounds)
    optimal_weights = optimized_results.x


    return [dict(zip(tickers, optimal_weights)), expected_return(optimal_weights, log_returns), standard_deviation(optimal_weights, cov_matrix)]

if __name__ == '__main__':
    print(get_optimal_portfolio_weights(['MSFT', 'CAT', 'GILD', 'ECL', 'DLR', 'EFX', 'TTWO', 'ARE', 'DPZ', 'FFIV'], 1))