import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ============================================================
# PROFESSIONAL GARAMOND STYLING - FONTS INCREASED BY 4 STEPS
# ============================================================
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Garamond']
rcParams['font.size'] = 26        # was 22 (+4)
rcParams['font.weight'] = 'bold'
rcParams['axes.labelsize'] = 24   # was 20 (+4)
rcParams['axes.titlesize'] = 24   # was 20 (+4)
rcParams['xtick.labelsize'] = 20  # was 16 (+4)
rcParams['ytick.labelsize'] = 20  # was 16 (+4)
rcParams['legend.fontsize'] = 16  # was 14 (+4)

# ============================================================
# DATA
# ============================================================

models = [
    'Source',
    'Measured',
    '1: Lumped\nSeries',
    '2: Nominal π',
    '3: Distributed'
]

# Sending end voltages
Vs1 = 102
Vs2 = 104
Vs3 = 100

# Receiving end voltages
Vr1 = np.array([97.0, 99.3, 103.8, 113.9])
Vr2 = np.array([98.0, 101.5, 106.1, 116.5])
Vr3 = np.array([100.0, 97.9, 102.4, 112.4])

# Spread data (only for models, not source)
spread = np.array([3.0, 3.6, 3.7, 4.1])

# Define color sequence for Vr1, Vr2, Vr3
# Using matplotlib's default color cycle
color1 = 'tab:blue'    # Vr1 color
color2 = 'tab:orange'  # Vr2 color  
color3 = 'tab:green'   # Vr3 color

# ============================================================
# FIGURE
# ============================================================

fig, ax = plt.subplots(
    2, 1,
    figsize=(10.8, 10.5),
    gridspec_kw={'height_ratios':[3, 1.5]}
)

# ============================================================
# TOP PANEL: RECEIVING-END VOLTAGES
# ============================================================

x = np.arange(len(models))

# Thin bars
w = 0.16

# Sending end voltage bars (Source) - using same colors as Vr
source_bars1 = ax[0].bar(
    x[0] - w,
    Vs1,
    width=w,
    edgecolor='black',
    linewidth=1.2,
    label=r'$V_{s1}$',
    color=color1,
    alpha=0.7
)

source_bars2 = ax[0].bar(
    x[0],
    Vs2,
    width=w,
    edgecolor='black',
    linewidth=1.2,
    label=r'$V_{s2}$',
    color=color2,
    alpha=0.7
)

source_bars3 = ax[0].bar(
    x[0] + w,
    Vs3,
    width=w,
    edgecolor='black',
    linewidth=1.2,
    label=r'$V_{s3}$',
    color=color3,
    alpha=0.7
)

# Receiving end voltage bars for all models
bars1 = ax[0].bar(
    x[1:] - w,
    Vr1,
    width=w,
    edgecolor='black',
    linewidth=1.2,
    label=r'$V_{r1}$',
    color=color1
)

bars2 = ax[0].bar(
    x[1:],
    Vr2,
    width=w,
    edgecolor='black',
    linewidth=1.2,
    label=r'$V_{r2}$',
    color=color2
)

bars3 = ax[0].bar(
    x[1:] + w,
    Vr3,
    width=w,
    edgecolor='black',
    linewidth=1.2,
    label=r'$V_{r3}$',
    color=color3
)

# Value labels for source bars
for b in [source_bars1, source_bars2, source_bars3]:
    for bar in b:
        ax[0].text(
            bar.get_x()+bar.get_width()/2,
            bar.get_height()+0.6,
            f'{bar.get_height():.1f}',
            ha='center',
            va='bottom',
            fontsize=17,
            rotation=90
        )

# Value labels for receiving end bars
for bars in [bars1, bars2, bars3]:
    for b in bars:
        ax[0].text(
            b.get_x()+b.get_width()/2,
            b.get_height()+0.6,
            f'{b.get_height():.1f}',
            ha='center',
            va='bottom',
            fontsize=17,
            rotation=90
        )

