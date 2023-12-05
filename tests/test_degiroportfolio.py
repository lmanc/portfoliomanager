import pytest

from portfoliomanager.degiroportfolio import DegiroPortfolio
from tests.conftest import (
    portfolios_columns,
    portfolios_conv,
    portfolios_plain,
)


@pytest.mark.parametrize(
    'read_pickles',
    zip(portfolios_plain, portfolios_columns, strict=True),
    indirect=True,
)
def test_replace_columns(read_pickles):
    df_working_from_pickle, df_expected_from_pickle = read_pickles

    assert df_expected_from_pickle.equals(DegiroPortfolio._replace_columns(df_working_from_pickle))


@pytest.mark.parametrize('read_pickles', zip(portfolios_plain, strict=True), indirect=True)
def test_replace_columns_raise_ValueError(read_pickles):
    (df_working_from_pickle,) = read_pickles
    df_working_from_pickle = df_working_from_pickle.drop(df_working_from_pickle.columns[0], axis=1)

    with pytest.raises(ValueError, match=r'Column mismatch: .*'):
        DegiroPortfolio._replace_columns(df_working_from_pickle)


@pytest.mark.parametrize(
    'read_pickles',
    zip(portfolios_columns, portfolios_conv, strict=True),
    indirect=True,
)
def test_convert_str_columns_to_float(read_pickles):
    df_working_from_pickle, df_expected_from_pickle = read_pickles
    df_working_from_pickle = DegiroPortfolio._dropna_isin(df_working_from_pickle)
    df_working_from_pickle = DegiroPortfolio._set_index_isin(df_working_from_pickle)

    assert df_expected_from_pickle.equals(
        DegiroPortfolio._convert_str_columns_to_float(df_working_from_pickle)
    )


@pytest.mark.parametrize('read_pickles', zip(portfolios_columns[0:1], strict=True), indirect=True)
def test_convert_str_columns_to_float_raise_ValueError(read_pickles):
    (df_working_from_pickle,) = read_pickles
    df_working_from_pickle = DegiroPortfolio._dropna_isin(df_working_from_pickle)

    index = df_working_from_pickle.index[0]
    df_working_from_pickle.loc[index, 'Closing'] = 'wrong'

    with pytest.raises(ValueError, match=r'Failed to convert column .*'):
        DegiroPortfolio._convert_str_columns_to_float(df_working_from_pickle)


@pytest.mark.parametrize(
    'read_pickles',
    zip(portfolios_plain, portfolios_conv, strict=True),
    indirect=True,
)
def test_clean_portfolio(read_pickles):
    df_working_from_pickle, df_expected_from_pickle = read_pickles

    assert df_expected_from_pickle.equals(DegiroPortfolio._clean_portfolio(df_working_from_pickle))
