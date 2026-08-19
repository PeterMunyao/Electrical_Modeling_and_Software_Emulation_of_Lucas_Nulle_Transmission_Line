import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# DATA FROM DIGSILENT POWERFACTORY 2026
# Lucas Nulle Line Representation
# ==========================================================

# Transmission voltage levels (kV, line-to-line)
V_ll = np.array([380, 220, 200, 132, 100, 95])

# Receiving end voltage (per unit)
Vr_pu = np.array([1.04, 1.03, 1.03, 0.99, 0.86, 0.79])

# Voltage angle (degrees)
delta = np.array([-1.8, -4.8, -5.8, -13.6, -27.6, -34.1])

# Power and current data
P = np.array([55.6, 55.6, 55.6, 55.3, 57.9, 58.9])  # MW
Q = np.array([-181.8, -55.3, -43.5, -6.3, 20.5, 31.9])  # MVAR
I = np.array([0.289, 0.206, 0.204, 0.248, 0.355, 0.407])  # kA

# ==========================================================
# CREATE THE PLOT - Transmission Voltage on X-axis
# ==========================================================

fig, ax1 = plt.subplots(figsize=(10.5, 8.2))

# --- Primary plot: Vr (pu) vs. Transmission Voltage ---
ax1.plot(V_ll, Vr_pu, 'bo-', linewidth=2.5, markersize=10, 
         markerfacecolor='white', markeredgewidth=2.5,
         label='Vr (Receiving End Voltage)')

# Add value labels on each point (Vr values) - MODIFIED to place exactly below
for i, (v, vr) in enumerate(zip(V_ll, Vr_pu)):
    ax1.annotate(f'{vr:.2f} pu', 
                xy=(v, vr),
                xytext=(-7, -13),  # Exactly below the point (centered horizontally)
                textcoords='offset points',
                fontsize=13, fontweight='bold',
                ha='center',  # Center aligned
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.1))

# --- Secondary y-axis: Voltage Angle ---
ax2 = ax1.twinx()  # This creates a right y-axis
ax2.plot(V_ll, delta, 'rs--', linewidth=2, markersize=8, 
         markerfacecolor='white', markeredgewidth=2,
         label='δ (Voltage Angle)')

# Add angle labels - MODIFIED for 132kV point to place label BELOW
for i, (v, d) in enumerate(zip(V_ll, delta)):
    if v == 132:  # Special case for 132kV - place label below
        ax2.annotate(f'{d:.1f}°', 
                    xy=(v, d),
                    xytext=(0, -27),  # Negative y offset places it below
                    textcoords='offset points',
                    fontsize=13, fontweight='bold',
                    color='red',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='pink', alpha=0.2))
    else:
        ax2.annotate(f'{d:.1f}°', 
                    xy=(v, d),
                    xytext=(11, 7), 
                    textcoords='offset points',
                    fontsize=11, fontweight='bold',
                    color='red',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='pink', alpha=0.2))

# ==========================================================
# ANNOTATION BOX - CENTER-BOTTOM INSIDE GRAPH
# ==========================================================

# Create annotation text with all operating points
annotation_text = "DIgSILENT PowerFactory 2026\n"
annotation_text += "Lucas Nulle 300 km Line Representation\n"
annotation_text += "=" * 35 + "\n"
annotation_text += f"{'V_ll':>6} {'Vr':>8} {'δ':>8} {'P':>8} {'Q (Line)':>10} {'I':>8}\n"
annotation_text += f"{'kV':>6} {'pu':>8} {'°':>8} {'MW':>8} {'MVAR':>10} {'kA':>8}\n"
annotation_text += "-" * 35 + "\n"

for i in range(len(V_ll)):
    annotation_text += f"{V_ll[i]:6.0f} {Vr_pu[i]:8.2f} {delta[i]:8.1f} "
    annotation_text += f"{P[i]:8.1f} {Q[i]:10.1f} {I[i]:8.3f}\n"

annotation_text += "-" * 35 + "\n"
annotation_text += "Load: 55 MW + j2 MVAR"

# Add text box at center-bottom position
ax1.text(0.62, 0.057, annotation_text, 
         transform=ax1.transAxes,
         fontsize=12.7, verticalalignment='bottom', horizontalalignment='center',
         family='monospace',
         bbox=dict(boxstyle='round', facecolor='none', 
                   edgecolor='black', alpha=0.92, pad=0.8),
         zorder=100)

