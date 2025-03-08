# Copyright 2021 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from single_period import SinglePeriod

def optimize_portfolio(stocks=['AAPL', 'MSFT', 'AAL', 'WMT'], budget=1000000000, bin_size=None, 
                       gamma=None, alpha=[0.005], file_path='', 
                       baseline='^GSPC', max_risk=0.0, min_return=0.0, dates=[], 
                       model_type='CQM', rebalance=False, params="{}", verbose=False, 
                       num=0, t_cost=0.00):
    """
    Optimize a stock portfolio based on the provided parameters.

    :param stocks: List of stock symbols to include in the portfolio.
    :param budget: Total budget for the portfolio.
    :param bin_size: Maximum number of intervals for each stock (DQM-only).
    :param gamma: Penalty coefficient for budget constraint (DQM-only).
    :param alpha: Risk aversion coefficient.
    :param file_path: Path to the CSV file containing stock data.
    :param baseline: Baseline stock for comparison in multi-period optimization.
    :param max_risk: Upper bound on risk/variance (CQM-only).
    :param min_return: Lower bound on the returns (CQM-only).
    :param dates: Start and end date for querying stock data.
    :param model_type: Model type ('CQM' or 'DQM').
    :param rebalance: Whether to perform a multi-period rebalancing optimization.
    :param params: Additional sampler arguments.
    :param verbose: Enable verbose output.
    :param num: Number of stocks to randomly generate (requires dates).
    :param t_cost: Transaction cost as a percentage of transaction value.
    """

    if ((max_risk or min_return) and model_type != 'CQM'):
        raise Exception("The bound options require a CQM.")
        
    if ((gamma or bin_size) and model_type != 'DQM'):
        raise Exception("The option gamma or bin-size requires a DQM.")

    if (num and not dates):
        raise Exception("User must provide dates with option 'num'.") 

    if (t_cost and model_type != 'CQM'):
        raise Exception("The transaction cost option requires a CQM. "\
                        "Set t_cost=0 for DQM.")

    print(f"\nSingle period portfolio optimization run...")
    
    my_portfolio = SinglePeriod(stocks=stocks, budget=budget,
                                bin_size=bin_size, gamma=gamma, 
                                file_path=file_path, dates=dates, 
                                model_type=model_type, alpha=alpha, 
                                verbose=verbose, sampler_args=params,
                                t_cost=t_cost)
    
    return my_portfolio.run(min_return=None, max_risk=None, num=num)['stocksratios']

if __name__ == '__main__':
    # Example of calling the function
    print(optimize_portfolio(stocks=['MSFT', 'CAT', 'GILD', 'ECL', 'DLR', 'EFX', 'TTWO', 'ARE', 'DPZ', 'FFIV'], alpha=1))