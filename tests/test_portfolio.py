from sys import path

import pandas as pd
import pytest

path.append('..')

from portfolio import Portfolio

@pytest.mark.parametrize('file', ['portfolio_EUR.csv', 'portfolio_GBP.csv'])
def test_read_file_well_formed(file):
    df = Portfolio._read_file(file)
    expected_df = pd.read_csv(file)

    assert isinstance(df, pd.DataFrame)
    assert df.equals(expected_df)

def test_read_file_raise_FileNotFoundError():
    with pytest.raises(FileNotFoundError):
        df = Portfolio._read_file('portfolio.csv')
