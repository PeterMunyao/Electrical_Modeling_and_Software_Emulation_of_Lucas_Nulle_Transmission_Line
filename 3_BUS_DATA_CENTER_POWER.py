import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates
import numpy as np

# Set font to Garamond globally
plt.rcParams['font.family'] = 'Garamond'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = 17
plt.rcParams['legend.fontsize'] = 15
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 17

# PV System data (Column42)
pv_data = [
    0.033000, 0.066000, 0.132000, 0.231000, 0.330000, 0.363000, 0.462000,
    0.627000, 0.726000, 0.759000, 0.759000, 0.858000, 0.924000, 0.990000,
    1.023000, 1.155000, 1.221000, 1.287000, 1.320000, 1.485000, 1.518000,
    1.650000, 1.452000, 1.485000, 1.452000, 1.320000, 1.320000, 1.419000,
    2.013000, 2.112000, 1.749000, 1.947000, 2.211000, 2.409000, 2.376000,
    2.508000, 2.739000, 2.772000, 2.574000, 3.036000, 3.102000, 3.135000,
    3.663000, 4.059000, 4.653000, 5.214000, 6.138000, 6.864000, 7.392000,
    7.128000, 7.293001, 7.458000, 8.580001, 9.603000, 10.329001, 11.121000,
    10.989000, 11.220000, 11.451000, 11.022001, 10.560001, 10.164001, 10.527000,
    11.913001, 11.517000, 11.748000, 13.068001, 13.860001, 13.596001, 14.322001,
    14.091001, 13.332000, 13.365001, 13.497000, 13.728000, 14.025000, 14.718000,
    14.322001, 14.190000, 14.157001, 14.157001, 14.157001, 14.982001, 14.718000,
    14.322001, 14.685001, 14.520001, 14.355001, 14.157001, 13.992001, 13.959000,
    13.959000, 13.959000, 13.926001, 13.992001, 14.025000, 14.058001, 14.058001,
    13.959000, 13.827001, 13.662001, 13.530001, 13.365001, 13.200000, 13.002001,
    12.870001, 12.606001, 12.474001, 12.408001, 12.243001, 11.847001, 11.583000,
    10.923001, 10.824000, 10.494001, 10.131000, 9.900000, 9.240000, 8.976000,
    8.382001, 7.524000, 6.534000, 6.105000, 5.742000, 5.346000, 4.983000,
    4.587000, 4.521000, 4.455000, 4.389000, 4.323000, 4.257000, 4.191001,
    4.092000, 4.026000, 3.960000, 3.861000, 3.795000, 3.729000, 3.630000,
    3.630000, 4.554000, 3.432000, 3.333000, 3.861000, 3.168000, 3.102000,
    3.168000, 3.531000, 3.432000, 3.663000, 2.937000, 3.069000, 3.069000,
    2.607000, 2.607000, 2.376000, 2.376000, 1.881000, 1.749000, 1.617000,
    1.485000, 1.386000, 1.254000, 1.089000, 1.089000, 0.825000, 0.825000,
    0.429000, 0.429000, 0.165000
]

# External Grid data (Column97)
grid_data = [
    3.344227, 3.374627, 3.213213, 3.177612, 3.142641, 3.014227, 2.851830,
    2.877021, 2.651225, 2.649612, 2.586213, 2.582626, 2.453227, 2.546039,
    2.322209, 2.253612, 2.156228, 2.185641, 1.993827, 1.923611, 1.859228,
    1.790627, 1.893213, 2.019023, 1.925225, 2.088612, 2.152641, 1.926212,
    1.364228, 1.328626, 1.659612, 1.366829, 1.261638, 0.968227, 1.064626,
    0.900612, 0.606213, 0.605228, 0.866626, 7.983218, 16.215655, 15.064697,
    17.253061, 14.939534, 15.783576, 12.506601, 15.097372, 12.613811, 11.286860,
    13.627839, 12.344392, 10.422098, 12.975291, 9.555091, 9.787763, 6.918600,
    10.086713, 8.097656, 7.067741, 9.574203, 9.236982, 7.396526, 10.868616,
    7.085533, 8.759376, 6.611215, 7.848060, 5.617811, 5.242340, 6.274203,
    3.948600, 8.383549, 5.793090, 6.460160, 3.992601, 7.050712, 4.919392,
    4.356859, 6.565839, 4.042697, 7.078372, 5.160656, 5.294376, 3.162098,
    6.594060, 4.313534, 5.276982, 4.004214, 6.439203, 5.485811, 4.080600,
    6.477575, -1.983421, -10.389960, -10.614776, -10.584374, -10.712788,
    -10.649389, -10.486359, -10.449774, -10.348171, -10.089376, -9.987774,
    -9.791388, -3.257720, 6.447653, 5.274097, 8.761372, 6.590534, 8.193575,
    6.352696, 9.333061, 8.554811, 7.854860, 10.261839, 9.506392, 7.820601,
    12.315291, 10.182091, 11.734763, 10.515600, 14.541712, 13.212656, 12.776741,
    15.250204, 14.813982, 12.973526, 16.874616, 14.543534, 15.887376, 14.036215,
    16.659061, 15.286811, 14.746341, 16.570203, 14.025814, 17.784899, 15.363091,
    16.228160, 14.090601, 17.445712, 15.083392, 15.246860, 17.422840, 14.338697,
    18.067373, 16.215656, 17.108376, 14.349098, 17.484061, 15.335534, 16.859983,
    15.290215, 17.527204, 16.870811, 15.432600, 18.060576, 16.782091, 15.839602,
    7.995280, 1.124412, 1.096999, 1.037228, 1.009833, 1.016076, 0.857328,
    0.961952, 0.803218, 1.040491, 0.881136, 0.986424
]

# General Load data (Column32)
load_data = [
    2.560000, 2.624000, 2.528000, 2.592000, 2.656000, 2.560000, 2.496000,
    2.688000, 2.560000, 2.592000, 2.528000, 2.624000, 2.560000, 2.720000,
    2.528000, 2.592000, 2.560000, 2.656000, 2.496000, 2.592000, 2.560000,
    2.624000, 2.528000, 2.688000, 2.560000, 2.592000, 2.656000, 2.528000,
    2.560000, 2.624000, 2.592000, 2.496000, 2.656000, 2.560000, 2.624000,
    2.592000, 2.528000, 2.560000, 2.624000, 10.240000, 18.559999, 17.440001,
    20.160000, 18.240000, 19.680000, 16.959999, 20.480000, 18.719999, 17.920000,
    20.000000, 18.879999, 17.120001, 20.799999, 18.400000, 19.360001, 17.280001,
    20.320000, 18.559999, 17.760000, 19.840000, 19.040001, 16.799999, 20.639999,
    18.240000, 19.520000, 17.600000, 20.160000, 18.719999, 18.080000, 19.840000,
    17.280001, 20.959999, 18.400000, 19.200001, 16.959999, 20.320000, 18.879999,
    17.920000, 20.000000, 17.440001, 20.480000, 18.559999, 19.520000, 17.120001,
    20.160000, 18.240000, 19.040001, 17.600000, 19.840000, 18.719999, 17.280001,
    19.680000, 11.200000, 2.720000, 2.560000, 2.624000, 2.528000, 2.592000,
    2.656000, 2.560000, 2.496000, 2.624000, 2.560000, 2.592000, 8.960000,
    18.559999, 17.120001, 20.480000, 18.240000, 19.680000, 17.440001, 20.160000,
    18.719999, 17.920000, 20.000000, 18.879999, 16.959999, 20.799999, 18.400000,
    19.360001, 17.280001, 20.320000, 18.559999, 17.760000, 19.840000, 19.040001,
    16.799999, 20.639999, 18.240000, 19.520000, 17.600000, 20.160000, 18.719999,
    18.080000, 19.840000, 17.280001, 20.959999, 18.400000, 19.200001, 16.959999,
    20.320000, 18.879999, 17.920000, 20.000000, 17.440001, 20.480000, 18.559999,
    19.520000, 17.120001, 20.160000, 18.240000, 19.040001, 17.600000, 19.840000,
    18.719999, 17.280001, 19.680000, 18.400000, 16.959999, 8.960000, 1.920000,
    1.760000, 1.600000, 1.440000, 1.280000, 1.120000, 0.960000, 0.800000,
    0.640000, 0.480000, 0.320000
]

