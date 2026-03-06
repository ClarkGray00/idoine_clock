import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps
from scipy.stats import linregress

wav = [2832,2640,2557,2464,2361,2270,2208,2106,2011,1921,1835,1740,
       1643,1566,1484,1386,1320,1159,1073,987,904,822,703,630,573,491,
       434,323,266,211,160,110]

wav = [2640,2557,2464,2361,2270,2208,2106,2011,1921,1835,1740,
       1643,1557,1448,1386,1320,1159,1073,987,904,822,703,630,573,491,
       434,323,266]


modes = [(2*n - 1)/2 for n in range(1, len(wav)+1)]

# Fit a linear regression model
slope, intercept, r, p, stderr = linregress(modes, wav)

# Estimate where it hits x-axis (i.e., ΔE = 0)
v_max = -intercept / slope

# Create fine v-range up to v_max for area under the curve
v_dense = np.linspace(0, v_max, 500)
dE_dense = slope * v_dense + intercept

# Integrate to get dissociation energy in cm^-1
D_e = simps(dE_dense, v_dense)

# Plot
plt.figure(figsize=(8,5))
plt.plot(modes, wav, 'o', label='Observed ΔE')  # Plot original data points
plt.plot(v_dense, dE_dense, '-', label='Extrapolated linear fit')  # Plot the fitted line

# Fill the area under the curve
plt.fill_between(v_dense, dE_dense, color='skyblue', alpha=0.4)

# Plot additional details
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(v_max, color='red', linestyle='--', label=f'v_max ≈ {v_max:.2f}')

plt.xlabel('v + 1/2')
plt.ylabel('ΔE (cm⁻¹)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.xlim(0,None)
plt.ylim(0,None)

r_squared = r**2

plt.text(0.95, 0.95, f'$R^2$ = {r_squared:.4f}', transform=plt.gca().transAxes,
         verticalalignment='top', horizontalalignment='right', fontsize=12, bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3'))
plt.savefig('7_figures/' +'Birge–Sponer'+'.png', dpi=700)
# Show plot
plt.show()

print(f"Estimated dissociation energy Dₑ ≈ {D_e:.2f} cm⁻¹")

