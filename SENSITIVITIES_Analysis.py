import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# GLOBAL PLOT SETTINGS
# ==========================================================

plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18


# ==========================================================
# TRANSMISSION LINE
# ==========================================================

f = 50                  # Frequency (Hz)
R = 7.2                 # Series resistance (Ohm)
L = 230e-3              # Series inductance (H)

# Series reactance
X = 2 * np.pi * f * L

# Magnitude of series impedance
Z = np.sqrt(R**2 + X**2)


# ==========================================================
# LOADS
# ==========================================================

loads = np.array([750, 500, 200, 100, 75])   # Load resistance (Ohm)

Vs0 = 100               # Initial source voltage (V)
drop = 0.007            # Source voltage reduction per operating point


# ==========================================================
# STORAGE
# ==========================================================

Vs_list = []
Vr_list = []
delta_list = []
Power = []

dPdVs = []
dPdVr = []
dPdZ = []
dPdd = []


# ==========================================================
# SOLVE OPERATING POINTS
# ==========================================================

for i, RL in enumerate(loads):

    # ------------------------------------------------------
    # Source voltage regulation
    # ------------------------------------------------------
    Vs = Vs0 * (1 - drop * i)

    # ------------------------------------------------------
    # Line current
    # ------------------------------------------------------
    I = Vs / (RL + R + 1j * X)

    # ------------------------------------------------------
    # Receiving-end voltage
    # ------------------------------------------------------
    Vr = I * RL
    Vr_mag = np.abs(Vr)

    # ------------------------------------------------------
    # Power-angle difference
    # ------------------------------------------------------
    delta = np.angle(Vs + 0j) - np.angle(Vr)

    # ------------------------------------------------------
    # Active power
    # P = Vs * Vr / Z * sin(delta)
    # ------------------------------------------------------
    P = (Vs * Vr_mag / Z) * np.sin(delta)

    # ------------------------------------------------------
    # Sensitivities
    # ------------------------------------------------------

    # dP/dVs
    s1 = (Vr_mag / Z) * np.sin(delta)

    # dP/dVr
    s2 = (Vs / Z) * np.sin(delta)

    # dP/dZ
    s3 = -(Vs * Vr_mag / Z**2) * np.sin(delta)

    # dP/ddelta
    s4 = (Vs * Vr_mag / Z) * np.cos(delta)

    # ------------------------------------------------------
    # Store results
    # ------------------------------------------------------
    Vs_list.append(Vs)
    Vr_list.append(Vr_mag)
    delta_list.append(np.degrees(delta))
    Power.append(P)

    dPdVs.append(s1)
    dPdVr.append(s2)
    dPdZ.append(s3)
    dPdd.append(s4)


# ==========================================================
# CONVERT TO NUMPY ARRAYS
# ==========================================================

Vs_list = np.array(Vs_list)
Vr_list = np.array(Vr_list)
delta_list = np.array(delta_list)
Power = np.array(Power)

dPdVs = np.array(dPdVs)
dPdVr = np.array(dPdVr)
dPdZ = np.array(dPdZ)
dPdd = np.array(dPdd)


# ==========================================================
# CONVERT dP/ddelta FROM W/rad TO W/degree
# ==========================================================

dPdd_deg = dPdd * (np.pi / 180)


# ==========================================================
# PLOT 1:
# dP/dVs, dP/dVr, and dP/ddelta
# ==========================================================

fig1, ax1 = plt.subplots(figsize=(9, 6))

# ----------------------------------------------------------
# Left y-axis: Voltage sensitivities
# ----------------------------------------------------------

line1, = ax1.plot(
    loads,
    dPdVs,
    'o-',
    linewidth=2,
    markersize=8,
    label=r'$\partial P/\partial V_s$',
    color='blue'
)

line2, = ax1.plot(
    loads,
    dPdVr,
    's-',
    linewidth=2,
    markersize=8,
    label=r'$\partial P/\partial V_r$',
    color='red'
)

# Reverse load axis
ax1.invert_xaxis()

# Grid
ax1.grid(True, alpha=0.3)

# ----------------------------------------------------------
# Axis labels
# ----------------------------------------------------------

ax1.set_xlabel(
    "Load Resistance (Ω)",
    fontsize=18,
    fontweight='bold'
)

ax1.set_ylabel(
    "W/V",
    fontsize=18,
    fontweight='bold'
)

# ----------------------------------------------------------
# Tick formatting
# ----------------------------------------------------------

ax1.tick_params(
    axis='both',
    labelsize=18,
    width=2,
    length=6
)