# Generate timestamps (6:15 to 20:25, 5-minute intervals)
start_time = datetime(2024, 5, 19, 6, 15, 0)
timestamps = [start_time + pd.Timedelta(minutes=5*i) for i in range(len(pv_data))]

# Create DataFrame
df = pd.DataFrame({
    'Time': timestamps,
    'PV_System_MW': pv_data,
    'General_Load_MW': load_data,
    'External_Grid_MW': grid_data
})

# Calculate Net Power = PV - Load
df['Net_Power'] = df['PV_System_MW'] - df['General_Load_MW']

# ============================================
# GRAPH 1: Power Balance with Load Profile, PV, Grid, and Net Power
# ============================================
fig1, ax1 = plt.subplots(figsize=(8.3, 5.8))

# Plot Load Profile, PV, Grid, and Net Power
ax1.plot(df['Time'], df['General_Load_MW'], 'r-', linewidth=2.5, label='Data Center Load Profile', alpha=0.9)
ax1.plot(df['Time'], df['PV_System_MW'], 'orange', linewidth=2.5, label='PV Generation', alpha=0.9)
ax1.plot(df['Time'], df['External_Grid_MW'], 'b-', linewidth=2.5, label='External Grid (Load - PV)', alpha=0.9)
ax1.plot(df['Time'], df['Net_Power'], 'g-', linewidth=2.0, label='Net Power (PV - Load)', alpha=0.7)

# Fill between for excess and deficit
ax1.fill_between(df['Time'], 0, df['Net_Power'], where=(df['Net_Power'] > 0), 
                  color='green', alpha=0.2, label='Excess PV (Grid Absorbs)')
ax1.fill_between(df['Time'], 0, df['Net_Power'], where=(df['Net_Power'] < 0), 
                  color='red', alpha=0.2, label='Deficit (Grid Supplies)')

# Add zero reference line
ax1.axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.5)

# Labels
ax1.set_ylabel('Power (MW)', fontweight='bold')
ax1.set_xlabel('19/May/2024 (UTC) Serres C, Greece', fontweight='bold')

# Set Y-axis limits
ax1.set_ylim(-25, 25)
ax1.set_yticks(np.arange(-20, 25, 5))

# Set grid lines
ax1.grid(True, linestyle=':', alpha=0.5, linewidth=1.5)

# Legend below the plot
ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.37), ncol=2, fontsize=13.7)

# Format x-axis - NO ROTATION
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax1.tick_params(axis='x', rotation=0)
ax1.tick_params(axis='both', which='major', labelsize=17, width=2)

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(bottom=0.22)

# Save figure
plt.savefig('Power_Balance_With_Grid_May19_2024_00.pdf', format='pdf', bbox_inches='tight', dpi=300)

# Display first plot
plt.show()

# ============================================
# GRAPH 2: Net Cumulative Energy with Slope-based Coloring
# ============================================
# Calculate energy for each 5-minute interval (MW * 5/60 hours = MWh)
time_interval_hours = 5/60  # 5 minutes in hours
df['Energy_Grid'] = df['External_Grid_MW'] * time_interval_hours

# Calculate cumulative energy
df['Cumulative_Energy'] = df['Energy_Grid'].cumsum()

fig2, ax2 = plt.subplots(figsize=(8.5, 5))

# Plot cumulative energy
ax2.plot(df['Time'], df['Cumulative_Energy'], 'purple', linewidth=2.5, label='Cumulative Grid Energy')

# Fill between for positive slope (grid supplies) and negative slope (grid absorbs)
# Positive slope = grid supplies (External_Grid_MW > 0)
# Negative slope = grid absorbs (External_Grid_MW < 0)
ax2.fill_between(df['Time'], 0, df['Cumulative_Energy'], 
                  where=(df['External_Grid_MW'] > 0), 
                  color='red', alpha=0.2, label='Grid Supply Region (Positive Slope)')
ax2.fill_between(df['Time'], 0, df['Cumulative_Energy'], 
                  where=(df['External_Grid_MW'] < 0), 
                  color='green', alpha=0.2, label='Grid Absorption Region (Negative Slope)')

# Add zero reference line
ax2.axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.5)

# Labels - UPDATED ylabel
ax2.set_ylabel('Net Cumulative Energy (MWh)', fontweight='bold')
ax2.set_xlabel('19/May/2024 (UTC) Serres C, Greece', fontweight='bold')

# Set grid lines
ax2.grid(True, linestyle=':', alpha=0.5, linewidth=1.5)

# Legend below the plot
ax2.legend(loc='lower center', bbox_to_anchor=(0.45, -0.35), ncol=2, fontsize=13.5)

# Format x-axis - NO ROTATION
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax2.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax2.tick_params(axis='x', rotation=0)
ax2.tick_params(axis='both', which='major', labelsize=17, width=2)

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(bottom=0.22)

# Save second figure
plt.savefig('Net_Cumulative_Energy_With_Slope_May19_2024_00.pdf', format='pdf', bbox_inches='tight', dpi=300)

# Display second plot
plt.show()

# Calculate statistics
total_load = df['General_Load_MW'].sum() * time_interval_hours
total_pv = df['PV_System_MW'].sum() * time_interval_hours

# Calculate grid supply and absorption from energy data
df['Energy_Supplied'] = df['Energy_Grid'].where(df['Energy_Grid'] > 0, 0)
df['Energy_Absorbed'] = df['Energy_Grid'].where(df['Energy_Grid'] < 0, 0)

total_grid_sup = df['Energy_Supplied'].sum()
total_grid_abs = abs(df['Energy_Absorbed'].sum())
net_energy = df['Cumulative_Energy'].iloc[-1]

print("ENERGY STATISTICS FOR THE DAY:")
print("=" * 50)
print(f"Total Load Energy: {total_load:.2f} MWh")
print(f"Total PV Generation: {total_pv:.2f} MWh")
print(f"Total Energy Supplied by Grid: {total_grid_sup:.2f} MWh")
print(f"Total Energy Absorbed by Grid (Excess PV): {total_grid_abs:.2f} MWh")
print(f"Net Grid Energy: {net_energy:.2f} MWh ({'Supplied' if net_energy > 0 else 'Absorbed'} by Grid)")

print("\nENERGY BALANCE VERIFICATION:")
print("=" * 50)
print(f"Load = PV + Grid_Supplied - Grid_Absorbed")
print(f"{total_load:.2f} = {total_pv:.2f} + {total_grid_sup:.2f} - {total_grid_abs:.2f}")
print(f"{total_load:.2f} = {total_pv + total_grid_sup - total_grid_abs:.2f} ✓")

print("\nENERGY DENSITY METRICS (% of Load):")
print("=" * 50)
print(f"PV Generation / Load: {total_pv/total_load*100:.1f}%")
print(f"Energy Supplied by Grid / Load: {total_grid_sup/total_load*100:.1f}%")
print(f"Energy Absorbed by Grid / Load: {total_grid_abs/total_load*100:.1f}%")
print(f"Net Grid Energy / Load: {net_energy/total_load*100:.1f}%")
print(f"PV Direct Consumption / Load: {(total_pv - total_grid_abs)/total_load*100:.1f}%")
print(f"Total Flexibility Requirement: {(total_grid_sup + total_grid_abs):.2f} MWh")
print(f"Flexibility Density: {(total_grid_sup + total_grid_abs)/total_load*100:.1f}%")