ax[0].set_ylabel('Voltage (V)', fontweight='bold')
ax[0].set_xticks(x)
ax[0].set_xticklabels(models)

ax[0].grid(
    True,
    alpha=0.25,
    linestyle='-',
    linewidth=0.5
)

# Adjust y-axis height for top panel
ax[0].set_ylim(90, 120)

# ============================================================
# BOTTOM PANEL: VOLTAGE SPREAD - BROWN BARS
# ============================================================

# Only for Measured and models (excluding Source)
x_bottom = np.arange(len(models)-1)  # Skip Source

bars = ax[1].bar(
    x_bottom,
    spread,
    width=0.12,
    color='#8B4513',      # Brown color (SaddleBrown)
    edgecolor='black',
    linewidth=1.2
)

# Value labels
for b in bars:
    ax[1].text(
        b.get_x()+b.get_width()/2,
        b.get_height()+0.05,
        f'{b.get_height():.1f}',
        ha='center',
        va='bottom',
        fontsize=18
    )

ax[1].set_ylabel('Spread (V)', fontweight='bold')
ax[1].set_xticks(x_bottom)
ax[1].set_xticklabels(models[1:])  # Measured, A, B, C

ax[1].grid(
    True,
    alpha=0.25,
    linestyle='-',
    linewidth=0.5
)

# Adjust y-axis height for bottom panel
ax[1].set_ylim(0, 5.5)

# ============================================================
# LEGEND BELOW BOTH GRAPHS
# ============================================================

# Create custom legend handles that show the colors properly
from matplotlib.patches import Patch

legend_elements = [
    Patch(facecolor=color1, edgecolor='black', label=r'$V_{s1}$ / $V_{r1}$', alpha=0.7),
    Patch(facecolor=color2, edgecolor='black', label=r'$V_{s2}$ / $V_{r2}$', alpha=0.7),
    Patch(facecolor=color3, edgecolor='black', label=r'$V_{s3}$ / $V_{r3}$', alpha=0.7)
]

fig.legend(
    handles=legend_elements,
    loc='lower center',
    bbox_to_anchor=(0.5, -0.007),
    ncol=3,
    framealpha=0.9,
    edgecolor='black',
    fancybox=False,
    shadow=False
)

# ============================================================
# FORMAT
# ============================================================

for a in ax:
    a.tick_params(
        axis='both',
        which='major',
        width=1.2
    )

plt.tight_layout()
plt.subplots_adjust(bottom=0.12)

plt.savefig(
    'voltage_model_comparison.pdf',
    format='pdf',
    dpi=300,
    bbox_inches='tight',
    facecolor='white'
)

plt.show()


#-----------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Patch
from matplotlib.colors import to_rgb

# ============================================================
# PROFESSIONAL GARAMOND STYLING - ALL FONTS INCREASED BY 5 STEPS
# ============================================================
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Garamond']
rcParams['font.size'] = 31                    # was 26 (+5)
rcParams['font.weight'] = 'bold'
rcParams['axes.labelsize'] = 29               # was 24 (+5)
rcParams['axes.titlesize'] = 29               # was 24 (+5)
rcParams['xtick.labelsize'] = 23              # was 18 (+5)
rcParams['ytick.labelsize'] = 25              # was 20 (+5)
rcParams['legend.fontsize'] = 22              # was 17 (+5)

# ============================================================
# DATA
# ============================================================

loads = ['750 Ohm', '200 Ohm', '100 Ohm']
models = ['Voltage Sending End', 'Measured (Voltage Receiving End)', 'Lumped Model (Voltage Receiving End)', 'Nominal pi Model (Voltage Receiving End)', 'Distributed Model (Voltage Receiving End)']
phases = ['Phase 1', 'Phase 2', 'Phase 3']

