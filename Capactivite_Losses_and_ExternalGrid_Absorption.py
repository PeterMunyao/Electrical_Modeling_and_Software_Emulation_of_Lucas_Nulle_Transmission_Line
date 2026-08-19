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

# External Grid Reactive Power (Mvar) - Column30
# Grid is SINK -> NEGATIVE sign
grid_reactive_data_original = [
    -34.072241, -34.232315, -34.899602, -35.769316, -36.086004, -36.043484, -35.994891, 
    -35.940710, -35.887575, -35.825895, -35.768094, -35.713073, -35.643880, -35.612800, 
    -35.530136, -35.469477, -35.386681, -35.315971, -35.253074, -35.199699, -35.141666, 
    -35.076193, -35.124362, -35.177730, -35.167741, -35.215968, -35.264255, -35.309956, 
    -35.358169, -35.395985, -35.438673, -35.484031, -35.515792, -35.557892, -35.580298, 
    -35.592150, -35.569453, -35.604011, -35.635166, -35.669139, -35.706246, -35.715878, 
    -35.740849, -35.723847, -35.747600, -35.790153, -35.778252, -35.759311, -35.780658, 
    -35.835347, -35.890289, -35.962210, -36.025285, -36.084178, -36.138909, -36.193633, 
    -36.252436, -36.319317, -36.335339, -36.393787, -36.409593, -36.467881, -36.475625, 
    -36.533872, -36.541520, -36.549128, -36.641346, -36.666249, -36.705330, -36.742562, 
    -36.802295, -36.812087, -36.821781, -36.837797, -36.850270, -36.919287, -36.949437, 
    -36.963451, -37.000504, -37.023900, -37.054679, -37.071088, -37.080334, -37.103602, 
    -37.109678, -37.135843, -37.124780, -37.103601, -37.059268, -37.043915, -37.025496, 
    -37.015684, -37.001152, -36.943081, -36.950557, -36.955458, -36.962796, -36.924395, 
    -36.928967, -36.933619, -36.887775, -36.894620, -36.846366, -36.848599, -36.800357, 
    -36.789235, -36.529834, -36.318183, -36.060294, -35.797286, -35.586853, -35.320489, 
    -35.060808, -34.781278, -34.556529, -34.274251, -34.044558, -33.756521, -33.560904, 
    -33.281590, -33.055680, -32.723361, -32.476915, -32.210883, -31.996709, -31.730713, 
    -31.515957, -31.217687, -30.968924, -30.639872, -30.518385, -30.444032, -30.290256, 
    -30.214193, -30.028011, -29.946386, -29.828016, -29.760397, -29.692580, -29.603692, 
    -29.513916, -29.519007, -29.461380, -29.403718, -29.392853, -29.376478, -29.370935, 
    -29.315931, -29.259071, -29.176751, -29.117522, -29.062469, -29.126617, -29.142098, 
    -29.129460, -29.150590, -29.196452, -29.294734, -29.294705, -29.365921, -29.443210, 
    -29.560019, -29.624560, -29.735079, -29.811821, -29.922102, -30.299065, -30.979942, 
    -30.629003, -29.854118, -30.900203
]

# Grid is SINK -> Keep negative sign (as given)
grid_reactive_data = grid_reactive_data_original

