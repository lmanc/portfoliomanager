import pandas as pd

from portfolio import Portfolio


class PortfolioManager:
    def __init__(self, portfolio: Portfolio):
        self._portfolio = portfolio

    def rebalance_sell(self) -> pd.DataFrame:
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
        df = self._portfolio.summary
        mask = (df['Expected Percentage'] == 0) & (df['Current Value'] != 0)

        if mask.any():
            error_message = (
                "While performing a no-sell rebalance, you can't set an"
                "Expected Percentage of 0% in your desired allocation for an"
                "asset that you currently own. The following assets are"
                "currently owned but their Expected Percentage is 0%:\n\n"
                f"{df[mask][['Product', 'Current Value', 'Expected Percentage']]}"
                "\n\nPlease adjust your target allocations and try again."
            )

            raise ValueError(error_message)

        max_isin = (
            df['Current Percentage'] / df['Expected Percentage']
        ).idxmax()

        df['Expected Value'] = df['Expected Percentage'] * (
            df.loc[max_isin]['Current Value']
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
