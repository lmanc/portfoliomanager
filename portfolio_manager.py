import pandas as pd




def rebalancing_sell(df: pd.DataFrame):
    movement = (df['Expected Value'] - df['Current Value']).round(2)
    return pd.DataFrame({'Product': df['Product'], 'Movments': movement})
