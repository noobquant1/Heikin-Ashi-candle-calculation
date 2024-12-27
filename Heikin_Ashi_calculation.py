import pandas as pd
import datetime

# Load the Excel file containing historical 5-minute data for NIFTY50.
file_name = 'NIFTY50_5min_data.xlsx'
df = pd.read_excel(file_name)

# Display the last few rows of the DataFrame to ensure data is loaded correctly.
print(df.tail())

# Function to calculate Heiken Ashi candles
def calculate_heiken_ashi(df: pd.DataFrame) -> pd.DataFrame:
    # Create a copy of the DataFrame to avoid modifying the original data.
    df_HA = df.copy()

    # Calculate the Heiken-Ashi close price:
    # It's the average of the current period's open, high, low, and close prices.
    df_HA['HA_close'] = round(((df_HA['open'] + df_HA['high'] + df_HA['low'] + df_HA['close']) / 4), 2)

    # Initialize HA_open, HA_high, and HA_low with default values.
    df_HA['HA_open'] = 0.0
    df_HA['HA_high'] = 0.0
    df_HA['HA_low'] = 0.0

    # Loop through the DataFrame to calculate the Heiken-Ashi open price iteratively.
    for i in range(len(df_HA)):
        if i == 0:
            # For the first row, HA_open is the average of the first row's open and close.
            df_HA.loc[i, 'HA_open'] = round(((df_HA.loc[i, 'open'] + df_HA.loc[i, 'close']) / 2), 2)
        else:
            # For subsequent rows, HA_open is the average of the previous row's HA_open and HA_close.
            df_HA.loc[i, 'HA_open'] = round(((df_HA.loc[i - 1, 'HA_open'] + df_HA.loc[i - 1, 'HA_close']) / 2), 2)

    # Calculate HA_high as the maximum of HA_open, HA_close, and the actual high price for the period.
    df_HA['HA_high'] = round((df_HA[['HA_open', 'HA_close', 'high']].max(axis=1)), 2)

    # Calculate HA_low as the minimum of HA_open, HA_close, and the actual low price for the period.
    df_HA['HA_low'] = round((df_HA[['HA_open', 'HA_close', 'low']].min(axis=1)), 2)

    # Optional: You can return only the Heiken-Ashi columns for easier visualization.
    #print(df_HA[['timestamp', 'HA_open', 'HA_high', 'HA_low', 'HA_close']].tail())
    return df_HA

# Call the function to calculate Heiken-Ashi candles for the loaded data.
HA_data = calculate_heiken_ashi(df)

# Print the last few rows of the DataFrame with the calculated Heiken-Ashi values.
print(HA_data[['timestamp', 'HA_open', 'HA_high', 'HA_low', 'HA_close']].tail())
