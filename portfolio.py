import pandas as pd


class Portfolio:
    @staticmethod
    def _read_file(file: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file)
        except FileNotFoundError as e:
            print(e)
            raise FileNotFoundError(e) from None

    @staticmethod
    def _replace_columns(df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    @staticmethod
    def _dropna_isin(df: pd.DataFrame) -> pd.DataFrame:
        return df.dropna(subset=['ISIN'])

    @staticmethod
    def _set_index_isin(df: pd.DataFrame) -> pd.DataFrame:
        return df.set_index('ISIN')

    @staticmethod
    def _convert_str_columns_to_float(df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    @staticmethod
    def _validate_allocation_percentage_sum(df: pd.DataFrame) -> bool:
        return df['Expected Percentage'].sum() == 100

