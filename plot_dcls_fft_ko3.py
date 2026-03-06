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
    
    if i ==0:
        df['ABC_wma'] = np.interp(new_time, df["#Time"], df["ABC_wma"])
    else:    
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
custom_cmap = LinearSegmentedColormap.from_list("green_black", ["green", "black"])
# Generate values from 0 to 1 (for color transitions)
values = np.linspace(0, 1, 210)

# Extract the corresponding RGB colors from the custom colormap
colors = [custom_cmap(val) for val in values]
# Extract the corresponding RGB colors from the custom colormap

filenames = ['briggs_rauscher_run9_700c_0_5e_86p_1a_0i_DCLS',
             'briggs_rauscher_run7_3_700c_0_5e_86p_1a_0i_DCLS',
             'briggs_rauscher_run8_700c_0_5e_86p_1a_0i_DCLS',
             'briggs_rauscher_run1_700c_0_5e_86p_1a_0i_DCLS',]
#'briggs_rauscher_run9_700c_0_5e_86p_1a_0i_DCLS'
colors = [colors[47],colors[70],colors[94],colors[200]]

plt.figure(figsize=(15, 15))

legend_names = ['47mM','70mM','94mM','200mM']

time_lims = [(34.9, 1200), (736.9, 1245.7), (104.7,1109.6), (39.3,540.8)]
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
   

    if i ==0:
        intensity = df_filtered['ABC_wma'].values
    else:
        intensity = df_filtered['penta_wma'].values
    #print(intensity)
    # print(time)

    freq, fft_values = apply_fourier_transform(time, intensity)
    if i == 0:
        plt.plot(1000*freq, 10*fft_values-400*i,alpha=0.7, label=legend_names[i],linewidth = 2, color = colors[i])
    if i == 1:
        plt.plot(1000*freq, 5*fft_values-400*i,alpha=0.7, label=legend_names[i],linewidth = 2, color = colors[i])
    if i == 2:
        plt.plot(1000*freq, 2*fft_values-400*i,alpha=0.7, label=legend_names[i],linewidth = 2, color = colors[i])
    if i == 3:
        plt.plot(1000*freq, 3.5*fft_values-400*i,alpha=0.7, label=legend_names[i],linewidth = 2, color = colors[i])

    #else:    
    #    plt.plot(1000*freq, 2*fft_values-400*i,alpha=0.7, label=legend_names[i],linewidth = 2, color = colors[i])
    
    plt.text(380, (1+i)-400*i+100, legend_names[i], fontsize=18,fontweight='bold',color=colors[i],ha='right', va='center')


#plt.axvline(30, color = 'k', linestyle = '--',alpha = 0.8)
plt.xlim(0,400)
plt.ylim(-1200,300)
plt.yticks([])
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.savefig('7_figures/' + 'DCLS_ko3_BR_FFT' + '_plot.png', dpi=700)

plt.show()
