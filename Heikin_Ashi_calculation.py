import pandas as pd
import datetime
# Load Excel file
file_name = 'NIFTY50_5min_data.xlsx'
df = pd.read_excel(file_name)

# Display the first few rows
print(df.tail())
# Function to calculate Heiken Ashi candles
def calculate_heiken_ashi(df: pd.DataFrame) -> pd.DataFrame:
    df_HA = df.copy()
    # Calculate HA close price
    df_HA['HA_close'] = round(((df_HA['open'] + df_HA['high'] + df_HA['low'] + df_HA['close']) / 4),2)

    # Initialize HA_open
    df_HA['HA_open'] = 0.0
    df_HA['HA_high'] = 0.0
    df_HA['HA_low'] = 0.0

    # Loop through the dataframe to calculate HA_open iteratively
    for i in range(len(df_HA)):
        if i == 0:
            df_HA.loc[i, 'HA_open'] = round(((df_HA.loc[i, 'open'] + df_HA.loc[i, 'close']) / 2),2)
        else:
            df_HA.loc[i, 'HA_open'] = round(((df_HA.loc[i - 1, 'HA_open'] + df_HA.loc[i - 1, 'HA_close']) / 2),2)

    # Calculate HA_high and HA_low
    df_HA['HA_high'] = round((df_HA[['HA_open', 'HA_close', 'high']].max(axis=1)),2)
    df_HA['HA_low'] = round((df_HA[['HA_open', 'HA_close', 'low']].min(axis=1)),2)

    # Optional: Return only HA columns
    #print(df_HA[['timestamp', 'HA_open', 'HA_high', 'HA_low', 'HA_close']].tail())
    return df_HA

HA_data = calculate_heiken_ashi(df)
print(HA_data[['timestamp', 'HA_open', 'HA_high', 'HA_low', 'HA_close']].tail())