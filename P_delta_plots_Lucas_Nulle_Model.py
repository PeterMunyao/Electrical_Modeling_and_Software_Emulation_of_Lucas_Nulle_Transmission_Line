import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# =====================================================
# STEP 1: PLOTTING STYLE (Garamond, as specified)
# =====================================================
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Garamond']
rcParams['font.size'] = 20
rcParams['font.weight'] = 'bold'
rcParams['axes.labelsize'] = 22
rcParams['axes.titlesize'] = 18
rcParams['xtick.labelsize'] = 20
rcParams['ytick.labelsize'] = 20
rcParams['legend.fontsize'] = 14

# -----------------------
# Parameters
# -----------------------
Vs = 101
Vr = 90

R = 7.2
X = 72.26

kappa = 0.828

# -----------------------
# Different compensation levels to test
# -----------------------
Xc_ratios = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]   # max is 0.7

# -----------------------
# Delta range
# -----------------------
delta_deg = np.linspace(0, 180, 1000)
delta = np.radians(delta_deg)

# -----------------------
# Create figure
# -----------------------
plt.figure(figsize=(9.2, 7))

# -----------------------
# Calculate and plot for each compensation ratio
# -----------------------
for Xc_ratio in Xc_ratios:
    # Compensation level (0 = no compensation, 1 = full series compensation)
    Xc = Xc_ratio * X
    
    # Effective impedance
    X_eff = X - Xc
    Zmag = np.sqrt(R**2 + X_eff**2)
    theta_eff = np.arctan2(X_eff, R)
    
    # Stiffness P(δ)
    P = kappa * (
        (Vs * Vr / Zmag) * np.cos(delta - theta_eff)
        - (Vr**2 / Zmag) * np.cos(theta_eff)
    )
    
    # Plot with label showing compensation ratio
    plt.plot(delta_deg, P, label=f"Xc/X = {Xc_ratio:.1f}", linewidth=2.4)

# -----------------------
# Formatting
# -----------------------
plt.axhline(0, color='black', linewidth=1, linestyle='--')
plt.axvline(90, color='gray', linewidth=0.8, linestyle=':', alpha=0.5)

plt.xlabel("Load angle δ (degrees)")
plt.ylabel("Power P (W)")
#plt.title("P–δ Curves with Series Compensation")

plt.grid(True, alpha=0.1)
plt.legend(loc='best')
plt.xlim(0, 180)
plt.tight_layout()

# -----------------------
# Save as PDF
# -----------------------
plt.savefig('P_delta_curves_series_compensation.pdf', format='pdf', dpi=300, bbox_inches='tight')

# -----------------------
# Display the plot
# -----------------------
plt.show()


#------------------------------------------------------------------------
#------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# =====================================================
# STEP 1: PLOTTING STYLE (Garamond, as specified)
# =====================================================
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Garamond']
rcParams['font.size'] = 20
rcParams['font.weight'] = 'bold'
rcParams['axes.labelsize'] = 22
rcParams['axes.titlesize'] = 18
rcParams['xtick.labelsize'] = 20
rcParams['ytick.labelsize'] = 20
rcParams['legend.fontsize'] = 14

# -----------------------
# Parameters
# -----------------------
Vs = 101
Vr = 90

R = 7.2
X = 72.26

kappa = 1.0  # Grounding stiffness factor (1.0 = no stiffness reduction)

# -----------------------
# Different compensation levels to test
# -----------------------
Xc_ratios = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]   # max is 0.7

# -----------------------
# Delta range
# -----------------------
delta_deg = np.linspace(0, 180, 1000)
delta = np.radians(delta_deg)

# -----------------------
# Create figure
# -----------------------
plt.figure(figsize=(9.2, 7))

# -----------------------
# Calculate and plot for each compensation ratio
# -----------------------
for Xc_ratio in Xc_ratios:
    # Compensation level (0 = no compensation, 1 = full series compensation)
    Xc = Xc_ratio * X
    
    # Effective impedance
    X_eff = X - Xc
    Zmag = np.sqrt(R**2 + X_eff**2)
    theta_eff = np.arctan2(X_eff, R)
    
    # WITHOUT grounding impedance term (only series impedance)
    
    P_no_grounding = kappa * (
        (Vs * Vr / Zmag) * np.cos(delta - theta_eff)
        - (Vr**2 / Zmag) * np.cos(theta_eff)
    )
    
    # Choose which one to plot
    P = P_no_grounding  # Change to P_with_grounding for version with grounding term
    
    # Plot with label showing compensation ratio
    plt.plot(delta_deg, P, label=f"Xc/X = {Xc_ratio:.1f}", linewidth=2.4)

# -----------------------
# Formatting
# -----------------------
plt.axhline(0, color='black', linewidth=1, linestyle='--')
plt.axvline(90, color='gray', linewidth=0.8, linestyle=':', alpha=0.5)

plt.xlabel("Load angle δ (degrees)")
plt.ylabel("Power P (W)")

plt.grid(True, alpha=0.1)
plt.legend(loc='best')
plt.xlim(0, 180)
plt.tight_layout()

# -----------------------
# Save as PDF
# -----------------------
plt.savefig('P_delta_curves_series_compensation_NO_SERIES_RESISTANCE_11.pdf', format='pdf', dpi=300, bbox_inches='tight')

# -----------------------
# Display the plot
# -----------------------
plt.show()

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# =====================================================
# STEP 1: PLOTTING STYLE (Garamond, as specified)
# =====================================================
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Garamond']
rcParams['font.size'] = 20
rcParams['font.weight'] = 'bold'
rcParams['axes.labelsize'] = 22
rcParams['axes.titlesize'] = 18
rcParams['xtick.labelsize'] = 20
rcParams['ytick.labelsize'] = 20
rcParams['legend.fontsize'] = 13

# -----------------------
# Parameters
# -----------------------
Vs = 101
Vr = 98

R = 0  # Set R = 0 for purely reactive line
X = 72.26

kappa = 1.0  # Changed from 0.828 to 1.0 (no grounding effects)

# -----------------------
# Different compensation levels to test
# -----------------------
Xc_ratios = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

# -----------------------
# Delta range
# -----------------------
delta_deg = np.linspace(0, 180, 1000)
delta = np.radians(delta_deg)

# -----------------------
# Create figure
# -----------------------
plt.figure(figsize=(9.3, 7))

# -----------------------
# Calculate and plot for each compensation ratio
# -----------------------
for Xc_ratio in Xc_ratios:
    Xc = Xc_ratio * X
    X_eff = X - Xc
    
    Zmag = np.abs(X_eff)
    P = kappa * (Vs * Vr / Zmag) * np.sin(delta)
    
    if X_eff < 0:
        P = -P
    
    plt.plot(delta_deg, P, label=f"Xc/X = {Xc_ratio:.1f}", linewidth=2.5)

# -----------------------
# Formatting
# -----------------------
plt.axhline(0, color='black', linewidth=1, linestyle='--')
plt.axvline(90, color='gray', linewidth=0.8, linestyle=':', alpha=0.4)

plt.xlabel("Load angle δ (degrees)")
plt.ylabel("Power P (W)")

plt.grid(True, alpha=0.1)
plt.legend(loc='best')
plt.xlim(0, 180)
plt.tight_layout()

# -----------------------
# Save as PDF
# -----------------------
plt.savefig('P_delta_curves_reactive_line_series_compensation_00.pdf', format='pdf', dpi=300, bbox_inches='tight')

# -----------------------
# Display the plot
# -----------------------
plt.show()

