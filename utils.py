import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


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

    selling_positions = selling_positions[selling_positions['Corrupted'].isin([
        False])]
    buying_positions = buying_positions[buying_positions['Corrupted'].isin([
        False])]

    figure = plt.plot(
        selling_positions['Date'], selling_positions[value_name], marker='x', color='blue', linewidth=0)
    figure = plt.plot(
        buying_positions['Date'], buying_positions[value_name], marker='x', color='red', linewidth=0)

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
    value = data['Strategy return'].cumsum()
    figure = plt.plot(data['Date'], value)
    figure = plt.title(title)
    plt.show()


def get_ma(data):
    return data['Close'].rolling(window=100).mean()


def get_upper_band(data, window_number, std_number):
    return get_ma(data) + (data['Close'].rolling(window=window_number).std() * std_number)


def get_lower_band(data, window_number, std_number):
    return get_ma(data) - (data['Close'].rolling(window=window_number).std() * std_number)


def stop_loss(data):
    orders = pd.DataFrame(columns=data.columns)
    for row in range(len(data)):
        if data['Position'].iloc[row] == 1 and data['Corrupted'].iloc[row] == False and data['Order'].iloc[row] == True:
            orders = orders.append({
                'Close': data['Close'].iloc[row],
                'Date': data['Date'].iloc[row]
            }, ignore_index=True)

    for order_row in range(len(orders)):
        for data_row in range(len(data)):
            data_date = datetime.strptime(
                str(data['Date'].iloc[data_row]), "%Y-%m-%d %H:%M:%S")
            order_date = datetime.strptime(
                str(orders['Date'].iloc[order_row]), "%Y-%m-%d %H:%M:%S")

            if data_date > order_date and data['Corrupted'].iloc[data_row] == False and data['Order'].iloc[data_row] == True:
                if (data['Close'].iloc[data_row] * 0.99) < orders['Close'].iloc[order_row]:
                    data['Position'].iloc[data_row] = -1
                    data['Corrupted'].iloc[data_row] = False
                    data['TradeCost'].iloc[data_row] = 0.1

    return data


def get_positions(data):
    data['Position'] = None
    data['TradeCost'] = None
    data['Corrupted'] = True
    data['Order'] = False
    for row in range(len(data)):
        if (data['Close'].iloc[row] > data['UpperBand'].iloc[row]) and (data['Close'].iloc[row-1] < data['UpperBand'].iloc[row-1]):
            data['Position'].iloc[row] = -1
            data['TradeCost'].iloc[row] = 0.1
            data['Corrupted'].iloc[row] = False
        if (data['Close'].iloc[row] < data['LowerBand'].iloc[row]) and (data['Close'].iloc[row-1] > data['LowerBand'].iloc[row-1]):
            data['Position'].iloc[row] = 1
            data['TradeCost'].iloc[row] = 0.1
            data['Corrupted'].iloc[row] = False
            data['Order'].iloc[row] = True

    data['Position'].fillna(method='ffill', inplace=True)
    data['TradeCost'].fillna(value=0, inplace=True)
    return data


def plot_comparison(data, optimized_data):
    plt.plot(data['Date'], data['Strategy return'].cumsum())
    plt.title('Default')

    plt.plot(optimized_data['Date'],
             optimized_data['Strategy return'].cumsum())
    plt.title('Compared')

    plt.legend(['Default', 'Optimized'])

    plt.show()