# General Load Reactive Power (Mvar) - Column26
# Load is SINK -> NEGATIVE sign
load_reactive_data_original = [
    4.750000, 4.600000, 3.950000, 3.100000, 2.800000, 2.850000, 2.900000, 
    2.950000, 3.000000, 3.050000, 3.100000, 3.150000, 3.200000, 3.200000, 
    3.250000, 3.300000, 3.350000, 3.400000, 3.450000, 3.500000, 3.550000, 
    3.600000, 3.550000, 3.500000, 3.500000, 3.450000, 3.400000, 3.350000, 
    3.300000, 3.250000, 3.200000, 3.150000, 3.100000, 3.050000, 3.000000, 
    2.950000, 2.950000, 2.900000, 2.850000, 2.800000, 2.750000, 2.700000, 
    2.650000, 2.600000, 2.550000, 2.500000, 2.500000, 2.450000, 2.400000, 
    2.350000, 2.300000, 2.250000, 2.200000, 2.150000, 2.100000, 2.050000, 
    2.000000, 1.950000, 1.950000, 1.900000, 1.900000, 1.850000, 1.850000, 
    1.800000, 1.800000, 1.800000, 1.750000, 1.750000, 1.750000, 1.750000, 
    1.700000, 1.700000, 1.700000, 1.700000, 1.700000, 1.650000, 1.650000, 
    1.650000, 1.650000, 1.650000, 1.650000, 1.650000, 1.650000, 1.650000, 
    1.650000, 1.650000, 1.650000, 1.650000, 1.700000, 1.700000, 1.700000, 
    1.700000, 1.700000, 1.750000, 1.750000, 1.750000, 1.750000, 1.800000, 
    1.800000, 1.800000, 1.850000, 1.850000, 1.900000, 1.900000, 1.950000, 
    1.950000, 2.200000, 2.400000, 2.650000, 2.900000, 3.100000, 3.350000, 
    3.550000, 3.800000, 4.000000, 4.250000, 4.450000, 4.700000, 4.900000, 
    5.150000, 5.350000, 5.600000, 5.800000, 6.050000, 6.250000, 6.500000, 
    6.700000, 6.950000, 7.150000, 7.400000, 7.500000, 7.550000, 7.650000, 
    7.700000, 7.800000, 7.850000, 7.900000, 7.950000, 8.000000, 8.050000, 
    8.100000, 8.100000, 8.150000, 8.200000, 8.200000, 8.200000, 8.200000, 
    8.200000, 8.200000, 8.200000, 8.200000, 8.200000, 8.150000, 8.100000, 
    8.100000, 8.050000, 8.000000, 7.900000, 7.900000, 7.850000, 7.800000, 
    7.700000, 7.650000, 7.550000, 7.500000, 7.400000, 7.050000, 6.400000, 
    6.750000, 7.500000, 6.500000
]

# Load is SINK -> Change sign to negative
load_reactive_data = [-x for x in load_reactive_data_original]

# Line Capacitive Losses (Mvar) - Column18
# Capacitors are SOURCE -> POSITIVE sign
loss_data_original = [
    39.410352, 39.427448, 39.491546, 39.575276, 39.608925, 39.607823, 39.604068, 
    39.597689, 39.591831, 39.582269, 39.574751, 39.568326, 39.556530, 39.546460, 
    39.532077, 39.524445, 39.510996, 39.501001, 39.493238, 39.487837, 39.481274, 
    39.472937, 39.477123, 39.482517, 39.480146, 39.484341, 39.488543, 39.492148, 
    39.496345, 39.498155, 39.501136, 39.504722, 39.505299, 39.508245, 39.506964, 
    39.503748, 39.499308, 39.500948, 39.501960, 39.503576, 39.505817, 39.502985, 
    39.503197, 39.496192, 39.496386, 39.499826, 39.497834, 39.491222, 39.491300, 
    39.496744, 39.502213, 39.510401, 39.517204, 39.523336, 39.528795, 39.534254, 
    39.540383, 39.547851, 39.550516, 39.556625, 39.559283, 39.565384, 39.566703, 
    39.572806, 39.574121, 39.575434, 39.587466, 39.591959, 39.599069, 39.606070, 
    39.612687, 39.614579, 39.616466, 39.619609, 39.622101, 39.630622, 39.636827, 
    39.639849, 39.647829, 39.653193, 39.660376, 39.664455, 39.666785, 39.672665, 
    39.674354, 39.681334, 39.678400, 39.672665, 39.669576, 39.665532, 39.660860, 
    39.658480, 39.654945, 39.648370, 39.650150, 39.651332, 39.653108, 39.651281, 
    39.652442, 39.653613, 39.650003, 39.651754, 39.647552, 39.648133, 39.643933, 
    39.641036, 39.615375, 39.593887, 39.568769, 39.542461, 39.521501, 39.494562, 
    39.462697, 39.433253, 39.409703, 39.380109, 39.355851, 39.325508, 39.308077, 
    39.279577, 39.256449, 39.218737, 39.192301, 39.166761, 39.146097, 39.120592, 
    39.099900, 39.069083, 39.042966, 39.007761, 38.995323, 38.987027, 38.969743, 
    38.961335, 38.939614, 38.930504, 38.916290, 38.909267, 38.902231, 38.892299, 
    38.882312, 38.883017, 38.877419, 38.871818, 38.870349, 38.868142, 38.867400, 
    38.860046, 38.852576, 38.841958, 38.834402, 38.827486, 38.833851, 38.834115, 
    38.832551, 38.833559, 38.837638, 38.846599, 38.846596, 38.853798, 38.861765, 
    38.873034, 38.879438, 38.889933, 38.897875, 38.908356, 38.943921, 39.007718, 
    38.975328, 38.903219, 39.001070
]

