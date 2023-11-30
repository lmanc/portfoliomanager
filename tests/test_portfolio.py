import pytest
from conftest import (
    MockPortfolio,
    allocations_csv,
    allocations_idx,
    allocations_plain,
    csv_dir,
    currencies,
    portfolios_columns,
    portfolios_conv,
    portfolios_csv,
    portfolios_dropna,
    portfolios_idx,
    portfolios_plain,
    summaries,
)
from portfolio import Portfolio


@pytest.mark.parametrize(
    'raw_csv_portfolio, raw_csv_allocation',
    zip(portfolios_csv, allocations_csv, strict=True),
    indirect=True,
)
def test_portfolio_init(raw_csv_portfolio, raw_csv_allocation, mocker):
    read_portfolio_spy = mocker.spy(MockPortfolio, '_read_portfolio')
    allocation_portfolio_spy = mocker.spy(MockPortfolio, '_read_allocation')

    mock_portfolio = MockPortfolio(
        assets_file=raw_csv_portfolio, allocation_file=raw_csv_allocation
    )

    assert read_portfolio_spy.call_count == 1
    assert allocation_portfolio_spy.call_count == 1
    assert mock_portfolio.currency == 'EUR'


@pytest.mark.parametrize('currency', currencies)
def test_currency(currency):
    mock_portfolio = MockPortfolio(currency=currency)
    assert mock_portfolio.currency == currency


@pytest.mark.parametrize(
    'read_pickles', zip(portfolios_conv, strict=True), indirect=True
)
def test_total_value(read_pickles, mocker):
    (df_expected_from_pickle,) = read_pickles
    mocker.patch.object(
        Portfolio, '_read_portfolio', return_value=df_expected_from_pickle
    )

    mock_portfolio = MockPortfolio()

    assert (
        mock_portfolio.total_value
        == df_expected_from_pickle['Current Value'].sum()
    )


@pytest.mark.parametrize(
    'read_pickles',
    zip(portfolios_conv, allocations_idx, summaries, strict=True),
    indirect=True,
)
def test_summary(read_pickles, mocker):
    portfolio, allocation, df_expected_from_pickle = read_pickles

    portfolio.rename(index={portfolio.index[0]: 'US0003692039'}, inplace=True)

    mocker.patch.object(Portfolio, '_read_portfolio', return_value=portfolio)
    mocker.patch.object(Portfolio, '_read_allocation', return_value=allocation)

    mock_portfolio = MockPortfolio()

    assert mock_portfolio.summary.equals(df_expected_from_pickle)


@pytest.mark.parametrize(
    'read_pickles, raw_csv_portfolio',
    zip(zip(portfolios_plain, strict=True), portfolios_csv, strict=True),
    indirect=True,
)
def test_read_file_portfolio(read_pickles, raw_csv_portfolio):
    df = Portfolio._read_file(raw_csv_portfolio)
    (df_expected_from_pickle,) = read_pickles
    assert df.equals(df_expected_from_pickle)


@pytest.mark.parametrize(
    'read_pickles, raw_csv_allocation',
    zip(zip(allocations_plain, strict=True), allocations_csv, strict=True),
    indirect=True,
)
def test_read_file_allocation(read_pickles, raw_csv_allocation):
    df = Portfolio._read_file(raw_csv_allocation)
    (df_expected_from_pickle,) = read_pickles
    assert df.equals(df_expected_from_pickle)


def test_read_file_raise_FileNotFoundError():
    with pytest.raises(FileNotFoundError):
        Portfolio._read_file(csv_dir / 'missing.csv')


@pytest.mark.parametrize(
    'read_pickles', zip(portfolios_plain, strict=True), indirect=True
)
def test_replace_columns_raise_NotImplementedError(read_pickles):
    (df_working_from_pickle,) = read_pickles
    with pytest.raises(NotImplementedError):
        Portfolio._replace_columns(df_working_from_pickle)


