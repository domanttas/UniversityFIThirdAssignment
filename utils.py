import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load(data):
    result = pd.read_csv(data, parse_dates=['Date'])

    return pd.DataFrame(result)


def plot_data(data, value_name, indicator_name, upper, lower):
    figure = plt.plot(data['Date'], data[value_name])
    figure = plt.plot(data['Date'], data[indicator_name])
    figure = plt.plot(data['Date'], data[upper])
    figure = plt.plot(data['Date'], data[lower])

    figure = plt.legend(['Close', indicator_name, upper, lower])
    figure = plt.title('Close price')
    figure = plt.xlabel('Date')
    figure = plt.ylabel('Price')

    plt.show()


def plot_calculated_data(data, value_name, indicator_name, upper, lower, title):
    selling_positions = data[data['Position'].isin([-1])]
    buying_positions = data[data['Position'].isin([1])]

    figure = plt.plot(
        selling_positions['Date'], selling_positions[value_name], marker='x', color='blue')
    figure = plt.plot(
        buying_positions['Date'], buying_positions[value_name], marker='x', color='red')

    figure = plt.plot(data['Date'], data[value_name])
    figure = plt.plot(data['Date'], data[indicator_name])
    figure = plt.plot(data['Date'], data[upper])
    figure = plt.plot(data['Date'], data[lower])

    figure = plt.legend(['Sell', 'Buy', 'Close', indicator_name, upper, lower])
    figure = plt.title(title)
    figure = plt.xlabel('Date')
    figure = plt.ylabel('Price')

    plt.show()


def plot_profit(data, title):
    figure = plt.plot(data['Date'], data['Strategy return'].cumsum())
    figure = plt.title(title)
    plt.show()


def get_ma(data):
    return data['Close'].rolling(window=100).mean()


def get_upper_band(data, window_number, std_number):
    return get_ma(data) + (data['Close'].rolling(window=window_number).std() * std_number)


def get_lower_band(data, window_number, std_number):
    return get_ma(data) - (data['Close'].rolling(window=window_number).std() * std_number)


def get_positions(data):
    data['Position'] = None
    for row in range(len(data)):
        if (data['Close'].iloc[row] > data['UpperBand'].iloc[row]) and (data['Close'].iloc[row-1] < data['UpperBand'].iloc[row-1]):
            data['Position'].iloc[row] = -1
        if (data['Close'].iloc[row] < data['LowerBand'].iloc[row]) and (data['Close'].iloc[row-1] > data['LowerBand'].iloc[row-1]):
            data['Position'].iloc[row] = 1

    data['Position'].fillna(method='ffill', inplace=True)
    return data


def plot_comparison(data, optimized_data):
    plt.plot(data['Date'], data['Strategy return'].cumsum())
    plt.title('Default')

    plt.plot(optimized_data['Date'], optimized_data['Strategy return'].cumsum())
    plt.title('Optimized')

    plt.legend(['Default', 'Optimized'])

    plt.show()
