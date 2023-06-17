import pandas as pd

# TODO:
# API to get daily closing value
# Class architecture -
# portfolio : init with portfolio.csv and assets.csv - takes care of validation and creating the portfolio object. Must have a currencty attr
# portfolio manager: return views which are some columns of the portfolio and the movments - does not touch the portfolio object, but only read it.
# print(e) should be logged instead
# currency should support changes and a change in the "currency" property should impact the values inside the portfolio

# FIXME:
# currency validator
# when rebalancing there are certain scenarios to be considered:
# - no_sell: all assets in the portfolio must be in assets.csv.
#            assets.csv can have assets that are not in the portfolio.
#
# - sell: join must not discard rows that are not present in one of
#         the two files since operations on all the assets has to be done.
#         Fix `join` in `build_working_dataframe`.
# rebalancing should return the product name instead of the ISIN


class Portfolio:
    def __init__(
        self,
        portfolio_file: str = 'portfolio.csv',
        allocation_file: str = 'allocation.csv',
        currency: str = 'EUR',
    ):
        self._pf = Portfolio._read_portfolio(portfolio_file)
        self._al = Portfolio._read_allocation(allocation_file)
        self._currency = currency

    @property
    def currency(self) -> str:
        return self._currency

    @currency.setter
    def currency(self, currency: str) -> None:
        self._currency = currency

    @property
    def total_value(self) -> float:
        try:
            return self._pf['Current Value'].sum()
        except KeyError as e:
            print(e)
            raise KeyError(e) from None

    @staticmethod
    def _read_file(file: str):
        try:
            return pd.read_csv(file)
        except FileNotFoundError as e:
            print(e)
            raise FileNotFoundError(e) from None

    @staticmethod
    def _read_portfolio(portfolio_file: str) -> pd.DataFrame:
        df = Portfolio._read_file(portfolio_file)
        Portfolio._clean_portfolio(df)

        return df

    @staticmethod
    def _clean_portfolio(df: pd.DataFrame) -> None:
        try:
            df.columns = [
                'Product',
                'ISIN',
                'Amount',
                'Closing',
                'Local value',
                'Current Value',
            ]
        except ValueError as e:
            print(e)
            raise ValueError(e) from None

        if df['Current Value'].dtype == 'object':
            try:
                df['Current Value'] = (
                    df['Current Value']
                    .apply(lambda x: x.replace(',', '.'))
                    .astype('float')
                )
            except (KeyError, AttributeError, ValueError) as e:
                print(e)
                raise type(e)(e) from None

        try:
            df.dropna(subset=['ISIN'], inplace=True)
        except KeyError as e:
            print(e)
            raise KeyError(e) from None

        df.set_index('ISIN', inplace=True)

    @staticmethod
    def _read_allocation(allocation_file: str) -> pd.DataFrame:
        df = Portfolio._read_file(allocation_file)

        try:
            if (s := df['Expected Percentage'].sum()) != 100:
                raise ValueError(
                    f'The total sum of percentages in the "Percentage" column is {s}%, not 100.0%'
                )
        except KeyError as e:
            print(e)
            raise KeyError(e) from None

        df.set_index('ISIN', inplace=True)

        return df