print("\nPEAK POWER REQUIREMENTS:")
print("=" * 50)
print(f"Peak Load: {df['General_Load_MW'].max():.2f} MW at {df.loc[df['General_Load_MW'].idxmax(), 'Time'].strftime('%H:%M')}")
print(f"Peak PV Generation: {df['PV_System_MW'].max():.2f} MW at {df.loc[df['PV_System_MW'].idxmax(), 'Time'].strftime('%H:%M')}")
print(f"Peak Grid Supply: {df['External_Grid_MW'].max():.2f} MW at {df.loc[df['External_Grid_MW'].idxmax(), 'Time'].strftime('%H:%M')}")
print(f"Peak Grid Absorption: {df['External_Grid_MW'].min():.2f} MW at {df.loc[df['External_Grid_MW'].idxmin(), 'Time'].strftime('%H:%M')}")
print(f"Peak Excess PV: {df['Net_Power'].max():.2f} MW at {df.loc[df['Net_Power'].idxmax(), 'Time'].strftime('%H:%M')}")
print(f"Peak Deficit: {df['Net_Power'].min():.2f} MW at {df.loc[df['Net_Power'].idxmin(), 'Time'].strftime('%H:%M')}")

print("\nINTERPRETATION OF SECOND PLOT:")
print("=" * 50)
print("• Purple line: Net Cumulative Energy")
print("• Red fill: Regions where slope is POSITIVE (Grid SUPPLIES power)")
print("• Green fill: Regions where slope is NEGATIVE (Grid ABSORBS excess PV)")
print("• The slope indicates instantaneous grid power flow direction")
print("• Positive slope = grid is supplying energy to meet load")
print("• Negative slope = grid is absorbing excess PV generation")


#-------------------------------------------------
#-------------------------------------------------

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates
import numpy as np

# Set font to Garamond globally
plt.rcParams['font.family'] = 'Garamond'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = 17
plt.rcParams['legend.fontsize'] = 15
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 17

# PV System data (Column42)
pv_data = [
    0.033000, 0.066000, 0.132000, 0.231000, 0.330000, 0.363000, 0.462000,
    0.627000, 0.726000, 0.759000, 0.759000, 0.858000, 0.924000, 0.990000,
    1.023000, 1.155000, 1.221000, 1.287000, 1.320000, 1.485000, 1.518000,
    1.650000, 1.452000, 1.485000, 1.452000, 1.320000, 1.320000, 1.419000,
    2.013000, 2.112000, 1.749000, 1.947000, 2.211000, 2.409000, 2.376000,
    2.508000, 2.739000, 2.772000, 2.574000, 3.036000, 3.102000, 3.135000,
    3.663000, 4.059000, 4.653000, 5.214000, 6.138000, 6.864000, 7.392000,
    7.128000, 7.293001, 7.458000, 8.580001, 9.603000, 10.329001, 11.121000,
    10.989000, 11.220000, 11.451000, 11.022001, 10.560001, 10.164001, 10.527000,
    11.913001, 11.517000, 11.748000, 13.068001, 13.860001, 13.596001, 14.322001,
    14.091001, 13.332000, 13.365001, 13.497000, 13.728000, 14.025000, 14.718000,
    14.322001, 14.190000, 14.157001, 14.157001, 14.157001, 14.982001, 14.718000,
    14.322001, 14.685001, 14.520001, 14.355001, 14.157001, 13.992001, 13.959000,
    13.959000, 13.959000, 13.926001, 13.992001, 14.025000, 14.058001, 14.058001,
    13.959000, 13.827001, 13.662001, 13.530001, 13.365001, 13.200000, 13.002001,
    12.870001, 12.606001, 12.474001, 12.408001, 12.243001, 11.847001, 11.583000,
    10.923001, 10.824000, 10.494001, 10.131000, 9.900000, 9.240000, 8.976000,
    8.382001, 7.524000, 6.534000, 6.105000, 5.742000, 5.346000, 4.983000,
    4.587000, 4.521000, 4.455000, 4.389000, 4.323000, 4.257000, 4.191001,
    4.092000, 4.026000, 3.960000, 3.861000, 3.795000, 3.729000, 3.630000,
    3.630000, 4.554000, 3.432000, 3.333000, 3.861000, 3.168000, 3.102000,
    3.168000, 3.531000, 3.432000, 3.663000, 2.937000, 3.069000, 3.069000,
    2.607000, 2.607000, 2.376000, 2.376000, 1.881000, 1.749000, 1.617000,
    1.485000, 1.386000, 1.254000, 1.089000, 1.089000, 0.825000, 0.825000,
    0.429000, 0.429000, 0.165000
]

# External Grid data (Column97)
grid_data = [
    3.344227, 3.374627, 3.213213, 3.177612, 3.142641, 3.014227, 2.851830,
    2.877021, 2.651225, 2.649612, 2.586213, 2.582626, 2.453227, 2.546039,
    2.322209, 2.253612, 2.156228, 2.185641, 1.993827, 1.923611, 1.859228,
    1.790627, 1.893213, 2.019023, 1.925225, 2.088612, 2.152641, 1.926212,
    1.364228, 1.328626, 1.659612, 1.366829, 1.261638, 0.968227, 1.064626,
    0.900612, 0.606213, 0.605228, 0.866626, 7.983218, 16.215655, 15.064697,
    17.253061, 14.939534, 15.783576, 12.506601, 15.097372, 12.613811, 11.286860,
    13.627839, 12.344392, 10.422098, 12.975291, 9.555091, 9.787763, 6.918600,
    10.086713, 8.097656, 7.067741, 9.574203, 9.236982, 7.396526, 10.868616,
    7.085533, 8.759376, 6.611215, 7.848060, 5.617811, 5.242340, 6.274203,
    3.948600, 8.383549, 5.793090, 6.460160, 3.992601, 7.050712, 4.919392,
    4.356859, 6.565839, 4.042697, 7.078372, 5.160656, 5.294376, 3.162098,
    6.594060, 4.313534, 5.276982, 4.004214, 6.439203, 5.485811, 4.080600,
    6.477575, -1.983421, -10.389960, -10.614776, -10.584374, -10.712788,
    -10.649389, -10.486359, -10.449774, -10.348171, -10.089376, -9.987774,
    -9.791388, -3.257720, 6.447653, 5.274097, 8.761372, 6.590534, 8.193575,
    6.352696, 9.333061, 8.554811, 7.854860, 10.261839, 9.506392, 7.820601,
    12.315291, 10.182091, 11.734763, 10.515600, 14.541712, 13.212656, 12.776741,
    15.250204, 14.813982, 12.973526, 16.874616, 14.543534, 15.887376, 14.036215,
    16.659061, 15.286811, 14.746341, 16.570203, 14.025814, 17.784899, 15.363091,
    16.228160, 14.090601, 17.445712, 15.083392, 15.246860, 17.422840, 14.338697,
    18.067373, 16.215656, 17.108376, 14.349098, 17.484061, 15.335534, 16.859983,
    15.290215, 17.527204, 16.870811, 15.432600, 18.060576, 16.782091, 15.839602,
    7.995280, 1.124412, 1.096999, 1.037228, 1.009833, 1.016076, 0.857328,
    0.961952, 0.803218, 1.040491, 0.881136, 0.986424
]

