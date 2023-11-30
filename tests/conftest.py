from pathlib import Path

import pandas as pd
import pytest
from portfolio import Portfolio

csv_dir = Path(__file__).parent / 'csv'
pickles_dir = Path(__file__).parent / 'pickles'

currencies = ('EUR', 'GBP')
portfolios_csv = ('assets_EUR.csv', 'assets_GBP.csv')
allocations_csv = ('allocation_EUR.csv', 'allocation_GBP.csv')

portfolios_plain = ('assets_EUR.pickle', 'assets_GBP.pickle')
allocations_plain = ('allocation_EUR.pickle', 'allocation_GBP.pickle')

portfolios_columns = (
    'assets_EUR_columns.pickle',
    'assets_GBP_columns.pickle',
)
portfolios_dropna = (
    'assets_EUR_dropna.pickle',
    'assets_GBP_dropna.pickle',
)
portfolios_idx = ('assets_EUR_idx.pickle', 'assets_GBP_idx.pickle')

portfolios_conv = ('assets_EUR_conv.pickle', 'assets_GBP_conv.pickle')
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
    def __init__(
        self,
        assets_file=csv_dir / 'assets_EUR.csv',
        allocation_file=csv_dir / 'allocation_EUR.csv',
        currency='EUR',
    ):
        super().__init__(assets_file, allocation_file, currency)

    @staticmethod
    def _clean_portfolio(df: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame()


@pytest.fixture
def raw_csv_portfolio(request):
    return csv_dir / request.param


@pytest.fixture
def raw_csv_allocation(request):
    return csv_dir / request.param


@pytest.fixture
def read_pickles(request):
    return (pd.read_pickle(pickles_dir / path) for path in request.param)
