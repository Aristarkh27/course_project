import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('USD000UTSTOM.csv')

df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)

fig.add_trace(go.Scatter(x=df.index, y=df['close'], name='Close'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=df['volume'], name='Volume'), row=2, col=1)

fig.update_layout(height=600, width=900, title_text="Time Series and Volume", xaxis_rangeslider_visible=True)
fig.show()


#  ACF и PACF
def plot_acf_pacf(data, lags=30):
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))

    plot_acf(data, lags=lags, ax=axes[0], title='ACF Plot')
    plot_pacf(data, lags=lags, ax=axes[1], title='PACF Plot')

    plt.tight_layout()
    plt.show()

plot_acf_pacf(df['close'])