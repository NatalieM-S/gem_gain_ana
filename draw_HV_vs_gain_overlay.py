import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Data
x = np.array([2900, 2950, 3000, 3050, 3100, 3150])
y1 = np.array([3419.4, 5067.7, 8563.0, 12845.8, 18898.6, 29743.9]) ## Ar:CO2 = 90:10
y2 = np.array([2511.5, 3881.9, 6020.6, 9339.6, 14527.0, 22579.1]) ## Ar:CH4 = 95:5
y3 = np.array([4441.4, 6667.0, 9858.6, 14637.0, 21168.3, 30821.3]) ## Ar:Co2 = 90:10 pad chamber

# Take log10 of y
logy1 = np.log10(y1)
logy2 = np.log10(y2)
logy3 = np.log10(y3)

# Linear regression: x vs log10(y)
slope1, intercept1, r_value1, p_value1, std_err1 = linregress(x, logy1)
slope2, intercept2, r_value2, p_value2, std_err2 = linregress(x, logy2)
slope3, intercept3, r_value3, p_value3, std_err3 = linregress(x, logy3)


# Estimate intercept error from residuals
n = len(x)

residuals1 = logy1 - (slope1 * x + intercept1)
s_err1 = np.sqrt(np.sum(residuals1**2) / (n - 2))
x_mean = np.mean(x)
Sxx = np.sum((x - x_mean)**2)
intercept_err1 = s_err1 * np.sqrt(np.sum(x**2) / (n * Sxx))

residuals2 = logy2 - (slope2 * x + intercept2)
s_err2 = np.sqrt(np.sum(residuals2**2) / (n - 2))
intercept_err2 = s_err2 * np.sqrt(np.sum(x**2) / (n * Sxx))

residuals3 = logy3 - (slope3 * x + intercept3)
s_err3 = np.sqrt(np.sum(residuals3**2) / (n - 2))
intercept_err3 = s_err3 * np.sqrt(np.sum(x**2) / (n * Sxx))

# Print results with errors
#print(f"log10(Gain) = ({slope:.6f} ± {std_err:.6f}) * Voltage + ({intercept:.4f} ± {intercept_err:.4f})")
#print(f"R² = {r_value**2:.4f}")

# Fitted curve
x_draw = np.array([2900, 2950, 3000, 3050, 3100, 3150, 3200, 3250, 3300, 3350])
logy1_fit = slope1 * x_draw + intercept1
y1_fit = 10 ** logy1_fit

logy2_fit = slope2 * x_draw + intercept2
y2_fit = 10 ** logy2_fit

logy3_fit = slope3 * x_draw + intercept3
y3_fit = 10 ** logy3_fit

# Plot
plt.figure(figsize=(8, 5))
plt.plot(x, y3, 'o', label='Ar:CO2 = 90:10, Pad Chamber')
plt.plot(x_draw, y3_fit, 'b--', label=(
    f'Fit: log₁₀(G) = ({slope3:.4f}±{std_err3:.4f})·V + ({intercept3:.2f}±{intercept_err3:.2f})'
))

plt.plot(x, y1, 'o', label='Ar:CO2 = 90:10')
plt.plot(x_draw, y1_fit, 'r--', label=(
    f'Fit: log₁₀(G) = ({slope1:.4f}±{std_err1:.4f})·V + ({intercept1:.2f}±{intercept_err1:.2f})'
))
plt.plot(x, y2, 'o', label='Ar:CH4 = 95:5')
plt.plot(x_draw, y2_fit, 'g--', label=( 
    f'Fit: log₁₀(G) = ({slope2:.4f}±{std_err2:.4f})·V + ({intercept2:.2f}±{intercept_err2:.2f})'
))

plt.xlim(2800., 3500.)
plt.ylim(2000., 300000.)
plt.yscale('log')
plt.xlabel("GEM Voltage [V]")
plt.ylabel("Gain (log scale)")
plt.title("")
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("./output/gain_vs_voltage_1_atm.pdf")
#plt.show()
