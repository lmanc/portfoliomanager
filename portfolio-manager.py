import pandas as pd


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
        exit()


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
        exit()

    try:
        if (s := df['Expected Percentage'].sum()) != 100:
            raise ValueError(
                f'The total sum of percentages in the "Percentage" column is {s}%, not 100.0%'
            )
    except KeyError as e:
        print(e)
        exit()

    df.set_index('ISIN', inplace=True)

    return df


def clean_dataframe(df: pd.DataFrame) -> None:
    """
    Cleans the given dataframe 'df' by standardizing column names, converting 'Value in EUR' values
    to float type, and dropping rows with missing 'ISIN' values. The function operates in place,
    therefore the changes will be reflected in the original dataframe.

    This function attempts to rename dataframe columns to specific names:
    ['Product', 'ISIN', 'Amount', 'Closing', 'Local value', 'Value in EUR']. If this fails, it will
    print the error message and terminate the program.

    The function also attempts to change 'Value in EUR' column values to float type after replacing
    ',' with '.' in these values. In case of any failure (KeyError, AttributeError, ValueError),
    the error message will be printed and the program will be terminated.

    Lastly, the function tries to drop rows with NaN 'ISIN' values. If a KeyError is encountered,
    it will print the error and terminate the program.

    Args:
        df (pd.DataFrame): Dataframe to be cleaned.

    Raises:
        ValueError: If column renaming fails due to the provided dataframe not having the correct number of columns.
        KeyError: If 'Value in EUR' or 'ISIN' column doesn't exist in the dataframe.
        AttributeError: If 'Value in EUR' column values are not strings or don't have replace method.
        ValueError: If 'Value in EUR' column values cannot be converted to float type.

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
            'Value in EUR',
        ]
    except ValueError as e:
        print(e)
        exit()

    try:
        df['Value in EUR'] = (
            df['Value in EUR'].apply(
                lambda x: x.replace(
                    ',', '.')).astype('float'))
    except (KeyError, AttributeError, ValueError) as e:
        print(e)
        exit()

    try:
        df.dropna(inplace=True, subset=['ISIN'])
    except KeyError:
        print(e)
        exit()

    df.set_index('ISIN', inplace=True)


def get_total_value(df: pd.DataFrame) -> float:
    """
    Calculates and returns the total value of the 'Value in EUR' column in the provided pandas DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data. Expected to have a column named 'Value in EUR'.

    Returns:
        float: The total value of the 'Value in EUR' column.

    Raises:
        KeyError: If the DataFrame does not contain a 'Value in EUR' column.
    """
    try:
        return df['Value in EUR'].sum()
    except KeyError as e:
        print(e)
        exit()


def build_working_dataframe(
        pf: pd.DataFrame,
        al: pd.DataFrame) -> pd.DataFrame:
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
    df['Current Percentage'] = (
        df['Value in EUR'] /
        get_total_value(df) *
        100).apply(
        lambda x: round(
            x,
            2))

    return df.join(al)


def main():
    pf = read_portfolio()
    clean_dataframe(pf)

    al = read_allocation()

    df = build_working_dataframe(pf, al)


if __name__ == '__main__':
    main()
