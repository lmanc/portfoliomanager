import pandas as pd

# TODO:
# API to get daily closing value
# Class architecture -
# portfolio : init with portfolio.csv and assets.csv - takes care of validation and creating the portfolio object. Must have a currencty attr
# portfolio manager: return views which are some columns of the portfolio and the movments - does not touch the portfolio object, but only read it.

# FIXME:
# currency validator
# when rebalancing there are certain scenarios to be considered:
# - no_sell: all assets in the portfolio must be in assets.csv.
#            assets.csv can have assets that are not in the portfolio.
#
# - sell: join must not discard rows that are not present in one of
#         the two files since operations on all the assets has to be done.
#         Fix `join` in `build_working_dataframe`.
# rebalancing should return the product name instead of the ISIN


def read_portfolio(name: str = 'portfolio.csv') -> pd.DataFrame:
    """
    Reads a .csv file and returns it as a pandas DataFrame.

    Args:
        name (str, optional): The name of the csv file to read. Defaults to 'portfolio.csv'.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the data from the .csv file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    try:
        return pd.read_csv(name)
    except FileNotFoundError as e:
        print(e)
        return


def read_allocation(name: str = 'assets.csv') -> pd.DataFrame:
    """
    Reads an allocation file and returns it as a pandas DataFrame.

    Args:
        name (str): Optional. The name of the allocation file to read. Default is 'assets.csv'.

    Returns:
        pd.DataFrame: A pandas DataFrame representing the allocation data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the sum of percentages in the "Expected Percentage" column is not equal to 100.
    """
    try:
        df = pd.read_csv(name)
    except FileNotFoundError as e:
        print(e)
        return

    try:
        if (s := df['Expected Percentage'].sum()) != 100:
            raise ValueError(
                f'The total sum of percentages in the "Percentage" column is {s}%, not 100.0%'
            )
    except KeyError as e:
        print(e)
        return

    df.set_index('ISIN', inplace=True)

    return df


def clean_dataframe(df: pd.DataFrame, currency: str = 'EUR') -> None:
    """
    Cleans the given dataframe 'df' by standardizing column names, converting 'Current Value' values
    to float type, and dropping rows with missing 'ISIN' values. The function operates in place,
    therefore the changes will be reflected in the original dataframe.

    This function attempts to rename dataframe columns to specific names:
    ['Product', 'ISIN', 'Amount', 'Closing', 'Local value', 'Current Value']. If this fails, it will
    print the error message and terminate the program.

    The function also attempts to change 'Current Value' column values to float type after replacing
    ',' with '.' in these values. In case of any failure (KeyError, AttributeError, ValueError),
    the error message will be printed and the program will be terminated.

    Lastly, the function tries to drop rows with NaN 'ISIN' values. If a KeyError is encountered,
    it will print the error and terminate the program.

    Args:
        df (pd.DataFrame): Dataframe to be cleaned.
        currency (str): Portfolio currency. Default 'EUR'.

    Raises:
        ValueError: If column renaming fails due to the provided dataframe not having the correct number of columns.
        KeyError: If 'Current Value' or 'ISIN' column doesn't exist in the dataframe.
        AttributeError: If 'Current Value' column values are not strings or don't have replace method.
        ValueError: If 'Current Value' column values cannot be converted to float type.

    Returns:
        None
    """
    try:
        df.columns = [
            'Product',
            'ISIN',
            'Amount',
            'Closing',
            'Local value',
            'Current Value',
        ]
    except ValueError as e:
        print(e)
        return

    if df['Current Value'].dtype == 'object':
        try:
            df['Current Value'] = (
                df['Current Value'].apply(lambda x: x.replace(',', '.')).astype('float')
            )

        except (KeyError, AttributeError, ValueError) as e:
            print(e)
            return

    try:
        df.dropna(inplace=True, subset=['ISIN'])
    except KeyError:
        print(e)
        return

    df.set_index('ISIN', inplace=True)


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


def rebalancing_nosell():
    ...


def main():
    pf = read_portfolio()
    clean_dataframe(pf)

    al = read_allocation()

    df = build_working_dataframe(pf, al)


if __name__ == '__main__':
    main()