# General Load data (Column32)
load_data = [
    2.560000, 2.624000, 2.528000, 2.592000, 2.656000, 2.560000, 2.496000,
    2.688000, 2.560000, 2.592000, 2.528000, 2.624000, 2.560000, 2.720000,
    2.528000, 2.592000, 2.560000, 2.656000, 2.496000, 2.592000, 2.560000,
    2.624000, 2.528000, 2.688000, 2.560000, 2.592000, 2.656000, 2.528000,
    2.560000, 2.624000, 2.592000, 2.496000, 2.656000, 2.560000, 2.624000,
    2.592000, 2.528000, 2.560000, 2.624000, 10.240000, 18.559999, 17.440001,
    20.160000, 18.240000, 19.680000, 16.959999, 20.480000, 18.719999, 17.920000,
    20.000000, 18.879999, 17.120001, 20.799999, 18.400000, 19.360001, 17.280001,
    20.320000, 18.559999, 17.760000, 19.840000, 19.040001, 16.799999, 20.639999,
    18.240000, 19.520000, 17.600000, 20.160000, 18.719999, 18.080000, 19.840000,
    17.280001, 20.959999, 18.400000, 19.200001, 16.959999, 20.320000, 18.879999,
    17.920000, 20.000000, 17.440001, 20.480000, 18.559999, 19.520000, 17.120001,
    20.160000, 18.240000, 19.040001, 17.600000, 19.840000, 18.719999, 17.280001,
    19.680000, 11.200000, 2.720000, 2.560000, 2.624000, 2.528000, 2.592000,
    2.656000, 2.560000, 2.496000, 2.624000, 2.560000, 2.592000, 8.960000,
    18.559999, 17.120001, 20.480000, 18.240000, 19.680000, 17.440001, 20.160000,
    18.719999, 17.920000, 20.000000, 18.879999, 16.959999, 20.799999, 18.400000,
    19.360001, 17.280001, 20.320000, 18.559999, 17.760000, 19.840000, 19.040001,
    16.799999, 20.639999, 18.240000, 19.520000, 17.600000, 20.160000, 18.719999,
    18.080000, 19.840000, 17.280001, 20.959999, 18.400000, 19.200001, 16.959999,
    20.320000, 18.879999, 17.920000, 20.000000, 17.440001, 20.480000, 18.559999,
    19.520000, 17.120001, 20.160000, 18.240000, 19.040001, 17.600000, 19.840000,
    18.719999, 17.280001, 19.680000, 18.400000, 16.959999, 8.960000, 1.920000,
    1.760000, 1.600000, 1.440000, 1.280000, 1.120000, 0.960000, 0.800000,
    0.640000, 0.480000, 0.320000
]

# Generate timestamps (6:15 to 20:25, 5-minute intervals)
start_time = datetime(2024, 5, 19, 6, 15, 0)
timestamps = [start_time + pd.Timedelta(minutes=5*i) for i in range(len(pv_data))]

# Create DataFrame
df = pd.DataFrame({
    'Time': timestamps,
    'PV_System_MW': pv_data,
    'General_Load_MW': load_data,
    'External_Grid_MW': grid_data
})

# Calculate Net Power = PV - Load
df['Net_Power'] = df['PV_System_MW'] - df['General_Load_MW']

# ============================================
# SINGLE GRAPH: Net Cumulative Energy with Slope-based Coloring and Max Annotation
# ============================================
# Calculate energy for each 5-minute interval (MW * 5/60 hours = MWh)
time_interval_hours = 5/60  # 5 minutes in hours
df['Energy_Grid'] = df['External_Grid_MW'] * time_interval_hours

# Calculate cumulative energy
df['Cumulative_Energy'] = df['Energy_Grid'].cumsum()

fig, ax = plt.subplots(figsize=(7, 5))

# Plot cumulative energy
ax.plot(df['Time'], df['Cumulative_Energy'], 'purple', linewidth=2.5, label='Cumulative Grid Energy')

# Fill between for positive slope (grid supplies) and negative slope (grid absorbs)
# Positive slope = grid supplies (External_Grid_MW > 0)
# Negative slope = grid absorbs (External_Grid_MW < 0)
ax.fill_between(df['Time'], 0, df['Cumulative_Energy'], 
                  where=(df['External_Grid_MW'] > 0), 
                  color='red', alpha=0.2, label='Grid Supply Region (Positive Slope)')
ax.fill_between(df['Time'], 0, df['Cumulative_Energy'], 
                  where=(df['External_Grid_MW'] < 0), 
                  color='green', alpha=0.2, label='Grid Absorption Region (Negative Slope)')

# Add zero reference line
ax.axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.5)

# Labels
ax.set_ylabel('Net Cumulative Energy (MWh)', fontweight='bold')
ax.set_xlabel('19/May/2024 (UTC) Serres C, Greece', fontweight='bold')

# Set grid lines
ax.grid(True, linestyle=':', alpha=0.5, linewidth=1.5)

# ============================================
# ANNOTATE MAXIMUM VALUE ON THE LEFT SIDE
# ============================================
max_idx = df['Cumulative_Energy'].idxmax()
max_val = df['Cumulative_Energy'].max()
max_time = df.loc[max_idx, 'Time']

ax.annotate(f'Max: {max_val:.2f} MWh', 
            xy=(max_time, max_val),
            xytext=(15, 5), textcoords='offset points',
            color='purple', fontsize=12, fontweight='bold',
            verticalalignment='center',
            horizontalalignment='right')

# Legend below the plot
ax.legend(loc='lower center', bbox_to_anchor=(0.47, -0.47), ncol=1, fontsize=14.5)

# Format x-axis - NO ROTATION
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.tick_params(axis='x', rotation=0)
ax.tick_params(axis='both', which='major', labelsize=17, width=2)

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(bottom=0.22)

# Save figure with the specified PDF name
plt.savefig('Net_Cumulative_Energy_With_Slope_May19_2024_00.pdf', format='pdf', bbox_inches='tight', dpi=300)

# Display plot
plt.show()

# Calculate statistics
total_load = df['General_Load_MW'].sum() * time_interval_hours
total_pv = df['PV_System_MW'].sum() * time_interval_hours

# Calculate grid supply and absorption from energy data
df['Energy_Supplied'] = df['Energy_Grid'].where(df['Energy_Grid'] > 0, 0)
df['Energy_Absorbed'] = df['Energy_Grid'].where(df['Energy_Grid'] < 0, 0)

total_grid_sup = df['Energy_Supplied'].sum()
total_grid_abs = abs(df['Energy_Absorbed'].sum())
net_energy = df['Cumulative_Energy'].iloc[-1]

print("ENERGY STATISTICS FOR THE DAY:")
print("=" * 50)
print(f"Total Load Energy: {total_load:.2f} MWh")
print(f"Total PV Generation: {total_pv:.2f} MWh")
print(f"Total Energy Supplied by Grid: {total_grid_sup:.2f} MWh")
print(f"Total Energy Absorbed by Grid (Excess PV): {total_grid_abs:.2f} MWh")
print(f"Net Grid Energy: {net_energy:.2f} MWh ({'Supplied' if net_energy > 0 else 'Absorbed'} by Grid)")
print(f"Maximum Cumulative Energy: {max_val:.2f} MWh at {max_time.strftime('%H:%M')}")

print("\nENERGY BALANCE VERIFICATION:")
print("=" * 50)
print(f"Load = PV + Grid_Supplied - Grid_Absorbed")
print(f"{total_load:.2f} = {total_pv:.2f} + {total_grid_sup:.2f} - {total_grid_abs:.2f}")
print(f"{total_load:.2f} = {total_pv + total_grid_sup - total_grid_abs:.2f} ✓")

print("\nINTERPRETATION:")
print("=" * 50)
print("• Purple line: Net Cumulative Energy")
print("• Red fill: Regions where slope is POSITIVE (Grid SUPPLIES power)")
print("• Green fill: Regions where slope is NEGATIVE (Grid ABSORBS excess PV)")
print("• Purple annotation shows the maximum cumulative energy value")
print("• Positive slope = grid is supplying energy to meet load")
print("• Negative slope = grid is absorbing excess PV generation")


