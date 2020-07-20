from matplotlib import pyplot as plt
import pandas as pd

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def chart_from_csv(file_path, column_x, column_y, x_label_name='', y_label_name='', title_name=''):
    df = pd.read_csv(file_path)
    df[column_x] = pd.to_datetime(df.Date)
    chart = df.groupby(df[column_x].dt.strftime('%y'))[column_y].sum()

    chart = chart.sort_values()

    fig, ax = plt.subplots(figsize=(50, 50))
    ax.plot(chart, color='purple')

    ax.set(xlabel=x_label_name, ylabel=y_label_name, title=title_name)
    plt.show()


file_path = "C:/Users/kmaran/Downloads/Walmart_Store_sales.csv"
column_x = 'Date'
column_y = 'Weekly_Sales'
x_label_name = 'Months'
y_label_name = 'Weekly Sales'
title_name='Monthly Sales'
chart_from_csv(file_path, column_x, column_y, x_label_name, y_label_name, title_name)