# Source voltages (Vs1, Vs2, Vs3) per load
source_data = {
    '750 Ohm': [102, 104, 100],
    '200 Ohm': [101, 102, 98],
    '100 Ohm': [99, 101, 97]
}

# Receiving end voltages (Vr1, Vr2, Vr3) per load
vr_data = {
    '750 Ohm': {
        'Measured (Voltage Receiving End)': [101, 102, 105],
        'Lumped Model (Voltage Receiving End)': [100, 103, 99],
        'Nominal pi Model (Voltage Receiving End)': [105, 107, 104],
        'Distributed Model (Voltage Receiving End)': [115, 118, 114]
    },
    '200 Ohm': {
        'Measured (Voltage Receiving End)': [87, 88, 91],
        'Lumped Model (Voltage Receiving End)': [92, 94, 90],
        'Nominal pi Model (Voltage Receiving End)': [95, 97, 93],
        'Distributed Model (Voltage Receiving End)': [104, 106, 102]
    },
    '100 Ohm': {
        'Measured (Voltage Receiving End)': [76, 75, 78],
        'Lumped Model (Voltage Receiving End)': [77, 79, 76],
        'Nominal pi Model (Voltage Receiving End)': [79, 81, 78],
        'Distributed Model (Voltage Receiving End)': [85, 87, 84]
    }
}

# Base colors for each model
model_colors = {
    'Voltage Sending End':'#FF0000',                                          # Red
    'Measured (Voltage Receiving End)': '#000000',                             # Black
    'Lumped Model (Voltage Receiving End)': '#1f77b4',                         # Blue
    'Nominal pi Model (Voltage Receiving End)': '#ff7f0e',                     # Orange
    'Distributed Model (Voltage Receiving End)': '#2ca02c'                     # Green
}

# Phase shades (left to right: Phase 1 lightest, Phase 3 darkest)
phase_alpha = {
    'Phase 1': 1.0,    # Lightest
    'Phase 2': 0.65,   # Medium
    'Phase 3': 0.25     # Darkest
}

# ============================================================
# CREATE PLOT
# ============================================================

fig, ax = plt.subplots(figsize=(15, 8))

# Bar settings
bar_width = 0.105
phase_spacing = bar_width * 1.1
model_spacing = phase_spacing * 3.5
load_spacing = model_spacing * 5.5

x_pos = 0
load_centers = []

for load_idx, load in enumerate(loads):
    load_center = x_pos + (len(models) * model_spacing) / 2
    load_centers.append(load_center)
    
    for model_idx, model in enumerate(models):
        model_x = x_pos + model_idx * model_spacing
        
        for phase_idx, phase in enumerate(phases):
            # Get value based on model type
            if model == 'Voltage Sending End':
                value = source_data[load][phase_idx]
            else:
                value = vr_data[load][model][phase_idx]
            
            bar_x = model_x + phase_idx * phase_spacing
            
            # Apply color and shade - FIXED SECTION
            if model == 'Measured (Voltage Receiving End)':
                # Grayscale for Measured only
                gray_val = 0.3 + phase_idx * 0.15
                bar_color = (gray_val, gray_val, gray_val)
            else:
                # Use colored version with phase shading for all other models
                rgb = to_rgb(model_colors[model])
                bar_color = tuple(c * phase_alpha[phase] for c in rgb)
            
            bar = ax.bar(bar_x, value, width=bar_width, 
                        color=bar_color, edgecolor='black', linewidth=0.6)
            
            # Annotate all bars
            offset = 1.0 if value < 100 else 1.5
            ax.text(bar_x, value + offset, f'{value}', 
                   ha='center', va='bottom', fontsize=21, 
                   rotation=89, fontweight='bold')
    
    x_pos += load_spacing

# Customization
ax.set_xticks(load_centers)
ax.set_xticklabels(loads, fontweight='bold')
ax.set_ylabel('Voltage (V)', fontweight='bold')
ax.set_xlabel('Load Resistance', fontweight='bold')