#--------------------------------------------------

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates
import numpy as np

# Set font to Garamond globally
plt.rcParams['font.family'] = 'Garamond'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = 17
plt.rcParams['legend.fontsize'] = 15
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 17

# PV System data (Column42)
pv_data = [
    0.033000, 0.066000, 0.132000, 0.231000, 0.330000, 0.363000, 0.462000,
    0.627000, 0.726000, 0.759000, 0.759000, 0.858000, 0.924000, 0.990000,
    1.023000, 1.155000, 1.221000, 1.287000, 1.320000, 1.485000, 1.518000,
    1.650000, 1.452000, 1.485000, 1.452000, 1.320000, 1.320000, 1.419000,
    2.013000, 2.112000, 1.749000, 1.947000, 2.211000, 2.409000, 2.376000,
    2.508000, 2.739000, 2.772000, 2.574000, 3.036000, 3.102000, 3.135000,
    3.663000, 4.059000, 4.653000, 5.214000, 6.138000, 6.864000, 7.392000,
    7.128000, 7.293001, 7.458000, 8.580001, 9.603000, 10.329001, 11.121000,
    10.989000, 11.220000, 11.451000, 11.022001, 10.560001, 10.164001, 10.527000,
    11.913001, 11.517000, 11.748000, 13.068001, 13.860001, 13.596001, 14.322001,
    14.091001, 13.332000, 13.365001, 13.497000, 13.728000, 14.025000, 14.718000,
    14.322001, 14.190000, 14.157001, 14.157001, 14.157001, 14.982001, 14.718000,
    14.322001, 14.685001, 14.520001, 14.355001, 14.157001, 13.992001, 13.959000,
    13.959000, 13.959000, 13.926001, 13.992001, 14.025000, 14.058001, 14.058001,
    13.959000, 13.827001, 13.662001, 13.530001, 13.365001, 13.200000, 13.002001,
    12.870001, 12.606001, 12.474001, 12.408001, 12.243001, 11.847001, 11.583000,
    10.923001, 10.824000, 10.494001, 10.131000, 9.900000, 9.240000, 8.976000,
    8.382001, 7.524000, 6.534000, 6.105000, 5.742000, 5.346000, 4.983000,
    4.587000, 4.521000, 4.455000, 4.389000, 4.323000, 4.257000, 4.191001,
    4.092000, 4.026000, 3.960000, 3.861000, 3.795000, 3.729000, 3.630000,
    3.630000, 4.554000, 3.432000, 3.333000, 3.861000, 3.168000, 3.102000,
    3.168000, 3.531000, 3.432000, 3.663000, 2.937000, 3.069000, 3.069000,
    2.607000, 2.607000, 2.376000, 2.376000, 1.881000, 1.749000, 1.617000,
    1.485000, 1.386000, 1.254000, 1.089000, 1.089000, 0.825000, 0.825000,
    0.429000, 0.429000, 0.165000
]

# External Grid data (Column97)
grid_data = [
    3.344227, 3.374627, 3.213213, 3.177612, 3.142641, 3.014227, 2.851830,
    2.877021, 2.651225, 2.649612, 2.586213, 2.582626, 2.453227, 2.546039,
    2.322209, 2.253612, 2.156228, 2.185641, 1.993827, 1.923611, 1.859228,
    1.790627, 1.893213, 2.019023, 1.925225, 2.088612, 2.152641, 1.926212,
    1.364228, 1.328626, 1.659612, 1.366829, 1.261638, 0.968227, 1.064626,
    0.900612, 0.606213, 0.605228, 0.866626, 7.983218, 16.215655, 15.064697,
    17.253061, 14.939534, 15.783576, 12.506601, 15.097372, 12.613811, 11.286860,
    13.627839, 12.344392, 10.422098, 12.975291, 9.555091, 9.787763, 6.918600,
    10.086713, 8.097656, 7.067741, 9.574203, 9.236982, 7.396526, 10.868616,
    7.085533, 8.759376, 6.611215, 7.848060, 5.617811, 5.242340, 6.274203,
    3.948600, 8.383549, 5.793090, 6.460160, 3.992601, 7.050712, 4.919392,
    4.356859, 6.565839, 4.042697, 7.078372, 5.160656, 5.294376, 3.162098,
    6.594060, 4.313534, 5.276982, 4.004214, 6.439203, 5.485811, 4.080600,
    6.477575, -1.983421, -10.389960, -10.614776, -10.584374, -10.712788,
    -10.649389, -10.486359, -10.449774, -10.348171, -10.089376, -9.987774,
    -9.791388, -3.257720, 6.447653, 5.274097, 8.761372, 6.590534, 8.193575,
    6.352696, 9.333061, 8.554811, 7.854860, 10.261839, 9.506392, 7.820601,
    12.315291, 10.182091, 11.734763, 10.515600, 14.541712, 13.212656, 12.776741,
    15.250204, 14.813982, 12.973526, 16.874616, 14.543534, 15.887376, 14.036215,
    16.659061, 15.286811, 14.746341, 16.570203, 14.025814, 17.784899, 15.363091,
    16.228160, 14.090601, 17.445712, 15.083392, 15.246860, 17.422840, 14.338697,
    18.067373, 16.215656, 17.108376, 14.349098, 17.484061, 15.335534, 16.859983,
    15.290215, 17.527204, 16.870811, 15.432600, 18.060576, 16.782091, 15.839602,
    7.995280, 1.124412, 1.096999, 1.037228, 1.009833, 1.016076, 0.857328,
    0.961952, 0.803218, 1.040491, 0.881136, 0.986424
]

# General Load data (Column32)
load_data = [
    2.560000, 2.624000, 2.528000, 2.592000, 2.656000, 2.560000, 2.496000,
    2.688000, 2.560000, 2.592000, 2.528000, 2.624000, 2.560000, 2.720000,
    2.528000, 2.592000, 2.560000, 2.656000, 2.496000, 2.592000, 2.560000,
    2.624000, 2.528000, 2.688000, 2.560000, 2.592000, 2.656000, 2.528000,
    2.560000, 2.624000, 2.592000, 2.496000, 2.656000, 2.560000, 2.624000,
    2.592000, 2.528000, 2.560000, 2.624000, 10.240000, 18.559999, 17.440001,
    20.160000, 18.240000, 19.680000, 16.959999, 20.480000, 18.719999, 17.920000,
    20.000000, 18.879999, 17.120001, 20.799999, 18.400000, 19.360001, 17.280001,
    20.320000, 18.559999, 17.760000, 19.840000, 19.040001, 16.799999, 20.639999,
    18.240000, 19.520000, 17.600000, 20.160000, 18.719999, 18.080000, 19.840000,
    17.280001, 20.959999, 18.400000, 19.200001, 16.959999, 20.320000, 18.879999,
    17.920000, 20.000000, 17.440001, 20.480000, 18.559999, 19.520000, 17.120001,
    20.160000, 18.240000, 19.040001, 17.600000, 19.840000, 18.719999, 17.280001,
    19.680000, 11.200000, 2.720000, 2.560000, 2.624000, 2.528000, 2.592000,
    2.656000, 2.560000, 2.496000, 2.624000, 2.560000, 2.592000, 8.960000,
    18.559999, 17.120001, 20.480000, 18.240000, 19.680000, 17.440001, 20.160000,
    18.719999, 17.920000, 20.000000, 18.879999, 16.959999, 20.799999, 18.400000,
    19.360001, 17.280001, 20.320000, 18.559999, 17.760000, 19.840000, 19.040001,
    16.799999, 20.639999, 18.240000, 19.520000, 17.600000, 20.160000, 18.719999,
    18.080000, 19.840000, 17.280001, 20.959999, 18.400000, 19.200001, 16.959999,
    20.320000, 18.879999, 17.920000, 20.000000, 17.440001, 20.480000, 18.559999,
    19.520000, 17.120001, 20.160000, 18.240000, 19.040001, 17.600000, 19.840000,
    18.719999, 17.280001, 19.680000, 18.400000, 16.959999, 8.960000, 1.920000,
    1.760000, 1.600000, 1.440000, 1.280000, 1.120000, 0.960000, 0.800000,
    0.640000, 0.480000, 0.320000
]

