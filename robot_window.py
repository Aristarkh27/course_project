import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
import numpy as np
from datetime import datetime, timedelta
from moving_average import calculate_moving_average
from relative_strength_index import calculate_rsi
from loading_data import read_from_database, read_from_database_all
import datetime
import pytz


# def load_stock_data(stock_code):
#     df = read_from_database_all(stock_code)
#     df['time'] = pd.to_datetime(df['time'])
#     df.set_index('time', inplace=True)
#     return df


def run_trading_robot():
    global df, result, start_date, end_date
    stock_code = stock_code_var.get()
    start_date = start_date_entry.get()
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    start_date = datetime.datetime.combine(start_date, datetime.time())
    start_date = start_date.replace(tzinfo=pytz.UTC)
    end_date = end_date_entry.get()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.combine(end_date, datetime.time())
    end_date = end_date.replace(tzinfo=pytz.UTC)
    print()
    algorithm = algorithm_var.get()

    df = read_from_database(stock_code, start_date, end_date)
    print(df)
    if algorithm == "Moving Average":
        result = calculate_moving_average(df['close'])[0]
        plot_data(df, result, ['Moving Average short', 'Moving Average long'])
    elif algorithm == "RSI":
        result = calculate_rsi(df['close'])[0]
        plot_data(df, result, ['RSI'])


def plot_data(df, result, titles):
    global canvas, fig, ax
    fig, ax = plt.subplots(figsize=(10, 5))
    df['close'].plot(ax=ax, label='Close Price')
    for title in titles:
        result.plot(ax=ax, label=title)
    graph_title = "Moving Average"
    if titles[0] == "RSI":
        graph_title = "RSI"
    ax.set_title(f'{graph_title} for {stock_code_var.get()}')
    ax.legend()
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# Функция обновления графика
def update_plot():
    if not hasattr(update_plot, "counter"):
        update_plot.counter = 0

    if update_plot.counter < len(df):
        current_data = df.iloc[:update_plot.counter]
        current_result = result.iloc[:update_plot.counter]

        ax.clear()
        # current_data.plot(x='time', y='close')
        current_data['close'].plot(ax=ax, label='Close Price')
        current_result.plot(ax=ax, label=algorithm_var.get())
        ax.set_title(f'{algorithm_var.get()} for {stock_code_var.get()}')
        ax.legend()
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)
        canvas.draw()
        update_plot.counter += 1

        # if np.random.rand() > 0.5:
        #     action = "Buy"
        #     profit = round(np.random.rand() * 100, 2)
        # else:
        #     action = "Sell"
        #     profit = round(np.random.rand() * -100, 2)
        #
        # result_label.config(text=f"Action: {action}, Profit: {profit}")

        window.after(1000, update_plot)  # обновление графика


window = tk.Tk()
window.title("Trading Robot Interface")
window.geometry("900x700")
window.configure(bg="#e0f7fa")

logo_image = Image.open("logo.png")
logo_image = logo_image.resize((100, 100), Image.LANCZOS)  # Изменение размера логотипа
logo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(window, image=logo, bg="#e0f7fa")
logo_label.pack(pady=10)

input_frame = tk.LabelFrame(window, text="Input Parameters", bg="#b2ebf2", pady=10, padx=10)
input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

plot_frame = tk.LabelFrame(window, text="Trading Results", bg="#ffffff", pady=10, padx=10)
plot_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Label(input_frame, text="Stock Code:", bg="#b2ebf2").grid(row=0, column=0, padx=5, pady=5, sticky='e')
stock_code_var = tk.StringVar()
stock_code_entry = ttk.Entry(input_frame, textvariable=stock_code_var, width=20)
stock_code_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

tk.Label(input_frame, text="Start Date (YYYY-MM-DD):", bg="#b2ebf2").grid(row=1, column=0, padx=5, pady=5, sticky='e')
start_date_entry = ttk.Entry(input_frame, width=20)
start_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

tk.Label(input_frame, text="End Date (YYYY-MM-DD):", bg="#b2ebf2").grid(row=2, column=0, padx=5, pady=5, sticky='e')
end_date_entry = ttk.Entry(input_frame, width=20)
end_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

tk.Label(input_frame, text="Select Algorithm:", bg="#b2ebf2").grid(row=3, column=0, padx=5, pady=5, sticky='e')
algorithm_var = tk.StringVar(value="Moving Average")
algorithm_menu = ttk.Combobox(input_frame, textvariable=algorithm_var, values=["Moving Average", "RSI"], width=18)
algorithm_menu.grid(row=3, column=1, padx=5, pady=5, sticky='w')

run_button = ttk.Button(input_frame, text="Run Trading Robot", command=lambda:[run_trading_robot(), update_plot()])
run_button.grid(row=4, column=0, columnspan=2, pady=10)

result_label = tk.Label(window, text="", bg="#e0f7fa", font=("Arial", 12))
result_label.pack(pady=10)

window.mainloop()


# TCS00A1028C7
# 2021-01-01
# 2023-01-01
#