# Capacitors are SOURCE -> Keep positive sign
loss_data = loss_data_original

# Verify data lengths
print("DATA VERIFICATION AND SIGN ASSIGNMENT:")
print("=" * 60)
print("SIGN CONVENTION (Source = Positive, Sink = Negative):")
print("-" * 60)
print(f"External Grid: SINK   -> NEGATIVE sign (absorbing)")
print(f"General Load:  SINK   -> NEGATIVE sign (consuming)")
print(f"Capacitors:    SOURCE -> POSITIVE sign (generating)")
print("-" * 60)
print(f"Grid Reactive Data length:   {len(grid_reactive_data)}")
print(f"Load Reactive Data length:    {len(load_reactive_data)}")
print(f"Loss Data length:             {len(loss_data)}")

# Ensure all data lengths match
min_len = min(len(grid_reactive_data), len(load_reactive_data), len(loss_data))
if len(grid_reactive_data) != len(load_reactive_data) or len(grid_reactive_data) != len(loss_data):
    print(f"\nWARNING: Data lengths mismatch! Truncating to minimum length: {min_len}")
    grid_reactive_data = grid_reactive_data[:min_len]
    load_reactive_data = load_reactive_data[:min_len]
    loss_data = loss_data[:min_len]

# Generate timestamps (6:15 to 20:25, 5-minute intervals)
start_time = datetime(2024, 5, 19, 6, 15, 0)
timestamps = [start_time + pd.Timedelta(minutes=5*i) for i in range(min_len)]

# Create DataFrame
df = pd.DataFrame({
    'Time': timestamps,
    'Grid_Reactive_Mvar': grid_reactive_data,
    'Load_Reactive_Mvar': load_reactive_data,
    'Loss_Reactive_Mvar': loss_data
})

# Calculate reactive power balance: Sources + Sinks = 0
# Sources: Capacitors (positive)
# Sinks: Grid (negative) + Load (negative)
df['Reactive_Balance'] = df['Grid_Reactive_Mvar'] + df['Load_Reactive_Mvar'] + df['Loss_Reactive_Mvar']
df['Total_Sources'] = df['Loss_Reactive_Mvar']
df['Total_Sinks'] = abs(df['Grid_Reactive_Mvar']) + abs(df['Load_Reactive_Mvar'])

# ============================================
# SINGLE PLOT: Reactive Power Sources and Sinks
# ============================================
fig, ax = plt.subplots(figsize=(7, 5))

# Plot reactive power components
ax.plot(df['Time'], df['Grid_Reactive_Mvar'], 'b-', linewidth=2.5, label='External Grid (Sink)', alpha=0.9)
ax.plot(df['Time'], df['Load_Reactive_Mvar'], 'r-', linewidth=2.5, label='General Load (Sink)', alpha=0.9)
ax.plot(df['Time'], df['Loss_Reactive_Mvar'], 'purple', linewidth=2.5, label='Line Capacitive Losses (Source)', alpha=0.9)

# Fill areas for better visualization
ax.fill_between(df['Time'], df['Grid_Reactive_Mvar'], 0, where=(df['Grid_Reactive_Mvar'] < 0), 
                 color='blue', alpha=0.15, label='Grid Absorption')
ax.fill_between(df['Time'], df['Load_Reactive_Mvar'], 0, where=(df['Load_Reactive_Mvar'] < 0), 
                 color='red', alpha=0.15, label='Load Consumption')
ax.fill_between(df['Time'], 0, df['Loss_Reactive_Mvar'], where=(df['Loss_Reactive_Mvar'] > 0), 
                 color='purple', alpha=0.15, label='Capacitive Generation')

# Add zero reference line
ax.axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.4)

# Labels with better formatting
ax.set_ylabel('Reactive Power (MVAR)', fontweight='bold', fontsize=16)
ax.set_xlabel('19/May/2024 (UTC) Serres C, Greece', fontweight='bold', fontsize=16)

# Set grid lines
ax.grid(True, linestyle=':', alpha=0.5, linewidth=1.5)