# Generate timestamps (6:15 to 20:25, 5-minute intervals)
start_time = datetime(2024, 5, 19, 6, 15, 0)
timestamps = [start_time + pd.Timedelta(minutes=5*i) for i in range(len(pv_data))]

# Create DataFrame
df = pd.DataFrame({
    'Time': timestamps,
    'PV_System_MW': pv_data,
    'General_Load_MW': load_data,
    'External_Grid_MW': grid_data
})

# Calculate Net Power = PV - Load
df['Net_Power'] = df['PV_System_MW'] - df['General_Load_MW']

# ============================================
# SINGLE GRAPH: Net Cumulative Energy with Slope-based Coloring and Max Annotation
# ============================================
# Calculate energy for each 5-minute interval (MW * 5/60 hours = MWh)
time_interval_hours = 5/60  # 5 minutes in hours
df['Energy_Grid'] = df['External_Grid_MW'] * time_interval_hours

# Calculate cumulative energy
df['Cumulative_Energy'] = df['Energy_Grid'].cumsum()

fig, ax = plt.subplots(figsize=(7.5, 5))

# Plot cumulative energy
ax.plot(df['Time'], df['Cumulative_Energy'], 'purple', linewidth=2.5, label='Cumulative Grid Energy')

# Fill between for positive slope (grid supplies) and negative slope (grid absorbs)
# Positive slope = grid supplies (External_Grid_MW > 0)
# Negative slope = grid absorbs (External_Grid_MW < 0)
ax.fill_between(df['Time'], 0, df['Cumulative_Energy'], 
                  where=(df['External_Grid_MW'] > 0), 
                  color='red', alpha=0.2, label='Grid Supply Region (Positive Slope)')
ax.fill_between(df['Time'], 0, df['Cumulative_Energy'], 
                  where=(df['External_Grid_MW'] < 0), 
                  color='green', alpha=0.2, label='Grid Absorption Region (Negative Slope)')

# Add zero reference line
ax.axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.5)

# Labels
ax.set_ylabel('Net Cumulative Energy (MWh)', fontweight='bold')
ax.set_xlabel('19/May/2024 (UTC) Serres C, Greece', fontweight='bold')

# Set grid lines
ax.grid(True, linestyle=':', alpha=0.5, linewidth=1.5)

# ============================================
# ANNOTATE MAXIMUM VALUE ON THE LEFT SIDE
# ============================================
max_idx = df['Cumulative_Energy'].idxmax()
max_val = df['Cumulative_Energy'].max()
max_time = df.loc[max_idx, 'Time']

ax.annotate(f'Max: {max_val:.2f} MWh', 
            xy=(max_time, max_val),
            xytext=(15, 5), textcoords='offset points',
            color='purple', fontsize=12, fontweight='bold',
            verticalalignment='center',
            horizontalalignment='right')

# ============================================
# LEGEND INSIDE PLOT - TOP LEFT WITH TRANSPARENT BACKGROUND
# ============================================
ax.legend(loc='upper left', framealpha=0.3, fontsize=12, ncol=1, 
          edgecolor='black', fancybox=True)

# Format x-axis - NO ROTATION
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.tick_params(axis='x', rotation=0)
ax.tick_params(axis='both', which='major', labelsize=17, width=2)

# Adjust layout
plt.tight_layout()

# Save figure with the specified PDF name
plt.savefig('Net_Cumulative_Energy_With_Slope_May19_2024_00.pdf', format='pdf', bbox_inches='tight', dpi=300)

# Display plot
plt.show()

# Calculate statistics
total_load = df['General_Load_MW'].sum() * time_interval_hours
total_pv = df['PV_System_MW'].sum() * time_interval_hours

# Calculate grid supply and absorption from energy data
df['Energy_Supplied'] = df['Energy_Grid'].where(df['Energy_Grid'] > 0, 0)
df['Energy_Absorbed'] = df['Energy_Grid'].where(df['Energy_Grid'] < 0, 0)

total_grid_sup = df['Energy_Supplied'].sum()
total_grid_abs = abs(df['Energy_Absorbed'].sum())
net_energy = df['Cumulative_Energy'].iloc[-1]

print("ENERGY STATISTICS FOR THE DAY:")
print("=" * 50)
print(f"Total Load Energy: {total_load:.2f} MWh")
print(f"Total PV Generation: {total_pv:.2f} MWh")
print(f"Total Energy Supplied by Grid: {total_grid_sup:.2f} MWh")
print(f"Total Energy Absorbed by Grid (Excess PV): {total_grid_abs:.2f} MWh")
print(f"Net Grid Energy: {net_energy:.2f} MWh ({'Supplied' if net_energy > 0 else 'Absorbed'} by Grid)")
print(f"Maximum Cumulative Energy: {max_val:.2f} MWh at {max_time.strftime('%H:%M')}")

print("\nENERGY BALANCE VERIFICATION:")
print("=" * 50)
print(f"Load = PV + Grid_Supplied - Grid_Absorbed")
print(f"{total_load:.2f} = {total_pv:.2f} + {total_grid_sup:.2f} - {total_grid_abs:.2f}")
print(f"{total_load:.2f} = {total_pv + total_grid_sup - total_grid_abs:.2f} ✓")

print("\nINTERPRETATION:")
print("=" * 50)
print("• Purple line: Net Cumulative Energy")
print("• Red fill: Regions where slope is POSITIVE (Grid SUPPLIES power)")
print("• Green fill: Regions where slope is NEGATIVE (Grid ABSORBS excess PV)")
print("• Purple annotation shows the maximum cumulative energy value")
print("• Positive slope = grid is supplying energy to meet load")
print("• Negative slope = grid is absorbing excess PV generation")

#-----------------------------------------------------------------------
#----------------RAMP-RATES---------------------------------------------
#-----------------------------------------------------------------------


import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates
import numpy as np

# Set font to Garamond globally
plt.rcParams['font.family'] = 'Garamond'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = 17
plt.rcParams['legend.fontsize'] = 15
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 17

