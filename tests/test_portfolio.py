import sys
from pathlib import Path

import pandas as pd
import pytest

project_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(project_dir))

from portfolio import Portfolio

portfolios_csv = ['portfolio_EUR.csv', 'portfolio_GBP.csv']
allocations_csv = ['allocation_EUR.csv', 'allocation_GBP.csv']

portfolios_plane = ['portfolio_EUR.pickle', 'portfolio_GBP.pickle']
allocations_plane = ['allocation_EUR.pickle', 'allocation_GBP.pickle']

portfolios_columns = ['portfolio_EUR_columns.pickle', 'portfolio_GBP_columns.pickle']
portfolios_dropna = ['portfolio_EUR_dropna.pickle', 'portfolio_GBP_dropna.pickle']
portfolios_idx = ['portfolio_EUR_idx.pickle', 'portfolio_GBP_idx.pickle']
portfolios_conv = ['portfolio_EUR_conv.pickle', 'portfolio_GBP_conv.pickle']

@pytest.fixture
def raw_csv_portfolio(request):
    return project_dir / 'tests' / 'csv' / request.param

@pytest.fixture
def raw_csv_allocation(request):
    return project_dir / 'tests' / 'csv' / request.param

@pytest.fixture
def df_expected_from_pickle(request):
    return pd.read_pickle(project_dir / 'tests' / 'pickles' / request.param)


@pytest.fixture
def df_working_from_pickle(request):
    return pd.read_pickle(project_dir / 'tests' / 'pickles' / request.param)


@pytest.mark.parametrize(
    'df_expected_from_pickle, raw_csv_portfolio',
    zip(portfolios_plane, portfolios_csv),
    indirect=True,
)
def test_read_file_portfolio(df_expected_from_pickle, raw_csv_portfolio):
    df = Portfolio._read_file(raw_csv_portfolio)
    assert df.equals(df_expected_from_pickle)


@pytest.mark.parametrize(
    'df_expected_from_pickle, raw_csv_allocation',
    zip(allocations_plane, allocations_csv),
    indirect=True,
)
def test_read_file_allocation(df_expected_from_pickle, raw_csv_allocation):
    df = Portfolio._read_file(raw_csv_allocation)
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

@pytest.mark.parametrize('df_expected_from_pickle', portfolios_dropna, indirect=True)
def test_dropna_isin_untouched(df_expected_from_pickle):
    assert df_expected_from_pickle.equals(Portfolio._dropna_isin(df_expected_from_pickle))


@pytest.mark.parametrize('df_expected_from_pickle, df_working_from_pickle', zip(portfolios_idx, portfolios_dropna), indirect=True)
def test_set_index_isin(df_expected_from_pickle, df_working_from_pickle):
    assert df_expected_from_pickle.equals(Portfolio._set_index_isin(df_working_from_pickle))

@pytest.mark.parametrize('df_working_from_pickle', portfolios_idx, indirect=True)
def test_convert_str_columns_to_float_raise_NotImplementedError(df_working_from_pickle):
    with pytest.raises(NotImplementedError):
        Portfolio._convert_str_columns_to_float(df_working_from_pickle)

@pytest.mark.parametrize('df_expected_from_pickle', allocations_plane, indirect=True)
def test_validate_allocation_percentage_sum(df_expected_from_pickle):
    assert Portfolio._validate_allocation_percentage_sum(df_expected_from_pickle)


@pytest.mark.parametrize('df_expected_from_pickle', allocations_plane, indirect=True)
def test_validate_allocation_percentage_sum_wrong(df_expected_from_pickle):
    df_expected_from_pickle['Expected Percentage'] = 0
    assert not Portfolio._validate_allocation_percentage_sum(df_expected_from_pickle)