# Legend below the plot
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.41), ncol=2, fontsize=12)

# Format x-axis - NO ROTATION
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.tick_params(axis='x', rotation=0)
ax.tick_params(axis='both', which='major', labelsize=15, width=2)

# Adjust layout to accommodate legend
plt.tight_layout()
plt.subplots_adjust(bottom=0.22)

# Save figure
plt.savefig('Reactive_Power_Grid_Sink_May19_2024.pdf', format='pdf', bbox_inches='tight', dpi=300)

# Display plot
plt.show()

# ============================================
# REACTIVE POWER METRICS AND VERIFICATION
# ============================================
print("\n" + "="*60)
print("REACTIVE POWER METRICS AND VERIFICATION")
print("="*60)

# Basic statistics
print("\nBASIC STATISTICS (Source = Positive, Sink = Negative):")
print("-" * 40)
print(f"External Grid (SINK):")
print(f"  - Range: {df['Grid_Reactive_Mvar'].min():.2f} to {df['Grid_Reactive_Mvar'].max():.2f} Mvar")
print(f"  - Mean:  {df['Grid_Reactive_Mvar'].mean():.2f} Mvar")
print(f"  - Peak Absorption: {abs(df['Grid_Reactive_Mvar'].min()):.2f} Mvar at {df.loc[df['Grid_Reactive_Mvar'].idxmin(), 'Time'].strftime('%H:%M')}")
print(f"  - Min Absorption: {abs(df['Grid_Reactive_Mvar'].max()):.2f} Mvar at {df.loc[df['Grid_Reactive_Mvar'].idxmax(), 'Time'].strftime('%H:%M')}")

print(f"\nGeneral Load (SINK):")
print(f"  - Range: {df['Load_Reactive_Mvar'].min():.2f} to {df['Load_Reactive_Mvar'].max():.2f} Mvar")
print(f"  - Mean:  {df['Load_Reactive_Mvar'].mean():.2f} Mvar")
print(f"  - Peak Consumption: {abs(df['Load_Reactive_Mvar'].min()):.2f} Mvar at {df.loc[df['Load_Reactive_Mvar'].idxmin(), 'Time'].strftime('%H:%M')}")
print(f"  - Min Consumption: {abs(df['Load_Reactive_Mvar'].max()):.2f} Mvar at {df.loc[df['Load_Reactive_Mvar'].idxmax(), 'Time'].strftime('%H:%M')}")

print(f"\nCapacitive Losses (SOURCE):")
print(f"  - Range: {df['Loss_Reactive_Mvar'].min():.2f} to {df['Loss_Reactive_Mvar'].max():.2f} Mvar")
print(f"  - Mean:  {df['Loss_Reactive_Mvar'].mean():.2f} Mvar")
print(f"  - Peak Generation: {df['Loss_Reactive_Mvar'].max():.2f} Mvar at {df.loc[df['Loss_Reactive_Mvar'].idxmax(), 'Time'].strftime('%H:%M')}")

# Reactive power balance
avg_grid_absorption = abs(df['Grid_Reactive_Mvar'].mean())
avg_load_consumption = abs(df['Load_Reactive_Mvar'].mean())
avg_loss_generation = df['Loss_Reactive_Mvar'].mean()

print("\nREACTIVE POWER BALANCE:")
print("-" * 40)
print(f"Average Grid Absorption:        {avg_grid_absorption:.2f} Mvar")
print(f"Average Load Consumption:       {avg_load_consumption:.2f} Mvar")
print(f"Average Capacitive Generation:  {avg_loss_generation:.2f} Mvar")
print(f"Total Sinks (Grid + Load):      {avg_grid_absorption + avg_load_consumption:.2f} Mvar")
print(f"Total Sources (Capacitors):     {avg_loss_generation:.2f} Mvar")
print(f"Net Balance (Sources - Sinks):  {avg_loss_generation - (avg_grid_absorption + avg_load_consumption):.2f} Mvar")
print(f"Balance Status:                 {'✓ CLOSED' if abs(avg_loss_generation - (avg_grid_absorption + avg_load_consumption)) < 0.1 else '⚠ OPEN'}")