for label in ax1.get_xticklabels():
    label.set_fontweight('bold')

for label in ax1.get_yticklabels():
    label.set_fontweight('bold')

# Custom x-axis ticks
ax1.set_xticks([750, 500, 200, 75])


# ==========================================================
# RIGHT Y-AXIS:
# dP/ddelta
# ==========================================================

ax2 = ax1.twinx()

line3, = ax2.plot(
    loads,
    dPdd_deg,
    'd-',
    linewidth=2,
    markersize=8,
    label=r'$\partial P/\partial \delta$ (W/°)',
    color='green'
)

ax2.set_ylabel(
    "W/°",
    fontsize=18,
    fontweight='bold'
)

ax2.tick_params(
    axis='y',
    labelsize=18,
    width=2,
    length=6
)

for label in ax2.get_yticklabels():
    label.set_fontweight('bold')


# ==========================================================
# COMBINED LEGEND
# ==========================================================

lines = [line1, line2, line3]

labels = [
    r'$\partial P/\partial V_s$',
    r'$\partial P/\partial V_r$',
    r'$\partial P/\partial \delta$ (W/°)'
]

legend = ax1.legend(
    lines,
    labels,
    fontsize=16,
    loc='center left'
)

# Bold legend text
for text in legend.get_texts():
    text.set_fontweight('bold')

# Bold legend frame
legend.get_frame().set_linewidth(1.5)


# ==========================================================
# FINALIZE PLOT 1
# ==========================================================

plt.tight_layout()

plt.savefig(
    'voltage_angle_sensitivities.pdf',
    dpi=300,
    bbox_inches='tight'
)

plt.show()


# ==========================================================
# PLOT 2:
# dP/dZ
# ==========================================================

fig2, ax3 = plt.subplots(figsize=(9, 6))

line4, = ax3.plot(
    loads,
    dPdZ,
    '^-',
    linewidth=2,
    markersize=10,
    label=r'$\partial P/\partial Z$',
    color='purple'
)

# Reverse load axis
ax3.invert_xaxis()

# Grid
ax3.grid(True, alpha=0.3)

# ----------------------------------------------------------
# Axis labels
# ----------------------------------------------------------

ax3.set_xlabel(
    "Load Resistance (Ω)",
    fontsize=18,
    fontweight='bold'
)

ax3.set_ylabel(
    "W/Ω",
    fontsize=18,
    fontweight='bold'
)

# ----------------------------------------------------------
# Tick formatting
# ----------------------------------------------------------

ax3.tick_params(
    axis='both',
    labelsize=18,
    width=2,
    length=6
)

for label in ax3.get_xticklabels():
    label.set_fontweight('bold')

for label in ax3.get_yticklabels():
    label.set_fontweight('bold')

# Custom x-axis ticks
ax3.set_xticks([750, 500, 200, 75])


# ==========================================================
# LEGEND
# ==========================================================

legend2 = ax3.legend(
    fontsize=16,
    loc='best'
)

for text in legend2.get_texts():
    text.set_fontweight('bold')

legend2.get_frame().set_linewidth(1.5)


# ==========================================================
# FINALIZE PLOT 2
# ==========================================================

plt.tight_layout()

plt.savefig(
    'impedance_sensitivity.pdf',
    dpi=300,
    bbox_inches='tight'
)

plt.show()


# ==========================================================
# PRINT RESULTS
# ==========================================================

print("\nSensitivity Matrix\n")

print(
    f"{'Load (Ω)':>10}"
    f"{'dP/dVs (W/V)':>16}"
    f"{'dP/dVr (W/V)':>16}"
    f"{'dP/dZ (W/Ω)':>16}"
    f"{'dP/dδ (W/°)':>16}"
)

print("-" * 75)

for i in range(len(loads)):

    print(
        f"{loads[i]:10.0f}"
        f"{dPdVs[i]:16.4f}"
        f"{dPdVr[i]:16.4f}"
        f"{dPdZ[i]:16.4f}"
        f"{dPdd_deg[i]:16.4f}"
    )

print("\n" + "-" * 75)

print("\nTransmission-line parameters:")
print(f"Frequency, f       = {f:.1f} Hz")
print(f"Resistance, R      = {R:.2f} Ω")
print(f"Inductance, L      = {L:.3f} H")
print(f"Reactance, X       = {X:.4f} Ω")
print(f"Impedance, |Z|     = {Z:.4f} Ω")

print("\nFiles saved:")
print("  - voltage_angle_sensitivities.pdf")
print("  - impedance_sensitivity.pdf")