# PV System data (Column42)
pv_data = [
    0.033000, 0.066000, 0.132000, 0.231000, 0.330000, 0.363000, 0.462000,
    0.627000, 0.726000, 0.759000, 0.759000, 0.858000, 0.924000, 0.990000,
    1.023000, 1.155000, 1.221000, 1.287000, 1.320000, 1.485000, 1.518000,
    1.650000, 1.452000, 1.485000, 1.452000, 1.320000, 1.320000, 1.419000,
    2.013000, 2.112000, 1.749000, 1.947000, 2.211000, 2.409000, 2.376000,
    2.508000, 2.739000, 2.772000, 2.574000, 3.036000, 3.102000, 3.135000,
    3.663000, 4.059000, 4.653000, 5.214000, 6.138000, 6.864000, 7.392000,
    7.128000, 7.293001, 7.458000, 8.580001, 9.603000, 10.329001, 11.121000,
    10.989000, 11.220000, 11.451000, 11.022001, 10.560001, 10.164001, 10.527000,
    11.913001, 11.517000, 11.748000, 13.068001, 13.860001, 13.596001, 14.322001,
    14.091001, 13.332000, 13.365001, 13.497000, 13.728000, 14.025000, 14.718000,
    14.322001, 14.190000, 14.157001, 14.157001, 14.157001, 14.982001, 14.718000,
    14.322001, 14.685001, 14.520001, 14.355001, 14.157001, 13.992001, 13.959000,
    13.959000, 13.959000, 13.926001, 13.992001, 14.025000, 14.058001, 14.058001,
    13.959000, 13.827001, 13.662001, 13.530001, 13.365001, 13.200000, 13.002001,
    12.870001, 12.606001, 12.474001, 12.408001, 12.243001, 11.847001, 11.583000,
    10.923001, 10.824000, 10.494001, 10.131000, 9.900000, 9.240000, 8.976000,
    8.382001, 7.524000, 6.534000, 6.105000, 5.742000, 5.346000, 4.983000,
    4.587000, 4.521000, 4.455000, 4.389000, 4.323000, 4.257000, 4.191001,
    4.092000, 4.026000, 3.960000, 3.861000, 3.795000, 3.729000, 3.630000,
    3.630000, 4.554000, 3.432000, 3.333000, 3.861000, 3.168000, 3.102000,
    3.168000, 3.531000, 3.432000, 3.663000, 2.937000, 3.069000, 3.069000,
    2.607000, 2.607000, 2.376000, 2.376000, 1.881000, 1.749000, 1.617000,
    1.485000, 1.386000, 1.254000, 1.089000, 1.089000, 0.825000, 0.825000,
    0.429000, 0.429000, 0.165000
]

# External Grid data (Column97)
grid_data = [
    3.344227, 3.374627, 3.213213, 3.177612, 3.142641, 3.014227, 2.851830,
    2.877021, 2.651225, 2.649612, 2.586213, 2.582626, 2.453227, 2.546039,
    2.322209, 2.253612, 2.156228, 2.185641, 1.993827, 1.923611, 1.859228,
    1.790627, 1.893213, 2.019023, 1.925225, 2.088612, 2.152641, 1.926212,
    1.364228, 1.328626, 1.659612, 1.366829, 1.261638, 0.968227, 1.064626,
    0.900612, 0.606213, 0.605228, 0.866626, 7.983218, 16.215655, 15.064697,
    17.253061, 14.939534, 15.783576, 12.506601, 15.097372, 12.613811, 11.286860,
    13.627839, 12.344392, 10.422098, 12.975291, 9.555091, 9.787763, 6.918600,
    10.086713, 8.097656, 7.067741, 9.574203, 9.236982, 7.396526, 10.868616,
    7.085533, 8.759376, 6.611215, 7.848060, 5.617811, 5.242340, 6.274203,
    3.948600, 8.383549, 5.793090, 6.460160, 3.992601, 7.050712, 4.919392,
    4.356859, 6.565839, 4.042697, 7.078372, 5.160656, 5.294376, 3.162098,
    6.594060, 4.313534, 5.276982, 4.004214, 6.439203, 5.485811, 4.080600,
    6.477575, -1.983421, -10.389960, -10.614776, -10.584374, -10.712788,
    -10.649389, -10.486359, -10.449774, -10.348171, -10.089376, -9.987774,
    -9.791388, -3.257720, 6.447653, 5.274097, 8.761372, 6.590534, 8.193575,
    6.352696, 9.333061, 8.554811, 7.854860, 10.261839, 9.506392, 7.820601,
    12.315291, 10.182091, 11.734763, 10.515600, 14.541712, 13.212656, 12.776741,
    15.250204, 14.813982, 12.973526, 16.874616, 14.543534, 15.887376, 14.036215,
    16.659061, 15.286811, 14.746341, 16.570203, 14.025814, 17.784899, 15.363091,
    16.228160, 14.090601, 17.445712, 15.083392, 15.246860, 17.422840, 14.338697,
    18.067373, 16.215656, 17.108376, 14.349098, 17.484061, 15.335534, 16.859983,
    15.290215, 17.527204, 16.870811, 15.432600, 18.060576, 16.782091, 15.839602,
    7.995280, 1.124412, 1.096999, 1.037228, 1.009833, 1.016076, 0.857328,
    0.961952, 0.803218, 1.040491, 0.881136, 0.986424
]

# General Load data (Column32)
load_data = [
    2.560000, 2.624000, 2.528000, 2.592000, 2.656000, 2.560000, 2.496000,
    2.688000, 2.560000, 2.592000, 2.528000, 2.624000, 2.560000, 2.720000,
    2.528000, 2.592000, 2.560000, 2.656000, 2.496000, 2.592000, 2.560000,
    2.624000, 2.528000, 2.688000, 2.560000, 2.592000, 2.656000, 2.528000,
    2.560000, 2.624000, 2.592000, 2.496000, 2.656000, 2.560000, 2.624000,
    2.592000, 2.528000, 2.560000, 2.624000, 10.240000, 18.559999, 17.440001,
    20.160000, 18.240000, 19.680000, 16.959999, 20.480000, 18.719999, 17.920000,
    20.000000, 18.879999, 17.120001, 20.799999, 18.400000, 19.360001, 17.280001,
    20.320000, 18.559999, 17.760000, 19.840000, 19.040001, 16.799999, 20.639999,
    18.240000, 19.520000, 17.600000, 20.160000, 18.719999, 18.080000, 19.840000,
    17.280001, 20.959999, 18.400000, 19.200001, 16.959999, 20.320000, 18.879999,
    17.920000, 20.000000, 17.440001, 20.480000, 18.559999, 19.520000, 17.120001,
    20.160000, 18.240000, 19.040001, 17.600000, 19.840000, 18.719999, 17.280001,
    19.680000, 11.200000, 2.720000, 2.560000, 2.624000, 2.528000, 2.592000,
    2.656000, 2.560000, 2.496000, 2.624000, 2.560000, 2.592000, 8.960000,
    18.559999, 17.120001, 20.480000, 18.240000, 19.680000, 17.440001, 20.160000,
    18.719999, 17.920000, 20.000000, 18.879999, 16.959999, 20.799999, 18.400000,
    19.360001, 17.280001, 20.320000, 18.559999, 17.760000, 19.840000, 19.040001,
    16.799999, 20.639999, 18.240000, 19.520000, 17.600000, 20.160000, 18.719999,
    18.080000, 19.840000, 17.280001, 20.959999, 18.400000, 19.200001, 16.959999,
    20.320000, 18.879999, 17.920000, 20.000000, 17.440001, 20.480000, 18.559999,
    19.520000, 17.120001, 20.160000, 18.240000, 19.040001, 17.600000, 19.840000,
    18.719999, 17.280001, 19.680000, 18.400000, 16.959999, 8.960000, 1.920000,
    1.760000, 1.600000, 1.440000, 1.280000, 1.120000, 0.960000, 0.800000,
    0.640000, 0.480000, 0.320000
]

# Generate timestamps (6:15 to 20:25, 5-minute intervals)
start_time = datetime(2024, 5, 19, 6, 15, 0)
timestamps = [start_time + pd.Timedelta(minutes=5*i) for i in range(len(pv_data))]

# Create DataFrame
df = pd.DataFrame({
    'Time': timestamps,
    'PV_System_MW': pv_data,
    'General_Load_MW': load_data,
    'External_Grid_MW': grid_data
})

# Calculate ramp rates in MW/5 minutes (no division by time interval)
# Ramp rate = (current - previous) / 1 interval (5 minutes)
df['Load_Ramp'] = df['General_Load_MW'].diff()
df['Grid_Ramp'] = df['External_Grid_MW'].diff()
df['PV_Ramp'] = df['PV_System_MW'].diff()

