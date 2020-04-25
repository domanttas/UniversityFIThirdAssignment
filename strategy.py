from utils import load, plot


data = load('./data.csv')


data['100MA'] = data['Close'].rolling(window=100).mean()


plot(data, 'Close', '100MA')
