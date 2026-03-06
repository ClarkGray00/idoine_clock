import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq

def load_data(i, file_path):
    """Load CSV data into a pandas DataFrame."""
    df = pd.read_csv(file_path)
    
    
    if i ==0:
        df = df.sort_values(by="#Time", ascending=True)
        new_time = np.linspace(df["#Time"].min(), df["#Time"].max(), len(df))
        df['penta_wma'] = np.interp(new_time, df["#Time"], df["penta_wma"])
        df["#Time"] = new_time
    if i ==1:
        df = df.sort_values(by="Time (s)", ascending=True)
        new_time = np.linspace(df["Time (s)"].min(), df["Time (s)"].max(), len(df))
        df['V'] = np.interp(new_time, df["Time (s)"], df["V"])
        df["Time (s)"] = new_time
    
    #print(df)
      # Replace original time values with evenly spaced ones

    df = df.dropna()
    
    return df

def filter_time_range(df, t_min, t_max):
    """Filter the DataFrame based on the specified time range."""
    if i ==0: 
        return df[(df['#Time'] >= t_min) & (df['#Time'] <= t_max)]
    if i ==1: 
        return df[(df['Time (s)'] >= t_min) & (df['Time (s)'] <= t_max)]

def apply_fourier_transform(time, intensity):
    """Apply Fourier Transform to the intensity data."""
    N = len(time)
    dt = np.mean(np.diff(time))  # Compute the time step
    freq = fftfreq(N, dt)  # Frequency axis
    fft_values = fft(intensity)  # Perform FFT
    return freq, np.abs(fft_values)

from matplotlib.colors import LinearSegmentedColormap
custom_cmap = LinearSegmentedColormap.from_list("blue_purple_red", ["black", "orange"])
# Generate values from 0 to 1 (for color transitions)
values = np.linspace(0, 1, 44)
colors = [custom_cmap(val) for val in values]
# Extract the corresponding RGB colors from the custom colormap
colors = [colors[1],colors[43]]

filenames = ['briggs_rauscher_run5_700c_0_5e_86p_1a_0i_DCLS',
             'run16_hues_542_794_266_497']


#'briggs_rauscher_run9_700c_0_5e_86p_1a_0i_DCLS'
plt.figure(figsize=(15, 15))


legend_names = ['Starch','No Starch']

time_lims = [(40.8,533.7), (38.2,190.6)]
plt.xlabel("Frequency (ms⁻¹)", fontsize = 20,labelpad=15)
plt.ylabel("Amplitude (a.u.)", fontsize = 20,labelpad=15)
plt.title("Fourier Transform of Intensity")
#plt.grid()

for i in range(len(filenames)):
#for i in range(2):
    if i==1:
        filename = filenames[i]
        file_path = '2_datasets/' + str(filename) + '.csv'
        df = load_data(i, file_path)
        df_filtered = filter_time_range(df, time_lims[i][0],time_lims[i][1])
        time = df_filtered['Time (s)'].values
        #time = df['#Time'].values
        intensity = df_filtered['V'].values

    if i==0:
        filename = filenames[i]
        file_path = '2_datasets/' + str(filename) + '.csv'
        df = load_data(i, file_path)
        print(df)
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
    if i ==0:
        plt.plot(1000*freq, fft_values*2-i,alpha=0.9, label=legend_names[i],linewidth = 3, color = colors[i])
    if i ==1:
        plt.plot(1000*freq, (fft_values)/1000 - 150*i,alpha=0.9, label=legend_names[i],linewidth = 3, color = colors[i])
    
    plt.text(380, -150*i-15, legend_names[i], fontsize=18,fontweight='bold',color=colors[i],ha='right', va='center')


#plt.axvline(30, color = 'k', linestyle = '--',alpha = 0.8)
plt.xlim(0,400)
plt.ylim(-200,200)
plt.yticks([])
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.savefig('7_figures/' + 'DCLS_starch_BR_FFT' + '_plot.png', dpi=700)

plt.show()
