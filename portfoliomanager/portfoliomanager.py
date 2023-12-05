import pandas as pd

from portfoliomanager.portfolio import Portfolio


class PortfolioManager:
    """A class to manage a financial portfolio.

    Attributes:
        _portfolio (Portfolio): The portfolio to manage.
    """

    def __init__(self, portfolio: Portfolio):
        """__init__ method.

        Constructs all the necessary attributes for the portfolio
        manager object.

        Args:
            portfolio (Portfolio): The portfolio to manage.
        """
        self._portfolio = portfolio

    def rebalance_sell(self) -> pd.DataFrame:
        """Rebalance with sell operations.

        Calculates the required changes to rebalance the portfolio
        with selling allowed.

        Returns:
            DataFrame: A DataFrame showing the current and expected
                values, percentages, and movements.
        """
        summary = self._portfolio.summary
        summary['Expected Value'] = (
            self._portfolio.total_value / 100 * summary['Expected Percentage']
        ).round(2)

        summary['Movement'] = summary['Expected Value'] - summary['Current Value']
        return summary[
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
        """Rebalance without sell operations.

        Calculates the required changes to rebalance the portfolio
        without selling. If an asset is owned but its expected
        percentage is 0, an error is raised.

        Raises:
            ValueError: If an asset is owned but its expected percentage
                is 0.

        Returns:
            DataFrame: A DataFrame showing the current and expected
                values, percentages, and movements.
        """
        summary = self._portfolio.summary
        mask = (summary['Expected Percentage'] == 0) & (summary['Current Value'] != 0)

        if mask.any():
            msg = (
                "While performing a no-sell rebalance, you can't set an "
                "Expected Percentage of 0% in your desired allocation for an "
                "asset that you currently own. The following assets are "
                "currently owned but their Expected Percentage is 0%:\n\n"
                f"{summary[mask][['Product', 'Current Value', 'Expected Percentage']]}"
                "\n\nPlease adjust your desired assets allocation and try again."
            )

            raise ValueError(msg)

        max_isin = (summary['Current Percentage'] / summary['Expected Percentage']).idxmax()

        summary['Expected Value'] = (
            summary['Expected Percentage']
            * summary.loc[max_isin]['Current Value']
            / summary.loc[max_isin]['Expected Percentage']
        ).round(2)

        summary['Movement'] = summary['Expected Value'] - summary['Current Value']

        return summary[
            [
                'Product',
                'Current Value',
                'Expected Value',
                'Current Percentage',
                'Expected Percentage',
                'Movement',
            ]
        ]
