import pandas as pd
import matplotlib.pyplot as plt


def load(data):
    result = pd.read_csv(data, parse_dates=['Date'])

    return pd.DataFrame(result)


def plot(data, value_name, indicator_name):
    figure = plt.plot(data['Date'], data[value_name])
    figure = plt.plot(data['Date'], data[indicator_name])
    figure = plt.title('Close price')
    figure = plt.xlabel('Date')
    figure = plt.ylabel('Price')
    plt.show()
