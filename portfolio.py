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
