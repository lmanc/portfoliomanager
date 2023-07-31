# TODO
- Implement a mechanism using some public API to retrieve print names and daily closing values for assets.
- Improve logging by replacing print statements in `except` blocks with appropriate logging functions.
- Enhance the `currency` property to support changes and ensure that changing it affects the values inside the portfolio.
- Use Plotly to plot both `Portfolio` and `PortfolioManager` instances.
- Create `Portfolio`'s child class `DegiroPortfolio`.

# FIXME
- Write docstrings.
- Document that `ISIN` is a mandatory column for all `Portfolio`'s child classes.
- Document that `allocation.csv` must contain exactly two columns and be formatted like the examples in `tests/csv`.
- At this point, `Portfolio` should probably be an abstract class
- All the imports need a proper refactor
- Write `requirements.txt`
- Set up proper GitHub Actions
- Use `ruff` for linting
