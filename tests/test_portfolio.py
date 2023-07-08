import sys
from pathlib import Path

import pandas as pd
import pytest

from portfolio import Portfolio

project_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(project_dir))


currencies = ('EUR', 'GBP')
portfolios_csv = ('portfolio_EUR.csv', 'portfolio_GBP.csv')
allocations_csv = ('allocation_EUR.csv', 'allocation_GBP.csv')

portfolios_plain = ('portfolio_EUR.pickle', 'portfolio_GBP.pickle')
allocations_plain = ('allocation_EUR.pickle', 'allocation_GBP.pickle')

portfolios_columns = ('portfolio_EUR_columns.pickle', 'portfolio_GBP_columns.pickle')
portfolios_dropna = ('portfolio_EUR_dropna.pickle', 'portfolio_GBP_dropna.pickle')
portfolios_idx = ('portfolio_EUR_idx.pickle', 'portfolio_GBP_idx.pickle')

# Not to be used yet - we need the Degiro conversion function defined.
portfolios_conv = ('portfolio_EUR_conv.pickle', 'portfolio_GBP_conv.pickle')

allocations_idx = ('allocation_EUR_idx.pickle', 'allocation_GBP_idx.pickle')


class MockPortfolio(Portfolio):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def _clean_portfolio(df: pd.DataFrame) -> pd.DataFrame:
        pass


@pytest.mark.parametrize(
    'raw_csv_portfolio, raw_csv_allocation',
    zip(portfolios_csv, allocations_csv),
    indirect=True,
)
def test_portfolio_init(raw_csv_portfolio, raw_csv_allocation, mocker):
    read_portfolio_spy = mocker.spy(MockPortfolio, '_read_portfolio')
    allocation_portfolio_spy = mocker.spy(MockPortfolio, '_read_allocation')

    mock_portfolio = MockPortfolio(
        portfolio_file=raw_csv_portfolio, allocation_file=raw_csv_allocation
    )

    assert read_portfolio_spy.call_count == 1
    assert allocation_portfolio_spy.call_count == 1
    assert mock_portfolio.currency == 'EUR'


@pytest.mark.parametrize('currency', currencies)
def test_currency(currency):
    mock_portfolio = MockPortfolio(currency=currency)
    assert mock_portfolio.currency == currency

@pytest.mark.parametrize('read_pickles', [ *zip(portfolios_conv, allocations_idx) ], indirect=True)
def test_summary(read_pickles, mocker):
    portfolio, allocation = read_pickles
    mocker.patch.object(Portfolio, '_read_portfolio', return_value=portfolio)
    mocker.patch.object(Portfolio, '_read_allocation', return_value=allocation)

    mock_portfolio = MockPortfolio()

    mock_portfolio.summary 
    

@pytest.mark.parametrize(
    'df_expected_from_pickle, raw_csv_portfolio',
    zip(portfolios_plain, portfolios_csv),
    indirect=True,
)
def test_read_file_portfolio(df_expected_from_pickle, raw_csv_portfolio):
    df = Portfolio._read_file(raw_csv_portfolio)
    assert df.equals(df_expected_from_pickle)


@pytest.mark.parametrize(
    'df_expected_from_pickle, raw_csv_allocation',
    zip(allocations_plain, allocations_csv),
    indirect=True,
)
def test_read_file_allocation(df_expected_from_pickle, raw_csv_allocation):
    df = Portfolio._read_file(raw_csv_allocation)
    assert df.equals(df_expected_from_pickle)


def test_read_file_raise_FileNotFoundError():
    with pytest.raises(FileNotFoundError):
        Portfolio._read_file(project_dir / 'tests' / 'csv' / 'missing.csv')


@pytest.mark.parametrize('df_working_from_pickle', portfolios_plain, indirect=True)
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
    assert df_expected_from_pickle.equals(
        Portfolio._dropna_isin(df_expected_from_pickle)
    )


@pytest.mark.parametrize(
    'df_expected_from_pickle, df_working_from_pickle',
    zip(portfolios_idx, portfolios_dropna),
    indirect=True,
)
def test_set_index_isin(df_expected_from_pickle, df_working_from_pickle):
    assert df_expected_from_pickle.equals(
        Portfolio._set_index_isin(df_working_from_pickle)
    )


@pytest.mark.parametrize('df_working_from_pickle', portfolios_idx, indirect=True)
def test_convert_str_columns_to_float_raise_NotImplementedError(df_working_from_pickle):
    with pytest.raises(NotImplementedError):
        Portfolio._convert_str_columns_to_float(df_working_from_pickle)


@pytest.mark.parametrize('df_working_from_pickle', portfolios_plain, indirect=True)
def test_clean_portfolio_raise_NotImplementedError(df_working_from_pickle):
    with pytest.raises(NotImplementedError):
        Portfolio._clean_portfolio(df_working_from_pickle)


@pytest.mark.parametrize('raw_csv_portfolio', portfolios_csv, indirect=True)
def test_read_portfolio(raw_csv_portfolio, mocker):
    spy_read_file = mocker.spy(Portfolio, '_read_file')
    spy_clean_portfolio = mocker.spy(MockPortfolio, '_clean_portfolio')

    MockPortfolio._read_portfolio(raw_csv_portfolio)

    assert spy_read_file.call_count == 1
    assert spy_clean_portfolio.call_count == 1


@pytest.mark.parametrize('df_expected_from_pickle', allocations_plain, indirect=True)
def test_validate_allocation_percentage_sum(df_expected_from_pickle):
    assert Portfolio._validate_allocation_percentage_sum(df_expected_from_pickle)


@pytest.mark.parametrize('df_expected_from_pickle', allocations_plain, indirect=True)
def test_validate_allocation_percentage_sum_wrong(df_expected_from_pickle):
    df_expected_from_pickle['Expected Percentage'] = 0
    assert not Portfolio._validate_allocation_percentage_sum(df_expected_from_pickle)


@pytest.mark.parametrize('raw_csv_allocation', allocations_csv, indirect=True)
def test_read_allocation_raise_ValueError(raw_csv_allocation, mocker):
    mocker.patch.object(
        Portfolio, '_validate_allocation_percentage_sum', return_value=False
    )

    with pytest.raises(ValueError):
        Portfolio._read_allocation(raw_csv_allocation)


@pytest.mark.parametrize(
    'df_expected_from_pickle, raw_csv_allocation',
    zip(allocations_idx, allocations_csv),
    indirect=True,
)
def test_read_allocation(df_expected_from_pickle, raw_csv_allocation):
    assert df_expected_from_pickle.equals(
        Portfolio._read_allocation(raw_csv_allocation)
    )
