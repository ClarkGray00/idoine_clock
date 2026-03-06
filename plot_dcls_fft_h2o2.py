import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq

def load_data(file_path):
    """Load CSV data into a pandas DataFrame."""
    df = pd.read_csv(file_path)
    df = df.sort_values(by="#Time", ascending=True)
    df = df.dropna()
    #print(df)
    new_time = np.linspace(df["#Time"].min(), df["#Time"].max(), len(df))
    df['penta_wma'] = np.interp(new_time, df["#Time"], df["penta_wma"])
    df["#Time"] = new_time  # Replace original time values with evenly spaced ones
    
    return df

def filter_time_range(df, t_min, t_max):
    """Filter the DataFrame based on the specified time range."""
    return df[(df['#Time'] >= t_min) & (df['#Time'] <= t_max)]

def apply_fourier_transform(time, intensity):
    """Apply Fourier Transform to the intensity data."""
    N = len(time)
    dt = np.mean(np.diff(time))  # Compute the time step
    freq = fftfreq(N, dt)  # Frequency axis
    fft_values = fft(intensity)  # Perform FFT
    return freq, np.abs(fft_values)

from matplotlib.colors import LinearSegmentedColormap
custom_cmap = LinearSegmentedColormap.from_list("green_black", ["blue", "black"])
# Generate values from 0 to 1 (for color transitions)
values = np.linspace(0, 1, 210)

# Extract the corresponding RGB colors from the custom colormap
colors = [custom_cmap(val) for val in values]

filenames = [
             'briggs_rauscher_run13_700c_0_5e_86p_1a_0i_DCLS',
             'briggs_rauscher_run14_700c_0_5e_86p_1a_0i_DCLS',
             'briggs_rauscher_run15_700c_0_5e_86p_1a_0i_DCLS',
             'briggs_rauscher_run1_700c_0_5e_86p_1a_0i_DCLS',]


#'briggs_rauscher_run9_700c_0_5e_86p_1a_0i_DCLS'
colors = [colors[2],colors[50],colors[94],colors[200]]

plt.figure(figsize=(15, 15))

legend_names = ['0.44M','0.88M','1.76M','3.08M']

time_lims = [(207.9, 363.7), (142.4, 445.2), (90,385.8), (46.18,382.23), (40.8,533.7)]
plt.xlabel("Frequency (mHz)", fontsize = 20,labelpad=15)
plt.ylabel("Amplitude (a.u.)", fontsize = 20,labelpad=15)
plt.title("Fourier Transform of Intensity")
#plt.grid()

for i in range(len(filenames)):
#for i in range(2):
    filename = filenames[i]

    file_path = '2_datasets/' + str(filename) + '.csv'

    df = load_data(file_path)


    #t_min = float(input("Enter minimum time: "))
    t_max = max(df['#Time'].values)
    #print(df)

    df_filtered = filter_time_range(df, time_lims[i][0],time_lims[i][1])
    #if df_filtered.empty:
    #    print("No data in the specified range.")

    time = df_filtered['#Time'].values
    #time = df['#Time'].values
   
    intensity = df_filtered['penta_wma'].values
    #print(intensity)
    # print(time)

    freq, fft_values = apply_fourier_transform(time, intensity)
    #if i == 5:
    #    plt.plot(1000*freq, (4*i+1)*fft_values-400*i,alpha=0.7, label=legend_names[i],linewidth = 2, color = colors[i])
    #if i <5:    
    plt.plot(1000*freq, fft_values-150*i,alpha=0.7, label=legend_names[i],linewidth = 2, color = colors[i])
    
    plt.text(240, (1+i)-150*i+25, legend_names[i], fontsize=18,fontweight='bold',color=colors[i],ha='right', va='center')


#plt.axvline(30, color = 'k', linestyle = '--',alpha = 0.8)
plt.xlim(0,250)
plt.ylim(-450,100)
plt.yticks([])
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.savefig('7_figures/' + 'DCLS_h202_BR_FFT' + '_plot.png', dpi=700)

plt.show()