# Contribution analysis
print("\nCONTRIBUTION ANALYSIS:")
print("-" * 40)
total_sinks = abs(df['Grid_Reactive_Mvar'].sum()) + abs(df['Load_Reactive_Mvar'].sum())
total_sources = df['Loss_Reactive_Mvar'].sum()
print(f"Total Reactive Sinks:           {total_sinks:.2f} Mvar")
print(f"Total Reactive Sources:         {total_sources:.2f} Mvar")
print(f"Grid Absorption Share:          {abs(df['Grid_Reactive_Mvar'].sum())/total_sinks*100:.1f}%")
print(f"Load Consumption Share:         {abs(df['Load_Reactive_Mvar'].sum())/total_sinks*100:.1f}%")

# Variation metrics
print("\nVARIATION METRICS:")
print("-" * 40)
print(f"Grid Variability: {abs(df['Grid_Reactive_Mvar'].max() - df['Grid_Reactive_Mvar'].min()):.2f} Mvar")
print(f"Load Variability: {abs(df['Load_Reactive_Mvar'].max() - df['Load_Reactive_Mvar'].min()):.2f} Mvar")
print(f"Grid Peak/Avg Ratio: {abs(df['Grid_Reactive_Mvar'].min())/abs(df['Grid_Reactive_Mvar'].mean()):.2f}")
print(f"Load Peak/Avg Ratio: {abs(df['Load_Reactive_Mvar'].min())/abs(df['Load_Reactive_Mvar'].mean()):.2f}")

# Time of day analysis
print("\nTIME-BASED ANALYSIS:")
print("-" * 40)
morning_mask = (df['Time'].dt.hour >= 6) & (df['Time'].dt.hour < 12)
afternoon_mask = (df['Time'].dt.hour >= 12) & (df['Time'].dt.hour < 18)
evening_mask = df['Time'].dt.hour >= 18

print(f"Morning (6:00-12:00):")
print(f"  - Avg Grid Absorption:     {abs(df.loc[morning_mask, 'Grid_Reactive_Mvar'].mean()):.2f} Mvar")
print(f"  - Avg Load Consumption:    {abs(df.loc[morning_mask, 'Load_Reactive_Mvar'].mean()):.2f} Mvar")
print(f"  - Avg Capacitive Gen:      {df.loc[morning_mask, 'Loss_Reactive_Mvar'].mean():.2f} Mvar")

print(f"\nAfternoon (12:00-18:00):")
print(f"  - Avg Grid Absorption:     {abs(df.loc[afternoon_mask, 'Grid_Reactive_Mvar'].mean()):.2f} Mvar")
print(f"  - Avg Load Consumption:    {abs(df.loc[afternoon_mask, 'Load_Reactive_Mvar'].mean()):.2f} Mvar")
print(f"  - Avg Capacitive Gen:      {df.loc[afternoon_mask, 'Loss_Reactive_Mvar'].mean():.2f} Mvar")

print(f"\nEvening (18:00+):")
print(f"  - Avg Grid Absorption:     {abs(df.loc[evening_mask, 'Grid_Reactive_Mvar'].mean()):.2f} Mvar")
print(f"  - Avg Load Consumption:    {abs(df.loc[evening_mask, 'Load_Reactive_Mvar'].mean()):.2f} Mvar")
print(f"  - Avg Capacitive Gen:      {df.loc[evening_mask, 'Loss_Reactive_Mvar'].mean():.2f} Mvar")

# System efficiency
print("\nSYSTEM EFFICIENCY METRICS:")
print("-" * 40)
print(f"Capacitive Support Ratio:     {avg_loss_generation/(avg_grid_absorption + avg_load_consumption)*100:.1f}%")
print(f"Grid/Load Sink Ratio:         {avg_grid_absorption/avg_load_consumption:.2f}")
print(f"Reactive Power Balance:       {'Surplus' if avg_loss_generation > avg_grid_absorption + avg_load_consumption else 'Deficit'}")

# Verification check
print("\nBALANCE VERIFICATION:")
print("-" * 40)
max_balance_error = df['Reactive_Balance'].abs().max()
mean_balance_error = df['Reactive_Balance'].abs().mean()
print(f"Maximum Instant Balance Error: {max_balance_error:.4f} Mvar")
print(f"Mean Balance Error:            {mean_balance_error:.4f} Mvar")
print(f"Verification Status:           {'✓ PASSED' if max_balance_error < 0.5 else '⚠ CHECK NEEDED'}")

print("\n" + "="*60)
print("REACTIVE POWER ANALYSIS COMPLETE")
print("="*60)
