# TODO
- Implement a mechanism using some public API to retrieve print names and daily closing values for assets.
- Improve logging by replacing print statements in `except` blocks with appropriate logging functions.
- Enhance the `currency` property to support changes and ensure that changing it affects the values inside the portfolio.
- Use Plotly to plot both `Portfolio` and `PortfolioManager` instances.

# FIXME
- Document that `ISIN` is a mandatory column for all `Portfolio`'s child classes.
- Document that `allocation.csv` must contain exactly two columns and be formatted like the examples in `tests/csv`.
- At this point, `Portfolio` should probably be an abstract class.
- All the imports need a proper refactor. 💀
- Write `requirements.txt`.
- Set up proper GitHub Actions.
- Use `ruff` for linting.

# Usage
The default usage is as follows:

```python
from degiroportfolio import DegiroPortfolio
from portfolio_manager import PortfolioManager

pf = DegiroPortfolio()
pm = PortfolioManager(pf)
```

`DegiroPortfolio` takes two optional keyword arguments: `assets_file` and `allocation_file`, which by default are set at `assets.csv` and `allocation.csv`, that must be in the same directory of the project.

## Sell Rebalance

In order to perform a sell rebalance, run:

```python
from degiroportfolio import DegiroPortfolio
from portfolio_manager import PortfolioManager

pf = DegiroPortfolio()
pm = PortfolioManager(pf)

pm.rebalance_sell()
```

## No-sell Rebalance

In order to perform a no-sell rebalance, run:
```python
from degiroportfolio import DegiroPortfolio
from portfolio_manager import PortfolioManager

pf = DegiroPortfolio()
pm = PortfolioManager(pf)

pm.rebalance_no_sell()
```