@pytest.mark.parametrize(
    'read_pickles',
    zip(portfolios_dropna, portfolios_columns, strict=True),
    indirect=True,
)
def test_dropna_isin(read_pickles):
    df_expected_from_pickle, df_working_from_pickle = read_pickles
    assert df_expected_from_pickle.equals(
        Portfolio._dropna_isin(df_working_from_pickle)
    )


@pytest.mark.parametrize(
    'read_pickles', zip(portfolios_dropna, strict=True), indirect=True
)
def test_dropna_isin_untouched(read_pickles):
    (df_expected_from_pickle,) = read_pickles
    assert df_expected_from_pickle.equals(
        Portfolio._dropna_isin(df_expected_from_pickle)
    )


@pytest.mark.parametrize(
    'read_pickles',
    zip(portfolios_idx, portfolios_dropna, strict=True),
    indirect=True,
)
def test_set_index_isin(read_pickles):
    df_expected_from_pickle, df_working_from_pickle = read_pickles
    assert df_expected_from_pickle.equals(
        Portfolio._set_index_isin(df_working_from_pickle)
    )


@pytest.mark.parametrize(
    'read_pickles', zip(portfolios_idx, strict=True), indirect=True
)
def test_convert_str_columns_to_float_raise_NotImplementedError(
    read_pickles,
):
    (df_working_from_pickle,) = read_pickles
    with pytest.raises(NotImplementedError):
        Portfolio._convert_str_columns_to_float(df_working_from_pickle)


@pytest.mark.parametrize(
    'read_pickles', zip(portfolios_plain, strict=True), indirect=True
)
def test_clean_portfolio_raise_NotImplementedError(read_pickles):
    (df_working_from_pickle,) = read_pickles
    with pytest.raises(NotImplementedError):
        Portfolio._clean_portfolio(df_working_from_pickle)


@pytest.mark.parametrize('raw_csv_portfolio', portfolios_csv, indirect=True)
def test_read_portfolio(raw_csv_portfolio, mocker):
    spy_read_file = mocker.spy(Portfolio, '_read_file')
    spy_clean_portfolio = mocker.spy(MockPortfolio, '_clean_portfolio')

    MockPortfolio._read_portfolio(raw_csv_portfolio)

    assert spy_read_file.call_count == 1
    assert spy_clean_portfolio.call_count == 1


@pytest.mark.parametrize(
    'read_pickles', zip(allocations_plain, strict=True), indirect=True
)
def test_validate_allocation_percentage_sum(read_pickles):
    (df_expected_from_pickle,) = read_pickles
    assert Portfolio._validate_allocation_percentage_sum(
        df_expected_from_pickle
    )


@pytest.mark.parametrize(
    'read_pickles', zip(allocations_plain, strict=True), indirect=True
)
def test_validate_allocation_percentage_sum_wrong(read_pickles):
    (df_expected_from_pickle,) = read_pickles
    df_expected_from_pickle['Expected Percentage'] = 0
    assert not Portfolio._validate_allocation_percentage_sum(
        df_expected_from_pickle
    )


@pytest.mark.parametrize('raw_csv_allocation', allocations_csv, indirect=True)
def test_read_allocation_raise_ValueError(raw_csv_allocation, mocker):
    mocker.patch.object(
        Portfolio, '_validate_allocation_percentage_sum', return_value=False
    )

    with pytest.raises(ValueError):
        Portfolio._read_allocation(raw_csv_allocation)


@pytest.mark.parametrize(
    'read_pickles, raw_csv_allocation',
    zip(zip(allocations_idx, strict=True), allocations_csv, strict=True),
    indirect=True,
)
def test_read_allocation(read_pickles, raw_csv_allocation):
    (df_expected_from_pickle,) = read_pickles
    assert df_expected_from_pickle.equals(
        Portfolio._read_allocation(raw_csv_allocation)
    )