ax.grid(True, alpha=0.25, linestyle='-', linewidth=0.5, axis='y')
ax.set_ylim(65, 125)

# ============================================================
# LEGEND - Below the graph with simplified phase text
# ============================================================

legend_elements = []
for model in models:
    legend_elements.append(Patch(facecolor=model_colors[model], 
                                  edgecolor='black',
                                  label=model,
                                  alpha=0.7))

# Place legend below the graph with 6 columns
ax.legend(handles=legend_elements, loc='upper center', 
          bbox_to_anchor=(0.5, -0.12),
          framealpha=0.95, edgecolor='black', fancybox=False, 
          ncol=2, handlelength=2, fontsize=21)

plt.tight_layout()
plt.subplots_adjust(bottom=0.18)
plt.savefig('complete_voltage_comparison.pdf', format='pdf', dpi=300, 
            bbox_inches='tight', facecolor='white')
plt.show()

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ============================================================
# PROFESSIONAL GARAMOND STYLING (INCREASED FONT SIZES +5)
# ============================================================
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Garamond']
rcParams['font.size'] = 36  # Was 31 (+5)
rcParams['font.weight'] = 'bold'
rcParams['axes.labelsize'] = 34  # Was 29 (+5)
rcParams['axes.titlesize'] = 34  # Was 29 (+5)
rcParams['xtick.labelsize'] = 28  # Was 23 (+5)
rcParams['ytick.labelsize'] = 30  # Was 25 (+5)
rcParams['legend.fontsize'] = 27  # Was 22 (+5)

# ============================================================
# DATA FROM CALCULATIONS
# ============================================================

inductance_values = [1.2, 2.0, 2.8]  # H
reactance_values = [377.0, 628.3, 879.6]  # Ohm (wL)

# Supply voltages (fixed for all tests)
supply_voltages = [101, 102, 99]  # Vs1, Vs2, Vs3
supply_mean = np.mean(supply_voltages)

# Measured voltages [Vr1, Vr2, Vr3] for each test
measured_data = {
    1.2: [81, 82, 83],
    2.0: [87, 88, 89],
    2.8: [91, 92, 93]
}

# Model 1 (Lumped Series, A=1)
model_1_data = {
    1.2: [83.8, 84.9, 82.5],
    2.0: [89.5, 90.6, 88.0],
    2.8: [92.2, 93.4, 90.6]
}

# Model 2 (Nominal pi, A=0.954) 
model_2_data = {
    1.2: [87.2, 88.4, 85.7],
    2.0: [93.3, 94.5, 91.7],
    2.8: [96.1, 97.4, 94.5]
}

# Model 3 (Distributed/Telegrapher's, A=0.8667)
model_3_data = {
    1.2: [95.0, 96.3, 93.5],
    2.0: [101.9, 103.3, 100.2],
    2.8: [105.2, 106.6, 103.4]
}

# Error analysis
errors = {
    'Model 1': [2.3, 2.7, 1.0],
    'Model 2': [5.7, 6.7, 4.7],
    'Model 3': [13.7, 14.7, 14.3]
}
avg_errors = {'Model 1': 2.0, 'Model 2': 5.7, 'Model 3': 14.2}

# ============================================================
# CREATE SEPARATE PLOTS - ONE FOR EACH INDUCTOR VALUE
# ============================================================

phases = ['Phase 1', 'Phase 2', 'Phase 3']
x_pos = np.arange(len(phases))
bar_width = 0.13

# Colors
colors = {
    'Supply': '#9467bd',
    'Measured': '#000000',
    'Model 1': '#1f77b4',
    'Model 2': '#ff7f0e',
    'Model 3': '#2ca02c'
}

# Offset positions for each model
offsets = {
    'Supply': -2*bar_width,
    'Measured': -bar_width,
    'Model 1': 0,
    'Model 2': bar_width,
    'Model 3': 2*bar_width
}

