import sys
from pathlib import Path

project_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(project_dir))


import pandas as pd
import pytest

from portfolio import Portfolio

currencies = ('EUR', 'GBP')
portfolios_csv = ('portfolio_EUR.csv', 'portfolio_GBP.csv')
allocations_csv = ('allocation_EUR.csv', 'allocation_GBP.csv')

portfolios_plain = ('portfolio_EUR.pickle', 'portfolio_GBP.pickle')
allocations_plain = ('allocation_EUR.pickle', 'allocation_GBP.pickle')

portfolios_columns = (
    'portfolio_EUR_columns.pickle',
    'portfolio_GBP_columns.pickle',
)
portfolios_dropna = (
    'portfolio_EUR_dropna.pickle',
    'portfolio_GBP_dropna.pickle',
)
portfolios_idx = ('portfolio_EUR_idx.pickle', 'portfolio_GBP_idx.pickle')

portfolios_conv = ('portfolio_EUR_conv.pickle', 'portfolio_GBP_conv.pickle')
allocations_idx = ('allocation_EUR_idx.pickle', 'allocation_GBP_idx.pickle')
summaries = ('summary_EUR.pickle', 'summary_GBP.pickle')
rebalances_sell = ('rebalance_sell_EUR.pickle', 'rebalance_sell_GBP.pickle')
summaries_passing_no_sell = (
    'summary_EUR_passing_no_sell.pickle',
    'summary_GBP_passing_no_sell.pickle',
)
rebalances_no_sell = (
    'rebalance_no_sell_EUR.pickle',
    'rebalance_no_sell_GBP.pickle',
)


class MockPortfolio(Portfolio):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def _clean_portfolio(df: pd.DataFrame) -> pd.DataFrame:
        pass


@pytest.fixture
def raw_csv_portfolio(request):
    return project_dir / 'tests' / 'csv' / request.param


@pytest.fixture
def raw_csv_allocation(request):
    return project_dir / 'tests' / 'csv' / request.param


@pytest.fixture
def read_pickles(request):
    return (
        pd.read_pickle(project_dir / 'tests' / 'pickles' / path)
        for path in request.param
    )
