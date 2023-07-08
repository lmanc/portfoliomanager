import pandas as pd

from portfolio import Portfolio


class PortfolioManager:
    def __init__(self, portfolio: Portfolio):
        self._portfolio = portfolio

    def rebalancing_sell(self) -> pd.DataFrame:
        movement = (
            self._portfolio.summary['Expected Value']
            - self._portfolio.summary['Current Value']
        ).round(2)
        return pd.DataFrame(
            {'Product': self._portfolio.summary['Product'], 'Movment': movement}
        )

    def rebalancing_no_sell(self) -> pd.DataFrame:
        summary = self._portfolio.summary
        max_isin = (
            summary['Current Percentage'] / summary['Expected Percentage']
        ).idxmax()

        movement = (
            summary['Expected Percentage']
            * (
                summary.loc[max_isin]['Current Value']
                / summary.loc[max_isin]['Expected Percentage']
            )
        ).round(2) - summary['Current Value']

        return pd.DataFrame({'Product': summary['Product'], 'Movement': movement})
