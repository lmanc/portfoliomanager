import pandas as pd

from portfolio import Portfolio


class PortfolioManager:
    def __init__(self, portfolio: Portfolio):
        self._portfolio = portfolio

    # def rebalance_sell(self) -> pd.DataFrame:
    #     movement = (
    #         self._portfolio.summary['Expected Value']
    #         - self._portfolio.summary['Current Value']
    #     ).round(2)
    #     return pd.DataFrame(
    #         {
    #             'Product': self._portfolio.summary['Product'],
    #             'Movment': movement,
    #         }
    #     )

    # def rebalance_no_sell(self) -> pd.DataFrame:
    #     summary = self._portfolio.summary
    #     max_isin = (
    #         summary['Current Percentage'] / summary['Expected Percentage']
    #     ).idxmax()

    #     movement = (
    #         summary['Expected Percentage']
    #         * (
    #             summary.loc[max_isin]['Current Value']
    #             / summary.loc[max_isin]['Expected Percentage']
    #         )
    #     ).round(2) - summary['Current Value']

    #     return pd.DataFrame(
    #         {'Product': summary['Product'], 'Movement': movement}
    #     )

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
