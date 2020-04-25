from utils import load, plot_data, plot_calculated_data


data = load('./data.csv')


# MA for 100 days
data['100MA'] = data['Close'].rolling(window=100).mean()
# Bollinger's upper band
data['UpperBand'] = data['100MA'] + \
    (data['Close'].rolling(window=100).std() * 2)
# Bollinger's lower band
data['LowerBand'] = data['100MA'] - \
    (data['Close'].rolling(window=100).std() * 2)


data['Position'] = None


for row in range(len(data)):
    if (data['Close'].iloc[row] > data['UpperBand'].iloc[row]) and (data['Close'].iloc[row-1] < data['UpperBand'].iloc[row-1]):
        data['Position'] = -1
    if (data['Close'].iloc[row] < data['LowerBand'].iloc[row]) and (data['Close'].iloc[row-1] > data['LowerBand'].iloc[row-1]):
        data['Position'] = 1

data['Position'].fillna(method='ffill', inplace=True)


# plot_data(data, 'Close', '100MA', 'UpperBand', 'LowerBand')
plot_calculated_data(data, 'Close', '100MA', 'UpperBand', 'LowerBand')
