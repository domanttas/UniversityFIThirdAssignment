from utils import load, plot_data, plot_calculated_data, plot_profit, get_ma, get_lower_band, get_upper_band, get_positions, plot_comparison, stop_loss
import pandas as pd


data = load('./first_data_sample.csv')
starting_data = data.copy()


# MA for 100 days
data['100MA'] = get_ma(data)
# Bollinger's upper band
data['UpperBand'] = get_upper_band(data, 100, 2)
# Bollinger's lower band
data['LowerBand'] = get_lower_band(data, 100, 2)


data = get_positions(data)


# Plot start data
plot_data(data, 'Close', '100MA', 'UpperBand', 'LowerBand')

# Plot strategy data
plot_calculated_data(data, 'Close', '100MA', 'UpperBand',
                     'LowerBand', 'Without optimization')

# Plot profit without optimization
data['Trade'] = data['Close'] + data['TradeCost']
data['Return'] = data['Trade'].pct_change()
data['Strategy return'] = data['Return'] * data['Position']
plot_profit(data, 'Without optimization')


# Brute force optimization
ma_values = [10, 40, 70, 100]
std_values = [0.5, 1, 1.5, 2, 2.5, 3]
optimization_data = starting_data.copy()

result_df = pd.DataFrame({
    'window': [],
    'std': [],
    'result': []
})

for std_value in std_values:
    for ma_value in ma_values:
        optimization_data = starting_data.copy()
        ma = get_ma(optimization_data)
        upper_band = get_upper_band(optimization_data, ma_value, std_value)
        lower_band = get_lower_band(optimization_data, ma_value, std_value)

        optimization_data['100MA'] = ma
        optimization_data['UpperBand'] = upper_band
        optimization_data['LowerBand'] = lower_band

        optimization_data = get_positions(optimization_data)

        optimization_data['Return'] = optimization_data['Close'].pct_change()
        optimization_data['Strategy return'] = optimization_data['Return'] * \
            optimization_data['Position']

        result_df = result_df.append({
            'window': ma_value,
            'std': std_value,
            'result': optimization_data['Strategy return'].sum()
        }, ignore_index=True)


print(result_df.sort_values(by=['result'], ascending=False))

# Plotting for best data from optimization
best_row = result_df.loc[result_df['result'].idxmax()]
best_ma = int(best_row['window'])
best_std = best_row['std']

print(best_std)
print(best_ma)

best_data = starting_data.copy()

ma = get_ma(best_data)
upper_band = get_upper_band(best_data, best_ma, best_std)
lower_band = get_lower_band(best_data, best_ma, best_std)

best_data['100MA'] = ma
best_data['UpperBand'] = upper_band
best_data['LowerBand'] = lower_band

best_data = get_positions(best_data)

# Plot strategy data
plot_calculated_data(best_data, 'Close', '100MA',
                     'UpperBand', 'LowerBand', 'Optimized')

# Plot profit with optimization
best_data['Trade'] = best_data['Close'] + best_data['TradeCost']
best_data['Return'] = best_data['Trade'].pct_change()
best_data['Strategy return'] = best_data['Return'] * best_data['Position']

plot_profit(best_data, 'Optimized')
plot_comparison(data, best_data)
