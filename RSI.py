import pandas as pd

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def main():
    #file with stocks (we want csv)
    df = pd.read_csv('stock_data.csv')

    # convert index (datetime)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # count RSI
    df['RSI'] = calculate_rsi(df['Close'])

    print(df)

if __name__ == "__main__":
    main()