# ==========================================================
# ADD REFERENCE LINE FOR 1.0 PU
# ==========================================================
ax1.axhline(y=1.0, color='gray', linestyle=':', linewidth=1.5, alpha=0.7, label='1.0 pu Reference')
ax1.axvline(x=132, color='gray', linestyle=':', linewidth=1.5, alpha=0.5)

# Add shaded region for acceptable voltage range (±5%)
ax1.axhspan(0.95, 1.05, alpha=0.1, color='green', label='Acceptable Range (±5%)')

# ==========================================================
# STYLING - Dotted grid
# ==========================================================

# Main axes styling (Voltage on x-axis, Vr on y-axis)
ax1.set_xlabel('Transmission Voltage (kV, Line-to-Line)', fontsize=20, fontweight='bold')
ax1.set_ylabel('Receiving End Voltage (per unit)', fontsize=20, fontweight='bold', color='blue')
ax1.tick_params(axis='x', labelsize=19)
ax1.tick_params(axis='y', labelcolor='blue', labelsize=19)

# Secondary y-axis styling (Angle on right)
ax2.set_ylabel('Voltage Angle δ (degrees)', fontsize=18, fontweight='bold', color='red')
ax2.tick_params(axis='y', labelcolor='red', labelsize=16)

# Dotted grid lines
ax1.grid(True, which='major', linestyle=':', linewidth=0.8, alpha=0.7)
ax1.grid(True, which='minor', linestyle=':', linewidth=0.4, alpha=0.3)

# ==========================================================
# SET X-AXIS TICKS AND SKIP 95 kV LABEL
# ==========================================================

# Set x-axis ticks to show all voltage levels
ax1.set_xticks(V_ll)

# Create custom labels - skip 95 kV to avoid overcrowding
tick_labels = []
for x in V_ll:
    if x == 95:
        tick_labels.append('')  # Skip 95 kV label
    else:
        tick_labels.append(f'{int(x)}')

ax1.set_xticklabels(tick_labels, fontsize=16, fontweight='bold')

# Set axes limits
ax1.set_xlim(80, 400)
ax1.set_ylim(0.7, 1.1)
ax2.set_ylim(-40, 0)

# ==========================================================
# LEGEND - Below the plot
# ==========================================================

# Combine legends from both axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

# Place legend below the plot
ax1.legend(lines1 + lines2, labels1 + labels2, 
          loc='upper center', fontsize=17, frameon=True, 
          fancybox=True, shadow=True,
          bbox_to_anchor=(0.5, -0.12), ncol=2)

# ==========================================================
# LAYOUT
# ==========================================================

plt.tight_layout(rect=[0, 0, 1, 0.95])  # Make room for legend below

# Save as PDF
plt.savefig('lucas_nulle_transmission_voltage_vs_Vr_final.pdf', 
            format='pdf', bbox_inches='tight', dpi=300)

plt.show()

# ==========================================================
# PRINT SUMMARY TABLE
# ==========================================================

print("\n" + "="*80)
print("LUCAS NULLE LINE - DIGSILENT POWERFACTORY 2026 RESULTS")
print("="*80)
print(f"\n{'V_ll (kV)':>10} {'Vr (pu)':>10} {'δ (°)':>10} {'P (MW)':>10} {'Q (MVAR)':>12} {'I (kA)':>10}")
print("-"*80)
for i in range(len(V_ll)):
    print(f"{V_ll[i]:10.0f} {Vr_pu[i]:10.2f} {delta[i]:10.1f} "
          f"{P[i]:10.1f} {Q[i]:12.1f} {I[i]:10.3f}")

print("\n" + "="*80)
print("KEY OBSERVATIONS:")
print("="*80)
print(f"1. Maximum Vr: {Vr_pu.max():.2f} pu at {V_ll[np.argmax(Vr_pu)]} kV")
print(f"2. Minimum Vr: {Vr_pu.min():.2f} pu at {V_ll[np.argmin(Vr_pu)]} kV")
print(f"3. Voltage drop from 380kV to 95kV: {(Vr_pu[0]-Vr_pu[-1])*100:.1f}%")
print(f"4. Critical angle occurs at {V_ll[np.argmin(delta)]} kV: {delta.min():.1f}°")
print(f"5. Reactive power changes from {Q[0]:.1f} MVAR to {Q[-1]:.1f} MVAR")
print(f"6. System operates within acceptable range (0.95-1.05 pu) up to {V_ll[Vr_pu >= 0.95][-1]:.0f} kV")
print("="*80)
