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


def plot_calculated_data(data, value_name, indicator_name, upper, lower):
    figure = plt.plot(data['Date'], data[value_name])
    figure = plt.plot(data['Date'], data[indicator_name])
    figure = plt.plot(data['Date'], data[upper])
    figure = plt.plot(data['Date'], data[lower])

    figure = plt.legend(['Close', indicator_name, upper, lower])
    figure = plt.title('Close price')
    figure = plt.xlabel('Date')
    figure = plt.ylabel('Price')

    plt.show()
