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
custom_cmap = LinearSegmentedColormap.from_list("blue_purple_red", ["blue", "purple", "red"])

# Generate values from 0 to 1 (for color transitions)
values = np.linspace(0, 1, 44)

# Extract the corresponding RGB colors from the custom colormap
colors = [custom_cmap(val) for val in values]

filenames = ['briggs_rauscher_run6_700c_0_5e_86p_1a_0i_DCLS',
             'briggs_rauscher_run2_700c_0_5e_86p_1a_0i_DCLS',
             'briggs_rauscher_run1_700c_0_5e_86p_1a_0i_DCLS',
             'briggs_rauscher_run5_700c_0_5e_86p_1a_0i_DCLS',
             'briggs_rauscher_run4_700c_0_5e_86p_1a_0i_DCLS',
             'briggs_rauscher_run3_700c_0_5e_86p_1a_0i_DCLS']


colors = [colors[1],colors[13],colors[17],colors[22],colors[29],colors[43]]

plt.figure(figsize=(15, 15))

legend_names = ['5°C','13°C','17°C','22°C','29°C','43°C']

time_lims = [(93.8, 1244.4), (52, 759.21), (40.43,526.25), (46.18,382.23), (31.06,247.14),(36.7,123.4)]
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
    if i == 5:
        plt.plot(1000*freq, (4*i+1)*fft_values-400*i,alpha=0.7, label=legend_names[i],linewidth = 2, color = colors[i])
    if i <5:    
        plt.plot(1000*freq, (i+1)*fft_values-400*i,alpha=0.7, label=legend_names[i],linewidth = 2, color = colors[i])
    
    plt.text(650, (1+i)-400*i+100, legend_names[i], fontsize=18,fontweight='bold',color=colors[i],ha='center', va='center')


#plt.axvline(30, color = 'k', linestyle = '--',alpha = 0.8)
plt.xlim(0,700)
plt.ylim(-2000,300)
plt.yticks([])
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.savefig('7_figures/' + 'DCLS_temp_BR_FFT' + '_plot.png', dpi=700)

plt.show()
