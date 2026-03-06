import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import matplotlib.colors as mcolors
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

plt.figure(figsize=(15, 10))

legend_names = ['5°C','13°C','17°C','22°C','29°C','43°C']


for i in range(len(filenames)):
    filename = filenames[i]

    if filename == '' :
        sys.exit()
    file_path = '2_datasets/' + str(filename) + '.csv'

    df = pd.read_csv(file_path)

    time_s = df['#Time']

    product = df['penta']
    product_smo = df['penta_wma']

    plt.plot(time_s, 0.8*product_smo-i,alpha=0.7, label=legend_names[i],linewidth = 2.5, color = colors[i])
    plt.plot(time_s, 0.8*product-i, alpha=0.1, color=colors[i])
    plt.text(time_s.iloc[-1], -i+0.2, legend_names[i], fontsize=15,fontweight='bold',color=colors[i],ha='center', va='center')






plt.axvline(30, color = 'k', linestyle = '--',alpha = 0.8)
plt.xlabel('Time Elapsed (s)', fontsize = 20,labelpad=15)
plt.ylabel('Spectral Contribution (a.u.)', fontsize = 20,labelpad=15)
#plt.legend(fontsize = 20)
plt.yticks([])
#plt.xlim(0,200)
plt.xticks(fontsize = 15)

plt.savefig('7_figures/' + 'DCLS_temp_BR' + '_plot.png', dpi=700)



plt.ylim(-5.13,-4.1)
plt.plot(time_s, 0.8*product_smo-i,alpha=0.7, label=legend_names[i],linewidth = 5, color = colors[i])
plt.plot(time_s, 0.8*product-i, alpha=0.1, color=colors[i])
plt.xticks(fontsize = 30)
plt.xlim(30,140)
plt.savefig('7_figures/' + 'DCLS_temp_BR_zoomed' + '_plot.png', dpi=700)

