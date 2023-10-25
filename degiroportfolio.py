import pandas as pd

from portfolio import Portfolio


class DegiroPortfolio(Portfolio):
    """
    A subclass of Portfolio that represents a Degiro portfolio.
    """

    @staticmethod
    def _replace_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Replaces the column names in a DataFrame.

        The columns are renamed to: 'Product', 'ISIN', 'Amount', 'Closing', 'Local Value', 'Current Value'.

        Args:
            df (DataFrame): The DataFrame to process.

        Raises:
            ValueError: If the DataFrame doesn't have the correct number of columns.

        Returns:
            DataFrame: The processed DataFrame.
        """
        try:
            df.columns = pd.Index([
                'Product',
                'ISIN',
                'Amount',
                'Closing',
                'Local Value',
                'Current Value',
            ])
        except ValueError as e:
            print(e)
            raise ValueError(e) from None

        return df

    @staticmethod
    def _convert_str_columns_to_float(df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts the 'Current Value' and 'Closing' columns to float.

        Args:
            df (DataFrame): The DataFrame to process.

        Raises:
            ValueError: If a value can't be converted to float.

        Returns:
            DataFrame: The processed DataFrame.
        """
        for col in ('Current Value', 'Closing'):
            if all(df[col].apply(lambda x: isinstance(x, str))):
                try:
                    df[col] = (
                        df[col]
                        .apply(lambda x: x.replace(',', '.'))
                        .astype('float')
                    )
                except ValueError as e:
                    print(e)
                    raise ValueError(e) from None

        return df

    @staticmethod
    def _clean_portfolio(df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans a portfolio DataFrame.

        The cleaning process includes replacing column names, dropping NaN values from 'ISIN',
        setting 'ISIN' as the index, and converting 'Current Value' and 'Closing' to float.

        Args:
            df (DataFrame): The DataFrame to clean.

        Returns:
            DataFrame: The cleaned DataFrame.
        """
        df = DegiroPortfolio._replace_columns(df)
        df = DegiroPortfolio._dropna_isin(df)
        df = DegiroPortfolio._set_index_isin(df)
        df = DegiroPortfolio._convert_str_columns_to_float(df)

        return df
