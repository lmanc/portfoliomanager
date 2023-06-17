import pandas as pd


def get_total_value(df: pd.DataFrame) -> float:
    """
    Calculates and returns the total value of the 'Current Value' column in the provided pandas DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data. Expected to have a column named 'Current Value'.

    Returns:
        float: The total value of the 'Current Value' column.

    Raises:
        KeyError: If the DataFrame does not contain a 'Current Value' column.
    """
    try:
        return df['Current Value'].sum()
    except KeyError as e:
        print(e)
        return


def build_working_dataframe(pf: pd.DataFrame, al: pd.DataFrame) -> pd.DataFrame:
    """
    This function creates a working DataFrame from the provided DataFrames.
    The function drops several columns from the primary dataframe, then
    calculates and adds a new column 'Current Percentage'. Finally, it joins
    the additional DataFrame on the primary DataFrame and returns the result.

    Args:
        pf (pd.DataFrame): The primary DataFrame.
        al (pd.DataFrame): The additional dataframe to be joined with the
            primary dataframe.

    Returns:
        pd.DataFrame: The resulting dataframe after dropping specified columns,
            adding 'Current Percentage' column, and joining with the additional DataFrame.
    """
    df = pf.drop(['Amount', 'Closing', 'Local value'], axis=1)
    df['Current Percentage'] = (df['Current Value'] / get_total_value(df) * 100).apply(
        lambda x: round(x, 2)
    )

    total_value = get_total_value(df)
    df = df.join(al)
    df['Expected Value'] = (total_value / 100 * df['Expected Percentage']).round(2)

    return df[
        [
            'Product',
            'Current Value',
            'Expected Value',
            'Current Percentage',
            'Expected Percentage',
        ]
    ]


def rebalancing_sell(df: pd.DataFrame):
    movement = (df['Expected Value'] - df['Current Value']).round(2)
    return pd.DataFrame({'Product': df['Product'], 'Movments': movement})
