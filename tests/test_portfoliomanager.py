import pytest
from conftest import (
    MockPortfolio,
    portfolios_conv,
    rebalances_no_sell,
    rebalances_sell,
    summaries,
    summaries_passing_no_sell,
)
from portfolio import Portfolio
from portfoliomanager import PortfolioManager


@pytest.mark.parametrize(
    'read_pickles',
    zip(rebalances_sell, summaries, portfolios_conv, strict=True),
    indirect=True,
)
def test_rebalance_sell(read_pickles, mocker):
    df_expected_from_pickle, summary, portfolio = read_pickles
    mocker.patch.object(
        Portfolio,
        'summary',
        new_callable=mocker.PropertyMock,
        return_value=summary,
    )

    mocker.patch.object(Portfolio, '_read_portfolio', return_value=portfolio)

    mock_portfolio = MockPortfolio()
    pm = PortfolioManager(mock_portfolio)

    assert pm.rebalance_sell().equals(df_expected_from_pickle)


@pytest.mark.parametrize(
    'read_pickles', zip(summaries, strict=True), indirect=True
)
def test_rebalance_no_sell_raise_ValueError(read_pickles, mocker):
    (summary_file,) = read_pickles

    mocker.patch.object(
        Portfolio,
        'summary',
        new_callable=mocker.PropertyMock,
        return_value=summary_file,
    )
    mock_portfolio = MockPortfolio()
    pm = PortfolioManager(mock_portfolio)

    with pytest.raises(
        ValueError, match=r'While performing a no-sell rebalance, .*'
    ):
        pm.rebalance_no_sell()


@pytest.mark.parametrize(
    'read_pickles',
    zip(rebalances_no_sell, summaries_passing_no_sell, strict=True),
    indirect=True,
)
def test_rebalance_no_sell(read_pickles, mocker):
    df_expected_from_pickle, summary_file = read_pickles

    mocker.patch.object(
        Portfolio,
        'summary',
        new_callable=mocker.PropertyMock,
        return_value=summary_file,
    )
    mock_portfolio = MockPortfolio()
    pm = PortfolioManager(mock_portfolio)

    assert pm.rebalance_no_sell().equals(df_expected_from_pickle)
