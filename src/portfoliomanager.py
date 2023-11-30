import pandas as pd
from portfolio import Portfolio


class PortfolioManager:
    """
    A class to manage a financial portfolio.

    Attributes:
        _portfolio (Portfolio): The portfolio to manage.
    """

    def __init__(self, portfolio: Portfolio):
        """
        Constructs all the necessary attributes for the portfolio manager object.

        Args:
            portfolio (Portfolio): The portfolio to manage.
        """
        self._portfolio = portfolio

    def rebalance_sell(self) -> pd.DataFrame:
        """
        Calculates the required changes to rebalance the portfolio with selling allowed.

        Returns:
            DataFrame: A DataFrame showing the current and expected values, percentages, and movements.
        """
        df = self._portfolio.summary
        df['Expected Value'] = (
            self._portfolio.total_value / 100 * df['Expected Percentage']
        ).round(2)

        df['Movement'] = df['Expected Value'] - df['Current Value']
        return df[
            [
                'Product',
                'Current Value',
                'Expected Value',
                'Current Percentage',
                'Expected Percentage',
                'Movement',
            ]
        ]

    def rebalance_no_sell(self) -> pd.DataFrame:
        """
        Calculates the required changes to rebalance the portfolio without selling.

        If an asset is owned but its expected percentage is 0, an error is raised.

        Raises:
            ValueError: If an asset is owned but its expected percentage is 0.

        Returns:
            DataFrame: A DataFrame showing the current and expected values, percentages, and movements.
        """
        df = self._portfolio.summary
        mask = (df['Expected Percentage'] == 0) & (df['Current Value'] != 0)

        if mask.any():
            error_message = (
                "While performing a no-sell rebalance, you can't set an "
                "Expected Percentage of 0% in your desired allocation for an "
                "asset that you currently own. The following assets are "
                "currently owned but their Expected Percentage is 0%:\n\n"
                f"{df[mask][['Product', 'Current Value', 'Expected Percentage']]}"
                "\n\nPlease adjust your desired assets allocation and try again."
            )

            raise ValueError(error_message)

        max_isin = (
            df['Current Percentage'] / df['Expected Percentage']
        ).idxmax()

        df['Expected Value'] = (
            df['Expected Percentage']
            * df.loc[max_isin]['Current Value']
            / df.loc[max_isin]['Expected Percentage']
        ).round(2)

        df['Movement'] = df['Expected Value'] - df['Current Value']

        return df[
            [
                'Product',
                'Current Value',
                'Expected Value',
                'Current Percentage',
                'Expected Percentage',
                'Movement',
            ]
        ]
