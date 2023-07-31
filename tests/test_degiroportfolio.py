import sys
from pathlib import Path

import pandas as pd
import pytest

from degiroportfolio import DegiroPortfolio
from portfolio import Portfolio

project_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(project_dir))


from conftest import (
    allocations_csv,
    allocations_idx,
    allocations_plain,
    currencies,
    portfolios_columns,
    portfolios_conv,
    portfolios_csv,
    portfolios_dropna,
    portfolios_idx,
    portfolios_plain,
    summaries,
)


@pytest.mark.parametrize(
    'read_pickles', zip(portfolios_plain, portfolios_columns), indirect=True
)
def test_replace_columns(read_pickles):
    df_working_from_pickle, df_expected_from_pickle = read_pickles

    assert df_expected_from_pickle.equals(
        DegiroPortfolio._replace_columns(df_working_from_pickle)
    )


@pytest.mark.parametrize('read_pickles', zip(portfolios_plain), indirect=True)
def test_replace_columns_raise_ValueError(read_pickles):
    (df_working_from_pickle,) = read_pickles
    df_working_from_pickle.drop(
        df_working_from_pickle.columns[0], axis=1, inplace=True
    )

    with pytest.raises(ValueError):
        DegiroPortfolio._replace_columns(df_working_from_pickle)


@pytest.mark.parametrize(
    'read_pickles', zip(portfolios_columns, portfolios_conv), indirect=True
)
def test_convert_str_columns_to_float(read_pickles):
    df_working_from_pickle, df_expected_from_pickle = read_pickles
    df_working_from_pickle = DegiroPortfolio._dropna_isin(
        df_working_from_pickle
    )
    df_working_from_pickle = DegiroPortfolio._set_index_isin(
        df_working_from_pickle
    )

    assert df_expected_from_pickle.equals(
        DegiroPortfolio._convert_str_columns_to_float(df_working_from_pickle)
    )


@pytest.mark.parametrize(
    'read_pickles', zip(portfolios_columns[0:1]), indirect=True
)
def test_convert_str_columns_to_float(read_pickles):
    (df_working_from_pickle,) = read_pickles
    df_working_from_pickle = DegiroPortfolio._dropna_isin(
        df_working_from_pickle
    )

    index = df_working_from_pickle.index[0]
    df_working_from_pickle.loc[index, 'Closing'] = 'wrong'

    with pytest.raises(ValueError):
        DegiroPortfolio._convert_str_columns_to_float(df_working_from_pickle)


@pytest.mark.parametrize(
    'read_pickles', zip(portfolios_plain, portfolios_conv), indirect=True
)
def test_clean_portfolio(read_pickles, mocker):
    df_working_from_pickle, df_expected_from_pickle = read_pickles

    assert df_expected_from_pickle.equals(
        DegiroPortfolio._clean_portfolio(df_working_from_pickle)
    )
