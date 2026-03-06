import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys


# Function to apply WMA smoothing
def wma_smoothing(y, span):
    weights = np.arange(1, span + 1)

    return pd.Series(y).rolling(window=span).apply(lambda x: np.dot(x, weights)/weights.sum(), raw=True)
# Read filename and validate input
filename = input('Please enter the filename from /2_datasets : ')
if filename == '':
    sys.exit()

file_path = '2_datasets/' + str(filename) + '.csv'

# Read number of y-variables and validate input
columns_n = input('Enter the number of y-variables : ')
columns_n = int(columns_n)

# Load data
df = pd.read_csv(file_path)
time = df.iloc[:, :columns_n]
num_spectra = len(df)

intensities = df.iloc[:, columns_n:].values
clean_columns = [col.replace(".", "", 1) if col.count('.') > 1 else col for col in df.columns[columns_n:]]

wavenumbers = np.array([float(col) for col in df.columns[columns_n:]])

spectral_length = len(wavenumbers)

final_array = np.empty((0, spectral_length))
final_array = np.append(final_array, [wavenumbers], axis=0)

while True:
    # Prompt user for smoothing span
    span_input = input('Enter the WMA span (smoothing factor) or type "S" to save and exit: ')
    if span_input == '':
        sys.exit()
    if span_input.upper() == 'S':
        if final_array.shape[0] > 1:
            csv_file_path = f'2_datasets/{filename}_wma_span{span}.csv'
            fd = pd.DataFrame(final_array[1:], columns=final_array[0])
            fd = pd.concat([time, fd], axis=1)
            fd.to_csv(csv_file_path, index=False)
            print(f'WMA-smoothed file saved as: {filename}_wma_span{span}.csv')
        else:
            print("No data to save.")
        break

    try:
        span = int(span_input)
    except ValueError:
        print("Please enter a valid integer for the WMA span.")
        continue

    # Create a new DataFrame for plotting
    final_array = np.empty((0, spectral_length))
    final_array = np.append(final_array, [wavenumbers], axis=0)

    # Apply WMA smoothing and plot
    for f in range(num_spectra):
        x = intensities[f, :]
        x = np.array(x)
        smoothed_x = wma_smoothing(x, span)
        noise_x = smoothed_x - x

        alpha_value = 1.0 if num_spectra == 1 else (f + 1) / num_spectra

        plt.plot(wavenumbers, x, color='r', linewidth=1, alpha=alpha_value )
        plt.plot(wavenumbers, smoothed_x, color='b', linewidth=1, alpha=alpha_value )
        plt.plot(wavenumbers, noise_x, color='k', linewidth=1, alpha=alpha_value)
        
        final_array = np.append(final_array, [smoothed_x], axis=0)
    plt.axhline(color='gray', linestyle = '--')
    plt.show()