# Create individual plots for each test
for idx, L in enumerate(inductance_values):
    fig, ax = plt.subplots(figsize=(14, 9))  # Increased height for legend below
    
    # Get data for this inductance
    measured = measured_data[L]
    model_1 = model_1_data[L]
    model_2 = model_2_data[L]
    model_3 = model_3_data[L]
    
    # Plot supply voltage (as reference bars)
    supply_bars = ax.bar(x_pos + offsets['Supply'], supply_voltages, bar_width,
                         label=f'Supply (Vs)', color=colors['Supply'], 
                         edgecolor='black', alpha=0.7, hatch='//')
    
    # Plot measured data
    measured_bars = ax.bar(x_pos + offsets['Measured'], measured, bar_width,
                           label='Measured (Vr)', color=colors['Measured'], 
                           edgecolor='black', alpha=0.9)
    
    # Plot Model 1 (with reactance in legend)
    model_1_bars = ax.bar(x_pos + offsets['Model 1'], model_1, bar_width,
                          label=f'Model 1: Lumped Series (A=1, XL={reactance_values[idx]:.1f} Ohm)', 
                          color=colors['Model 1'], edgecolor='black', alpha=0.9)
    
    # Plot Model 2 (with reactance in legend)
    model_2_bars = ax.bar(x_pos + offsets['Model 2'], model_2, bar_width,
                          label=f'Model 2: Nominal pi (A=0.954, XL={reactance_values[idx]:.1f} Ohm)', 
                          color=colors['Model 2'], edgecolor='black', alpha=0.9)
    
    # Plot Model 3 (with reactance in legend)
    model_3_bars = ax.bar(x_pos + offsets['Model 3'], model_3, bar_width,
                          label=f'Model 3: Distributed (A=0.8667, XL={reactance_values[idx]:.1f} Ohm)', 
                          color=colors['Model 3'], edgecolor='black', alpha=0.9)
    
    # Add value labels on top of bars
    for i in range(len(phases)):
        # Supply labels
        ax.text(x_pos[i] + offsets['Supply'], supply_voltages[i] + 1.0, f'{supply_voltages[i]:.1f}',
               ha='center', va='bottom', fontsize=20, fontweight='bold')
        
        # Measured labels
        ax.text(x_pos[i] + offsets['Measured'], measured[i] + 1.0, f'{measured[i]:.1f}',
               ha='center', va='bottom', fontsize=20, fontweight='bold')
        
        # Model 1 labels
        ax.text(x_pos[i] + offsets['Model 1'], model_1[i] + 1.0, f'{model_1[i]:.1f}',
               ha='center', va='bottom', fontsize=20, fontweight='bold')
        
        # Model 2 labels
        ax.text(x_pos[i] + offsets['Model 2'], model_2[i] + 1.0, f'{model_2[i]:.1f}',
               ha='center', va='bottom', fontsize=20, fontweight='bold')
        
        # Model 3 labels
        ax.text(x_pos[i] + offsets['Model 3'], model_3[i] + 1.0, f'{model_3[i]:.1f}',
               ha='center', va='bottom', fontsize=20, fontweight='bold')
    
    # Customize axes (no title)
    ax.set_xlabel('Phase', fontweight='bold', fontsize=34)
    ax.set_ylabel('Voltage (V)', fontweight='bold', fontsize=34)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(phases, fontsize=28)
    ax.set_ylim(70, 115)
    ax.grid(True, alpha=0.25, linestyle='-', linewidth=0.5, axis='y')
    
    # Add inductance and reactance information as text annotation (instead of title)
    info_text = f'L = {L} H  |  XL = {reactance_values[idx]:.1f} Ohm  |  R_load = 750 Ohm || L'
    ax.text(0.5, 0.98, info_text, transform=ax.transAxes, fontsize=22,
            verticalalignment='top', horizontalalignment='center',
            fontweight='bold', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))
    
    # Add error annotation (font size increased by 1.5 points from original 16 to 17.5)
    error_text = f"Model 1 Error: {errors['Model 1'][idx]:.1f} V\nModel 2 Error: {errors['Model 2'][idx]:.1f} V\nModel 3 Error: {errors['Model 3'][idx]:.1f} V"
    ax.text(0.85, 0.904, error_text, transform=ax.transAxes, fontsize=20,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Add legend with col=1 (single column)
    legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12),
                      ncol=1, framealpha=0.95, edgecolor='black', 
                      fancybox=False, fontsize=22)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)  # Make room for legend below
    
    # Save each plot as a separate PDF
    filename = f'inductive_load_test_{idx+1}_L_{L}H_XL_{reactance_values[idx]:.0f}ohm.pdf'
    plt.savefig(filename, format='pdf', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print(f"Saved: {filename}")

# ============================================================
# PRINT SUMMARY STATISTICS
# ============================================================

print("=" * 80)
print("INDUCTIVE LOAD TEST SUMMARY")
print("=" * 80)
print(f"\nSupply Voltages: Vs1={supply_voltages[0]}V, Vs2={supply_voltages[1]}V, Vs3={supply_voltages[2]}V")
print(f"Average Supply: {supply_mean:.1f} V\n")

print("=" * 80)
print("VOLTAGE COMPARISON BY TEST")
print("=" * 80)
for i, L in enumerate(inductance_values):
    print(f"\nTest {i+1}: L = {L} H, XL = {reactance_values[i]:.1f} Ohm")
    print("-" * 70)
    print(f"{'Phase':<10} {'Supply':<12} {'Measured':<12} {'Model 1':<12} {'Model 2':<12} {'Model 3':<12}")
    print("-" * 70)
    for phase_idx, phase in enumerate(['Phase 1', 'Phase 2', 'Phase 3']):
        print(f"{phase:<10} {supply_voltages[phase_idx]:<12} "
              f"{measured_data[L][phase_idx]:<12.0f} "
              f"{model_1_data[L][phase_idx]:<12.1f} "
              f"{model_2_data[L][phase_idx]:<12.1f} "
              f"{model_3_data[L][phase_idx]:<12.1f}")

print("\n" + "=" * 80)
print("ERROR ANALYSIS")
print("=" * 80)
print(f"{'Test':<10} {'Model 1 Error':<18} {'Model 2 Error':<18} {'Model 3 Error':<18}")
print("-" * 70)
for i, L in enumerate(inductance_values):
    print(f"{L} H{'':<6} {errors['Model 1'][i]:<18.1f} {errors['Model 2'][i]:<18.1f} {errors['Model 3'][i]:<18.1f}")
print("-" * 70)
print(f"{'Average':<10} {avg_errors['Model 1']:<18.1f} {avg_errors['Model 2']:<18.1f} {avg_errors['Model 3']:<18.1f}")

print("\n" + "=" * 80)
print("MODEL RANKING")
print("=" * 80)
print("1. Model 1 (Lumped Series, A=1)       - Average error: 2.0 V  ✓ Best match")
print("2. Model 2 (Nominal pi, A=0.954)      - Average error: 5.7 V  ⚠ Overestimates")
print("3. Model 3 (Distributed, A=0.8667)    - Average error: 14.2 V ✗ Unphysical voltage gain")

print("\n" + "=" * 80)
print("KEY OBSERVATIONS")
print("=" * 80)
print("• As inductance increases, Vr increases (82 -> 88 -> 92 V)")
print("• Model 1 best matches measured data across all tests")
print("• Model 3 produces Vr > Vs at high L (physically impossible for passive RL load)")
print("• All models correctly capture increasing voltage trend with higher inductance")
print("• Supply variation (99-102 V) causes phase imbalances in measured data")

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

