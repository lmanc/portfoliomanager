import pandas as pd

from portfolio import Portfolio


class DegiroPortfolio(Portfolio):
    @staticmethod
    def _replace_columns(df: pd.DataFrame) -> pd.DataFrame:
        try:
            df.columns = [
                'Product',
                'ISIN',
                'Amount',
                'Closing',
                'Local Value',
                'Current Value',
            ]
        except ValueError as e:
            print(e)
            raise ValueError(e) from None

        return df

    @staticmethod
    def _convert_str_columns_to_float(df: pd.DataFrame) -> pd.DataFrame:
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
        df = DegiroPortfolio._replace_columns(df)
        df = DegiroPortfolio._dropna_isin(df)
        df = DegiroPortfolio._set_index_isin(df)
        df = DegiroPortfolio._convert_str_columns_to_float(df)

        return df