# Fill first row with 0 using proper assignment
df['Load_Ramp'] = df['Load_Ramp'].fillna(0)
df['Grid_Ramp'] = df['Grid_Ramp'].fillna(0)
df['PV_Ramp'] = df['PV_Ramp'].fillna(0)

# ============================================
# SINGLE GRAPH: Ramp Rates in MW/5 Minutes with External Grid Annotations Only
# ============================================
fig, ax = plt.subplots(figsize=(7, 5))

# Plot ramp rates with thinner lines
ax.plot(df['Time'], df['Load_Ramp'], 'r-', linewidth=1.5, label='Data Center Load Ramp Rate', alpha=0.9)
ax.plot(df['Time'], df['PV_Ramp'], 'orange', linewidth=1.5, label='PV Ramp Rate', alpha=0.9)
ax.plot(df['Time'], df['Grid_Ramp'], 'b-', linewidth=1.5, label='External Grid Ramp Rate', alpha=0.9)

# Add zero reference line
ax.axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.5)

# Labels - Updated to MW/5min
ax.set_ylabel('Ramp Rate (MW/5 Min)', fontweight='bold')
ax.set_xlabel('19/May/2024 (UTC) Serres C, Greece', fontweight='bold')

# Set grid lines
ax.grid(True, linestyle=':', alpha=0.5, linewidth=1.5)

# ============================================
# ANNOTATE ONLY EXTERNAL GRID MAX AND MIN VALUES (No Arrows, Placed Just Right of Point)
# ============================================

# Grid Ramp - Max (annotation placed just to the right)
grid_max_idx = df['Grid_Ramp'].idxmax()
grid_max_val = df['Grid_Ramp'].max()
grid_max_time = df.loc[grid_max_idx, 'Time']
ax.annotate(f'Grid Max: {grid_max_val:.2f} MW/5min', 
            xy=(grid_max_time, grid_max_val),
            xytext=(4, -2), textcoords='offset points',
            color='blue', fontsize=12.5, fontweight='bold',
            verticalalignment='center')

# Grid Ramp - Min (annotation placed just to the right)
grid_min_idx = df['Grid_Ramp'].idxmin()
grid_min_val = df['Grid_Ramp'].min()
grid_min_time = df.loc[grid_min_idx, 'Time']
ax.annotate(f'Grid Min: {grid_min_val:.2f} MW/5min', 
            xy=(grid_min_time, grid_min_val),
            xytext=(-45, -5.5), textcoords='offset points',
            color='blue', fontsize=12.5, fontweight='bold',
            verticalalignment='center')

# Legend below the plot
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.37), ncol=2, fontsize=13)

# Format x-axis - NO ROTATION
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.tick_params(axis='x', rotation=0)
ax.tick_params(axis='both', which='major', labelsize=17, width=2)

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(bottom=0.22, top=0.92)

# Save figure
plt.savefig('Ramp_Rates_MW_per_5min_May19_2024_22.pdf', format='pdf', bbox_inches='tight', dpi=300)

# Display plot
plt.show()

# ============================================
# STATISTICS
# ============================================
print("RAMP RATE STATISTICS (MW/5 minutes):")
print("=" * 60)

print("\nLOAD RAMP RATES:")
print("-" * 40)
print(f"Maximum Positive Ramp: {df['Load_Ramp'].max():.3f} MW/5min at {df.loc[df['Load_Ramp'].idxmax(), 'Time'].strftime('%H:%M')}")
print(f"Maximum Negative Ramp: {df['Load_Ramp'].min():.3f} MW/5min at {df.loc[df['Load_Ramp'].idxmin(), 'Time'].strftime('%H:%M')}")
print(f"Mean Ramp Rate: {df['Load_Ramp'].mean():.3f} MW/5min")
print(f"Std Deviation: {df['Load_Ramp'].std():.3f} MW/5min")
print(f"95th Percentile (positive): {df['Load_Ramp'][df['Load_Ramp'] > 0].quantile(0.95):.3f} MW/5min")
print(f"5th Percentile (negative): {df['Load_Ramp'][df['Load_Ramp'] < 0].quantile(0.05):.3f} MW/5min")

print("\nPV RAMP RATES:")
print("-" * 40)
print(f"Maximum Positive Ramp: {df['PV_Ramp'].max():.3f} MW/5min at {df.loc[df['PV_Ramp'].idxmax(), 'Time'].strftime('%H:%M')}")
print(f"Maximum Negative Ramp: {df['PV_Ramp'].min():.3f} MW/5min at {df.loc[df['PV_Ramp'].idxmin(), 'Time'].strftime('%H:%M')}")
print(f"Mean Ramp Rate: {df['PV_Ramp'].mean():.3f} MW/5min")
print(f"Std Deviation: {df['PV_Ramp'].std():.3f} MW/5min")
print(f"95th Percentile (positive): {df['PV_Ramp'][df['PV_Ramp'] > 0].quantile(0.95):.3f} MW/5min")
print(f"5th Percentile (negative): {df['PV_Ramp'][df['PV_Ramp'] < 0].quantile(0.05):.3f} MW/5min")

print("\nGRID RAMP RATES:")
print("-" * 40)
print(f"Maximum Positive Ramp: {df['Grid_Ramp'].max():.3f} MW/5min at {df.loc[df['Grid_Ramp'].idxmax(), 'Time'].strftime('%H:%M')}")
print(f"Maximum Negative Ramp: {df['Grid_Ramp'].min():.3f} MW/5min at {df.loc[df['Grid_Ramp'].idxmin(), 'Time'].strftime('%H:%M')}")
print(f"Mean Ramp Rate: {df['Grid_Ramp'].mean():.3f} MW/5min")
print(f"Std Deviation: {df['Grid_Ramp'].std():.3f} MW/5min")
print(f"95th Percentile (positive): {df['Grid_Ramp'][df['Grid_Ramp'] > 0].quantile(0.95):.3f} MW/5min")
print(f"5th Percentile (negative): {df['Grid_Ramp'][df['Grid_Ramp'] < 0].quantile(0.05):.3f} MW/5min")

print("\nEXTREME RAMP EVENTS (> 2 MW/5min):")
print("=" * 60)
extreme_load = df[abs(df['Load_Ramp']) > 2]
extreme_pv = df[abs(df['PV_Ramp']) > 2]
extreme_grid = df[abs(df['Grid_Ramp']) > 2]

print(f"Load extreme ramps: {len(extreme_load)} events")
if len(extreme_load) > 0:
    print(f"  Max positive: {extreme_load['Load_Ramp'].max():.3f} MW/5min")
    print(f"  Max negative: {extreme_load['Load_Ramp'].min():.3f} MW/5min")

print(f"PV extreme ramps: {len(extreme_pv)} events")
if len(extreme_pv) > 0:
    print(f"  Max positive: {extreme_pv['PV_Ramp'].max():.3f} MW/5min")
    print(f"  Max negative: {extreme_pv['PV_Ramp'].min():.3f} MW/5min")

print(f"Grid extreme ramps: {len(extreme_grid)} events")
if len(extreme_grid) > 0:
    print(f"  Max positive: {extreme_grid['Grid_Ramp'].max():.3f} MW/5min")
    print(f"  Max negative: {extreme_grid['Grid_Ramp'].min():.3f} MW/5min")

print("\nKEY OBSERVATIONS:")
print("=" * 60)
print("• RED line: Load ramp rate (MW/5min)")
print("• ORANGE line: PV ramp rate (MW/5min)")  
print("• BLUE line: Grid ramp rate (MW/5min)")
print("• Positive values = increasing power over 5-minute interval")
print("• Negative values = decreasing power over 5-minute interval")
print("• Grid ramp rates compensate for the mismatch between load and PV")
print("• Blue annotations show max and min ramp rates for External Grid")
