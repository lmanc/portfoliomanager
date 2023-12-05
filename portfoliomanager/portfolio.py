import pandas as pd

FULL_PERCENTAGE = 100


class Portfolio:
    """A class to represent a financial portfolio.

    Attributes:
        _as (DataFrame): A DataFrame containing assets data.
        _al (DataFrame): A DataFrame containing allocation data.
        _currency (str): The currency of the portfolio.
    """

    def __init__(
        self,
        assets_file: str = 'assets.csv',
        allocation_file: str = 'allocation.csv',
        currency: str = 'EUR',
    ):
        """__init__ method.

        Constructs all the necessary attributes for the portfolio
        object.

        Args:
            assets_file (str): The file name of the assets csv.
                Defaults to 'assets.csv'.
            allocation_file (str): The file name of the allocation csv.
                Defaults to 'allocation.csv'.
            currency (str): The currency of the portfolio.
                Defaults to 'EUR'.
        """
        self._as = self.__class__._read_portfolio(assets_file)  # noqa: SLF001
        self._al = self.__class__._read_allocation(allocation_file)  # noqa: SLF001
        self._currency = currency

    @property
    def currency(self) -> str:
        """Returns the currency of the portfolio."""
        return self._currency

    @property
    def total_value(self) -> float:
        """Calculates and returns the total value of the portfolio."""
        return self._as['Current Value'].sum()

    @property
    def summary(self) -> pd.DataFrame:
        """Generates and returns a summary of the portfolio.

        The summary includes the product, current value, current
        percentage, and expected percentage.
        """
        summary = self._as.drop(['Amount', 'Closing', 'Local Value'], axis=1)
        summary = summary.merge(self._al, how='outer', left_index=True, right_index=True)
        summary = summary.fillna({'Current Value': 0, 'Expected Percentage': 0})
        summary['Current Percentage'] = (summary['Current Value'] / self.total_value * 100).apply(
            lambda x: round(x, 2)
        )

        return summary[
            [
                'Product',
                'Current Value',
                'Current Percentage',
                'Expected Percentage',
            ]
        ]

    @staticmethod
    def _read_file(file: str) -> pd.DataFrame:
        """Reads a csv file and returns a DataFrame.

        Args:
            file (str): The file name of the csv.

        Raises:
            FileNotFoundError: If the file does not exist.

        Returns:
            DataFrame: The DataFrame constructed from the csv file.
        """
        try:
            return pd.read_csv(file)
        except FileNotFoundError as e:
            print(e)
            raise FileNotFoundError(e) from None

    @staticmethod
    def _replace_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Method to be implemented.

        Placeholder for a method that replaces column names in a
        DataFrame.

        Raises:
            NotImplementedError: This method needs to be implemented
                in a subclass.
        """
        raise NotImplementedError

    @staticmethod
    def _dropna_isin(df: pd.DataFrame) -> pd.DataFrame:
        """Drops NaN values from the 'ISIN' column in a DataFrame.

        Args:
            df (DataFrame): The DataFrame to process.

        Returns:
            DataFrame: The processed DataFrame.
        """
        return df.dropna(subset=['ISIN'])

    @staticmethod
    def _set_index_isin(df: pd.DataFrame) -> pd.DataFrame:
        """Sets the 'ISIN' column as the index of a DataFrame.

        Args:
            df (DataFrame): The DataFrame to process.

        Returns:
            DataFrame: The processed DataFrame.
        """
        return df.set_index('ISIN')

    @staticmethod
    def _convert_str_columns_to_float(df: pd.DataFrame) -> pd.DataFrame:
        """Method to be implemented.

        Placeholder for a method that converts string columns to float
        in a DataFrame.

        Raises:
            NotImplementedError: This method needs to be implemented
                in a subclass.
        """
        raise NotImplementedError

    @staticmethod
    def _clean_portfolio(df: pd.DataFrame) -> pd.DataFrame:
        """Method to be implemented.

        Placeholder for a method that cleans a portfolio DataFrame.

        Raises:
            NotImplementedError: This method needs to be implemented
                in a subclass.
        """
        raise NotImplementedError

    @classmethod
    def _read_portfolio(cls, portfolio_file: str) -> pd.DataFrame:
        """Reads a portfolio file and cleans the resulting DataFrame.

        Args:
            portfolio_file (str): The file name of the portfolio csv.

        Returns:
            DataFrame: The cleaned portfolio DataFrame.
        """
        return cls._clean_portfolio(Portfolio._read_file(portfolio_file))

    @staticmethod
    def _validate_allocation_percentage_sum(allocation: pd.DataFrame) -> bool:
        """Validate 'Expected Percentage'.

        Validates that the sum of the 'Expected Percentage' column in a
        DataFrame is 100.

        Args:
            allocation (DataFrame): The DataFrame to validate.

        Returns:
            bool: True if the sum is 100, False otherwise.
        """
        return allocation['Expected Percentage'].sum() == FULL_PERCENTAGE

    @staticmethod
    def _read_allocation(allocation_file: str) -> pd.DataFrame:
        """Reads allocation file and validates the resulting DataFrame.

        Args:
            allocation_file (str): The file name of the allocation csv.

        Raises:
            ValueError: If the sum of the 'Expected Percentage'
                column is not 100.

        Returns:
            DataFrame: The validated allocation DataFrame.
        """
        allocation = Portfolio._read_file(allocation_file)

        if not Portfolio._validate_allocation_percentage_sum(allocation):
            msg = 'The total sum of percentages in the "Expected Percentage" column is not 100%'
            raise ValueError(msg)

        return Portfolio._set_index_isin(allocation)
