import pandas as pd

"""
#TODO:
- Implement a mechanism using some public API to retrieve print names and daily closing values for assets.
- Improve logging by replacing print statements with appropriate logging functions.
- Enhance the "currency" property to support changes and ensure that changing the currency property affects the values inside the portfolio.
- Use Plotly to plot both Portfolio and PortfolioManager instances.

#FIXME:
- Refactor the class architecture for better organization and maintainability.
- Write docstrings.
- Unit test everything with pytest.
- Address certain scenarios during rebalancing:
    In the "no_sell" scenario, ensure that all assets in the portfolio are present in allocation.csv, while allowing assets in allocation.csv that are not in the portfolio.
    In the "sell" scenario, fix the ".join()" operation in the build_working_dataframe function to avoid discarding rows that are not present in either of the two files.
- Modify the rebalancing process to return the product name instead of the ISIN (or both).
"""


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

    def __str__(self):
        return self.summary.to_string()
    
    def __repr__(self):
        return f'Portfolio(currency={self.currency}, total_value={self.total_value})'
    
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

    @property
    def summary(self) -> pd.DataFrame:
        df = self._pf.drop(['Amount', 'Closing', 'Local value'], axis=1)
        df['Current Percentage'] = (df['Current Value'] / self.total_value * 100).apply(
            lambda x: round(x, 2)
        )

        df = df.join(self._al)
        df['Expected Value'] = (
            self.total_value / 100 * df['Expected Percentage']
        ).round(2)

        return df[
            [
                'Product',
                'Current Value',
                'Expected Value',
                'Current Percentage',
                'Expected Percentage',
            ]
        ]

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
