[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# 🚀 Roadmap
- Implement a mechanism using a public API to retrieve print names and daily closing values for assets 🐝
- Enhance the `currency` property to support changes and ensure that changing it affects the values inside the portfolio 💱
- Use Plotly Dash for data visualization 📊

# 🛠️ Improvements
- Consider if it's worth using abstract classes and methods, e.g., `Portfolio` should probably be an abstract class; similar consideration should be given to all the various methods that raise `NotImplementedError` 🤔
- Set up proper GitHub Actions 🦑
- Improve logging by replacing print statements in `except` blocks with appropriate logging functions 📝

# 🕹️ Usage
The default usage is as follows:

```python
from degiroportfolio import DegiroPortfolio
from portfolio_manager import PortfolioManager

pf = DegiroPortfolio()
pm = PortfolioManager(pf)
```

`DegiroPortfolio()` takes two optional arguments: `assets_file` and `allocation_file`. By default, these are set to `assets.csv` and `allocation.csv`, respectively, which must be in the same directory as the project.

## Sell Rebalance

To perform a sell rebalance, run:

```python
from degiroportfolio import DegiroPortfolio
from portfolio_manager import PortfolioManager

pf = DegiroPortfolio()
pm = PortfolioManager(pf)

pm.rebalance_sell()
```

## No-sell Rebalance

To perform a no-sell rebalance, run:

```python
from degiroportfolio import DegiroPortfolio
from portfolio_manager import PortfolioManager

pf = DegiroPortfolio()
pm = PortfolioManager(pf)

pm.rebalance_no_sell()
```

## `assets_file` and `allocation_file` Required Format

`assets_file` must have the second column filled with ISINs, which will then be used as the `Index` of the assets `DataFrame` inside the`Portfolio` object. `allocation_file` must have two columns with the ISINs and the desired percentages. Any subclass of `Portfolio` should be implemented accordingly. For examples of how they should be formatted, see the `assets.csv` and `allocations.csv` in `tests/csv`.
