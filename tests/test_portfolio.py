import sys
from pathlib import Path

import pandas as pd
import pytest

project_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(project_dir))

from portfolio import Portfolio

portfolios_csv = ['portfolio_EUR.csv', 'portfolio_GBP.csv']
portfolios_plane = ['portfolio_EUR.pickle', 'portfolio_GBP.pickle']
portfolios_dropna = ['portfolio_EUR_dropna.pickle', 'portfolio_GBP_dropna.pickle']
portfolios_columns = ['portfolio_EUR_columns.pickle', 'portfolio_GBP_columns.pickle']


@pytest.fixture
def df_expected_from_pickle(request):
    return pd.read_pickle(project_dir / 'tests' / 'pickles' / request.param)


@pytest.fixture
def df_working_from_pickle(request):
    return pd.read_pickle(project_dir / 'tests' / 'pickles' / request.param)


@pytest.fixture
def raw_csv_portfolio(request):
    return project_dir / 'tests' / 'csv' / request.param


@pytest.mark.parametrize(
    'df_expected_from_pickle, raw_csv_portfolio',
    zip(portfolios_plane, portfolios_csv),
    indirect=True,
)
def test_read_file(df_expected_from_pickle, raw_csv_portfolio):
    df = Portfolio._read_file(raw_csv_portfolio)

    assert df.equals(df_expected_from_pickle)


def test_read_file_raise_FileNotFoundError():
    with pytest.raises(FileNotFoundError):
        Portfolio._read_file(project_dir / 'tests' / 'csv' / 'missing.csv')


@pytest.mark.parametrize('df_working_from_pickle', portfolios_plane, indirect=True)
def test_replace_columns_raise_NotImplementedError(df_working_from_pickle):
    with pytest.raises(NotImplementedError):
        Portfolio._replace_columns(df_working_from_pickle)


@pytest.mark.parametrize(
    'df_expected_from_pickle, df_working_from_pickle',
    zip(portfolios_dropna, portfolios_columns),
    indirect=True,
)
def test_dropna_isin(df_expected_from_pickle, df_working_from_pickle):
    assert df_expected_from_pickle.equals(
        Portfolio._dropna_isin(df_working_from_pickle)
    )
