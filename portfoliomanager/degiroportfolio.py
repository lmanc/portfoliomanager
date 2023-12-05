import pandas as pd

from portfoliomanager.portfolio import Portfolio


class DegiroPortfolio(Portfolio):
    """A subclass of Portfolio that represents a Degiro portfolio."""

    @staticmethod
    def _replace_columns(assets: pd.DataFrame) -> pd.DataFrame:
        """Replaces the column names in a DataFrame.

        The columns are renamed to: 'Product', 'ISIN', 'Amount',
        'Closing', 'Local Value', 'Current Value'.

        Args:
            assets (DataFrame): The DataFrame to process.

        Raises:
            ValueError: If the DataFrame doesn't have the
                correct number of columns.

        Returns:
            DataFrame: The processed DataFrame.
        """
        try:
            columns = (
                'Product',
                'ISIN',
                'Amount',
                'Closing',
                'Local Value',
                'Current Value',
            )
            assets.columns = pd.Index(columns)
        except ValueError:
            msg = (
                f'Column mismatch: expected {len(columns)} columns {columns} '
                f'but received {len(assets.columns)}: {assets.columns}.'
            )
            raise ValueError(msg) from None

        return assets

    @staticmethod
    def _convert_str_columns_to_float(assets: pd.DataFrame) -> pd.DataFrame:
        """Converts the 'Current Value' and 'Closing' columns to float.

        Args:
            assets (DataFrame): The DataFrame to process.

        Raises:
            ValueError: If a value can't be converted to float.

        Returns:
            DataFrame: The processed DataFrame.
        """
        for col in ('Current Value', 'Closing'):
            if all(assets[col].apply(lambda x: isinstance(x, str))):
                try:
                    assets[col] = assets[col].apply(lambda x: x.replace(',', '.')).astype('float')
                except ValueError:
                    msg = f'Failed to convert column {col} to float. Check for non-numeric values.'
                    raise ValueError(msg) from None

        return assets

    @staticmethod
    def _clean_portfolio(assets: pd.DataFrame) -> pd.DataFrame:
        """Cleans a portfolio DataFrame.

        The cleaning process includes replacing column names,
        dropping NaN values from 'ISIN', setting 'ISIN' as the index,
        and converting 'Current Value' and 'Closing' to float.

        Args:
            assets (DataFrame): The DataFrame to clean.

        Returns:
            DataFrame: The cleaned DataFrame.
        """
        assets = DegiroPortfolio._replace_columns(assets)
        assets = DegiroPortfolio._dropna_isin(assets)
        assets = DegiroPortfolio._set_index_isin(assets)
        return DegiroPortfolio._convert_str_columns_to_float(assets)
