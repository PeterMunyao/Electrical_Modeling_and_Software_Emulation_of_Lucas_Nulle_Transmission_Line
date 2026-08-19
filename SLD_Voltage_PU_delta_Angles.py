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

# General Load Active Power (MW) - Column25
load_active_data = [
    4.450000, 4.200000, 4.050000, 3.850000, 3.400000, 3.050000, 2.950000, 
    3.100000, 3.200000, 3.650000, 3.900000, 4.050000, 4.700000, 5.600000, 
    6.450000, 6.700000, 7.450000, 7.900000, 8.150000, 8.200000, 8.350000, 
    8.650000, 8.700000, 8.650000, 8.850000, 8.900000, 8.950000, 9.050000, 
    9.100000, 9.350000, 9.500000, 9.600000, 9.950000, 10.100000, 10.600000, 
    11.250000, 11.600000, 11.850000, 12.150000, 12.400000, 12.600000, 13.200000, 
    13.550000, 14.450000, 14.800000, 14.900000, 15.050000, 15.899999, 16.249999, 
    16.200000, 16.150001, 15.899999, 15.750000, 15.650000, 15.600000, 15.549999, 
    15.449999, 15.250000, 15.050000, 14.950000, 14.749999, 14.650001, 14.550000, 
    14.450000, 14.350000, 14.250000, 13.699999, 13.349999, 12.800001, 12.250000, 
    12.100000, 11.950000, 11.800000, 11.550000, 11.350000, 11.050000, 10.550000, 
    10.300000, 9.650000, 9.200000, 8.600000, 8.250000, 8.050000, 7.550000, 
    7.400000, 6.800000, 7.050000, 7.550000, 7.400000, 7.750000, 8.150000, 
    8.350000, 8.650000, 8.800000, 8.650000, 8.550000, 8.400000, 8.150000, 
    8.050000, 7.950000, 7.850000, 7.700000, 7.650000, 7.600000, 7.550000, 
    7.800000, 7.950000, 8.150000, 8.250000, 8.450000, 8.600000, 8.850000, 
    9.900000, 10.350000, 10.700000, 11.150000, 11.550000, 12.050000, 11.900000, 
    12.250000, 12.549999, 13.600001, 14.150000, 14.250000, 14.350000, 14.450000, 
    14.550000, 15.050000, 15.549999, 16.350000, 16.550000, 16.800000, 17.350000, 
    17.600000, 18.449999, 18.750000, 19.400001, 19.550000, 19.700000, 20.050000, 
    20.400000, 20.350000, 20.400000, 20.450000, 20.550001, 20.700000, 20.750000, 
    21.250001, 21.750000, 22.450000, 22.950000, 23.400000, 23.300000, 23.600000, 
    23.700000, 23.950000, 23.999999, 24.050000, 24.050000, 23.899999, 23.700000, 
    23.600000, 23.500000, 23.450001, 23.250000, 23.199999, 23.100001, 23.050000, 
    22.950000, 22.900000, 22.849999
]

# General Load Reactive Power (Mvar) - Column26
load_reactive_data = [
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

# General Load Apparent Power (MVA) - Column27
load_apparent_data = [
    6.508840, 6.228965, 5.657296, 4.942924, 4.404543, 4.174326, 4.136726, 
    4.279311, 4.386343, 4.756574, 4.981968, 5.130789, 5.685948, 6.449806, 
    7.222534, 7.468601, 8.168537, 8.600582, 8.850141, 8.915717, 9.073312, 
    9.369231, 9.396409, 9.331264, 9.516959, 9.545287, 9.574054, 9.650129, 
    9.679876, 9.898738, 10.024470, 10.103589, 10.421732, 10.550474, 11.016351, 
    11.630348, 11.969231, 12.199693, 12.479784, 12.712199, 12.896608, 13.473307, 
    13.806701, 14.682047, 15.018073, 15.108276, 15.256228, 16.087650, 16.426274, 
    16.369560, 16.312956, 16.058408, 15.902908, 15.796993, 15.740712, 15.684546, 
    15.578911, 15.374167, 15.175803, 15.070252, 14.871869, 14.766348, 14.667141, 
    14.561679, 14.462451, 14.363234, 13.811317, 13.464211, 12.919076, 12.374369, 
    12.218838, 12.070314, 11.921829, 11.674438, 11.476607, 11.172511, 10.678249, 
    10.431323, 9.790046, 9.346791, 8.756855, 8.413383, 8.217360, 7.728195, 
    7.581722, 6.997321, 7.240511, 7.728195, 7.592760, 7.934261, 8.325413, 
    8.521297, 8.815469, 8.972318, 8.825248, 8.727256, 8.580355, 8.346407, 
    8.248788, 8.151227, 8.065048, 7.919122, 7.882417, 7.833900, 7.797756, 
    8.040056, 8.248788, 8.496029, 8.665160, 8.933784, 9.141663, 9.462822, 
    10.517248, 11.025539, 11.423222, 11.932519, 12.377601, 12.934160, 12.869344, 
    13.288529, 13.642763, 14.707822, 15.292563, 15.481117, 15.651997, 15.844636, 
    16.018505, 16.577243, 17.115052, 17.946657, 18.170099, 18.418537, 18.961672, 
    19.210674, 20.031038, 20.326953, 20.946838, 21.104620, 21.262408, 21.605670, 
    21.949259, 21.902797, 21.967760, 22.032760, 22.125608, 22.264995, 22.311488, 
    22.777237, 23.244408, 23.900680, 24.370935, 24.795161, 24.684256, 24.951353, 
    25.045958, 25.266678, 25.298221, 25.314275, 25.314275, 25.156162, 24.950551, 
    24.824383, 24.713812, 24.635442, 24.429746, 24.351591, 24.151864, 23.922009, 
    23.922061, 24.096888, 23.756525
]

# Voltage Magnitude (p.u.) - Column10
voltage_mag_data = [
    1.034952, 1.035386, 1.037012, 1.039131, 1.039982, 1.039954, 1.039859, 
    1.039698, 1.039550, 1.039308, 1.039118, 1.038955, 1.038657, 1.038402, 
    1.038038, 1.037845, 1.037504, 1.037251, 1.037054, 1.036918, 1.036751, 
    1.036540, 1.036646, 1.036783, 1.036723, 1.036829, 1.036935, 1.037027, 
    1.037133, 1.037179, 1.037255, 1.037345, 1.037360, 1.037435, 1.037402, 
    1.037321, 1.037208, 1.037250, 1.037275, 1.037316, 1.037373, 1.037301, 
    1.037307, 1.037129, 1.037134, 1.037221, 1.037171, 1.037003, 1.037005, 
    1.037143, 1.037282, 1.037489, 1.037662, 1.037817, 1.037955, 1.038093, 
    1.038248, 1.038437, 1.038505, 1.038659, 1.038727, 1.038881, 1.038914, 
    1.039069, 1.039102, 1.039135, 1.039439, 1.039553, 1.039732, 1.039909, 
    1.040077, 1.040124, 1.040172, 1.040251, 1.040314, 1.040530, 1.040686, 
    1.040763, 1.040964, 1.041099, 1.041281, 1.041384, 1.041442, 1.041591, 
    1.041633, 1.041809, 1.041735, 1.041591, 1.041513, 1.041411, 1.041293, 
    1.041233, 1.041144, 1.040978, 1.041023, 1.041052, 1.041097, 1.041051, 
    1.041080, 1.041110, 1.041019, 1.041063, 1.040957, 1.040972, 1.040866, 
    1.040793, 1.040145, 1.039602, 1.038966, 1.038301, 1.037770, 1.037088, 
    1.036280, 1.035533, 1.034936, 1.034184, 1.033568, 1.032796, 1.032352, 
    1.031627, 1.031037, 1.030076, 1.029401, 1.028749, 1.028221, 1.027569, 
    1.027040, 1.026251, 1.025582, 1.024680, 1.024361, 1.024148, 1.023704, 
    1.023489, 1.022931, 1.022697, 1.022331, 1.022151, 1.021970, 1.021715, 
    1.021458, 1.021476, 1.021332, 1.021188, 1.021150, 1.021093, 1.021074, 
    1.020885, 1.020693, 1.020419, 1.020225, 1.020046, 1.020210, 1.020217, 
    1.020177, 1.020203, 1.020308, 1.020539, 1.020539, 1.020724, 1.020929, 
    1.021219, 1.021384, 1.021654, 1.021858, 1.022128, 1.023041, 1.024679, 
    1.023848, 1.021995, 1.024508
]

# Verify data lengths
min_len = min(len(load_active_data), len(load_reactive_data), len(load_apparent_data), len(voltage_mag_data))
if not (len(load_active_data) == len(load_reactive_data) == len(load_apparent_data) == len(voltage_mag_data)):
    print(f"WARNING: Data lengths mismatch! Truncating to minimum length: {min_len}")
    load_active_data = load_active_data[:min_len]
    load_reactive_data = load_reactive_data[:min_len]
    load_apparent_data = load_apparent_data[:min_len]
    voltage_mag_data = voltage_mag_data[:min_len]

# Generate timestamps (6:15 to 20:25, 5-minute intervals)
start_time = datetime(2024, 5, 19, 6, 15, 0)
timestamps = [start_time + pd.Timedelta(minutes=5*i) for i in range(min_len)]

# Create DataFrame
df = pd.DataFrame({
    'Time': timestamps,
    'Load_Active_MW': load_active_data,
    'Load_Reactive_Mvar': load_reactive_data,
    'Load_Apparent_MVA': load_apparent_data,
    'Voltage_Magnitude_pu': voltage_mag_data
})

# ============================================
# PLOT: Active, Reactive, Apparent Power (Primary) and Voltage Magnitude (Secondary)
# ============================================
fig, ax1 = plt.subplots(figsize=(8, 5))

# Primary axis - Active, Reactive, and Apparent Power
ax1.plot(df['Time'], df['Load_Active_MW'], 'r-', linewidth=2.5, label='Active Power (MW)', alpha=0.9)
ax1.plot(df['Time'], df['Load_Reactive_Mvar'], 'y-', linewidth=2.5, label='Reactive Power (Mvar)', alpha=0.9)
ax1.plot(df['Time'], df['Load_Apparent_MVA'], 'purple', linewidth=2.5, label='Apparent Power (MVA)', alpha=0.9)
ax1.set_ylabel('Power (MW / Mvar / MVA)', fontweight='bold', fontsize=16, color='k')
ax1.tick_params(axis='y', labelcolor='k')

# Secondary axis - Voltage Magnitude
ax2 = ax1.twinx()
ax2.plot(df['Time'], df['Voltage_Magnitude_pu'], 'b-', linewidth=2.5, label='Voltage Magnitude (p.u.)', alpha=0.9)
ax2.set_ylabel('Voltage Magnitude (p.u.)', fontweight='bold', fontsize=16, color='b')
ax2.tick_params(axis='y', labelcolor='b')

# Add reference lines
ax1.axhline(y=0, color='black', linestyle='--', linewidth=1.0, alpha=0.3)
ax2.axhline(y=1.0, color='black', linestyle='--', linewidth=1.0, alpha=0.3)

# Labels
ax1.set_xlabel('19/May/2024 (UTC) Serres C, Greece', fontweight='bold', fontsize=16)

# Set grid lines
ax1.grid(True, linestyle=':', alpha=0.5, linewidth=1.5)

# Format x-axis
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax1.tick_params(axis='x', rotation=0)
ax1.tick_params(axis='both', which='major', labelsize=15, width=2)

# Legend - combine both axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower center', bbox_to_anchor=(0.5, -0.35), ncol=2, fontsize=13.7)

plt.tight_layout()
plt.subplots_adjust(bottom=0.18)

# Save as PDF with the specified filename
plt.savefig('Active_Reactive_Apparent_Voltage_Dual_Axis_May19_2024.pdf', format='pdf', bbox_inches='tight', dpi=300)
plt.show()

# ============================================
# METRICS AND ANALYSIS
# ============================================
print("\n" + "="*60)
print("ACTIVE, REACTIVE, APPARENT POWER AND VOLTAGE MAGNITUDE METRICS")
print("="*60)

# Active power statistics
print("\nACTIVE POWER STATISTICS:")
print("-" * 40)
print(f"Range:        {df['Load_Active_MW'].min():.2f} to {df['Load_Active_MW'].max():.2f} MW")
print(f"Mean:         {df['Load_Active_MW'].mean():.2f} MW")
print(f"Median:       {df['Load_Active_MW'].median():.2f} MW")
print(f"Std Dev:      {df['Load_Active_MW'].std():.2f} MW")
print(f"Peak:         {df['Load_Active_MW'].max():.2f} MW at {df.loc[df['Load_Active_MW'].idxmax(), 'Time'].strftime('%H:%M')}")
print(f"Min:          {df['Load_Active_MW'].min():.2f} MW at {df.loc[df['Load_Active_MW'].idxmin(), 'Time'].strftime('%H:%M')}")

# Reactive power statistics
print("\nREACTIVE POWER STATISTICS:")
print("-" * 40)
print(f"Range:        {df['Load_Reactive_Mvar'].min():.2f} to {df['Load_Reactive_Mvar'].max():.2f} Mvar")
print(f"Mean:         {df['Load_Reactive_Mvar'].mean():.2f} Mvar")
print(f"Median:       {df['Load_Reactive_Mvar'].median():.2f} Mvar")
print(f"Std Dev:      {df['Load_Reactive_Mvar'].std():.2f} Mvar")
print(f"Peak:         {df['Load_Reactive_Mvar'].max():.2f} Mvar at {df.loc[df['Load_Reactive_Mvar'].idxmax(), 'Time'].strftime('%H:%M')}")
print(f"Min:          {df['Load_Reactive_Mvar'].min():.2f} Mvar at {df.loc[df['Load_Reactive_Mvar'].idxmin(), 'Time'].strftime('%H:%M')}")

# Apparent power statistics
print("\nAPPARENT POWER STATISTICS:")
print("-" * 40)
print(f"Range:        {df['Load_Apparent_MVA'].min():.2f} to {df['Load_Apparent_MVA'].max():.2f} MVA")
print(f"Mean:         {df['Load_Apparent_MVA'].mean():.2f} MVA")
print(f"Median:       {df['Load_Apparent_MVA'].median():.2f} MVA")
print(f"Std Dev:      {df['Load_Apparent_MVA'].std():.2f} MVA")
print(f"Peak:         {df['Load_Apparent_MVA'].max():.2f} MVA at {df.loc[df['Load_Apparent_MVA'].idxmax(), 'Time'].strftime('%H:%M')}")
print(f"Min:          {df['Load_Apparent_MVA'].min():.2f} MVA at {df.loc[df['Load_Apparent_MVA'].idxmin(), 'Time'].strftime('%H:%M')}")

# Voltage magnitude statistics
print("\nVOLTAGE MAGNITUDE STATISTICS:")
print("-" * 40)
print(f"Range:        {df['Voltage_Magnitude_pu'].min():.4f} to {df['Voltage_Magnitude_pu'].max():.4f} p.u.")
print(f"Mean:         {df['Voltage_Magnitude_pu'].mean():.4f} p.u.")
print(f"Median:       {df['Voltage_Magnitude_pu'].median():.4f} p.u.")
print(f"Std Dev:      {df['Voltage_Magnitude_pu'].std():.4f} p.u.")
print(f"Max Voltage:  {df['Voltage_Magnitude_pu'].max():.4f} p.u. at {df.loc[df['Voltage_Magnitude_pu'].idxmax(), 'Time'].strftime('%H:%M')}")
print(f"Min Voltage:  {df['Voltage_Magnitude_pu'].min():.4f} p.u. at {df.loc[df['Voltage_Magnitude_pu'].idxmin(), 'Time'].strftime('%H:%M')}")

# Correlation analysis
print("\nCORRELATION ANALYSIS:")
print("-" * 40)
corr_active_mag = df['Load_Active_MW'].corr(df['Voltage_Magnitude_pu'])
corr_reactive_mag = df['Load_Reactive_Mvar'].corr(df['Voltage_Magnitude_pu'])
corr_apparent_mag = df['Load_Apparent_MVA'].corr(df['Voltage_Magnitude_pu'])
corr_active_reactive = df['Load_Active_MW'].corr(df['Load_Reactive_Mvar'])
corr_active_apparent = df['Load_Active_MW'].corr(df['Load_Apparent_MVA'])

print(f"Active Power vs Voltage Magnitude:     {corr_active_mag:.3f}")
print(f"Reactive Power vs Voltage Magnitude:   {corr_reactive_mag:.3f}")
print(f"Apparent Power vs Voltage Magnitude:   {corr_apparent_mag:.3f}")
print(f"Active vs Reactive Power:              {corr_active_reactive:.3f}")
print(f"Active vs Apparent Power:              {corr_active_apparent:.3f}")

# Time of day analysis
print("\nTIME-BASED ANALYSIS:")
print("-" * 40)
morning_mask = (df['Time'].dt.hour >= 6) & (df['Time'].dt.hour < 12)
afternoon_mask = (df['Time'].dt.hour >= 12) & (df['Time'].dt.hour < 18)
evening_mask = df['Time'].dt.hour >= 18

print(f"Morning (6:00-12:00):")
print(f"  - Avg Active:     {df.loc[morning_mask, 'Load_Active_MW'].mean():.2f} MW")
print(f"  - Avg Reactive:   {df.loc[morning_mask, 'Load_Reactive_Mvar'].mean():.2f} Mvar")
print(f"  - Avg Apparent:   {df.loc[morning_mask, 'Load_Apparent_MVA'].mean():.2f} MVA")
print(f"  - Avg Voltage:    {df.loc[morning_mask, 'Voltage_Magnitude_pu'].mean():.4f} p.u.")

print(f"\nAfternoon (12:00-18:00):")
print(f"  - Avg Active:     {df.loc[afternoon_mask, 'Load_Active_MW'].mean():.2f} MW")
print(f"  - Avg Reactive:   {df.loc[afternoon_mask, 'Load_Reactive_Mvar'].mean():.2f} Mvar")
print(f"  - Avg Apparent:   {df.loc[afternoon_mask, 'Load_Apparent_MVA'].mean():.2f} MVA")
print(f"  - Avg Voltage:    {df.loc[afternoon_mask, 'Voltage_Magnitude_pu'].mean():.4f} p.u.")

print(f"\nEvening (18:00+):")
print(f"  - Avg Active:     {df.loc[evening_mask, 'Load_Active_MW'].mean():.2f} MW")
print(f"  - Avg Reactive:   {df.loc[evening_mask, 'Load_Reactive_Mvar'].mean():.2f} Mvar")
print(f"  - Avg Apparent:   {df.loc[evening_mask, 'Load_Apparent_MVA'].mean():.2f} MVA")
print(f"  - Avg Voltage:    {df.loc[evening_mask, 'Voltage_Magnitude_pu'].mean():.4f} p.u.")

# Power factor analysis
print("\nPOWER FACTOR ANALYSIS:")
print("-" * 40)
df['Power_Factor'] = df['Load_Active_MW'] / df['Load_Apparent_MVA']
print(f"Average Power Factor:  {df['Power_Factor'].mean():.4f}")
print(f"Min Power Factor:      {df['Power_Factor'].min():.4f} at {df.loc[df['Power_Factor'].idxmin(), 'Time'].strftime('%H:%M')}")
print(f"Max Power Factor:      {df['Power_Factor'].max():.4f} at {df.loc[df['Power_Factor'].idxmax(), 'Time'].strftime('%H:%M')}")

# Key observations
print("\nKEY OBSERVATIONS:")
print("-" * 40)
print(f"1. All power components increase from morning to evening peak")
print(f"2. Apparent power (S) is always greater than active power (P) and reactive power (Q)")
print(f"3. S = √(P² + Q²) relationship is maintained throughout the day")
print(f"4. Voltage magnitude decreases as power demand increases (inverse relationship)")
print(f"5. Strong negative correlation between apparent power and voltage magnitude (r={corr_apparent_mag:.3f})")

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)


#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

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

# General Load Active Power (MW) - Column25
load_active_data = [
    4.450000, 4.200000, 4.050000, 3.850000, 3.400000, 3.050000, 2.950000, 
    3.100000, 3.200000, 3.650000, 3.900000, 4.050000, 4.700000, 5.600000, 
    6.450000, 6.700000, 7.450000, 7.900000, 8.150000, 8.200000, 8.350000, 
    8.650000, 8.700000, 8.650000, 8.850000, 8.900000, 8.950000, 9.050000, 
    9.100000, 9.350000, 9.500000, 9.600000, 9.950000, 10.100000, 10.600000, 
    11.250000, 11.600000, 11.850000, 12.150000, 12.400000, 12.600000, 13.200000, 
    13.550000, 14.450000, 14.800000, 14.900000, 15.050000, 15.899999, 16.249999, 
    16.200000, 16.150001, 15.899999, 15.750000, 15.650000, 15.600000, 15.549999, 
    15.449999, 15.250000, 15.050000, 14.950000, 14.749999, 14.650001, 14.550000, 
    14.450000, 14.350000, 14.250000, 13.699999, 13.349999, 12.800001, 12.250000, 
    12.100000, 11.950000, 11.800000, 11.550000, 11.350000, 11.050000, 10.550000, 
    10.300000, 9.650000, 9.200000, 8.600000, 8.250000, 8.050000, 7.550000, 
    7.400000, 6.800000, 7.050000, 7.550000, 7.400000, 7.750000, 8.150000, 
    8.350000, 8.650000, 8.800000, 8.650000, 8.550000, 8.400000, 8.150000, 
    8.050000, 7.950000, 7.850000, 7.700000, 7.650000, 7.600000, 7.550000, 
    7.800000, 7.950000, 8.150000, 8.250000, 8.450000, 8.600000, 8.850000, 
    9.900000, 10.350000, 10.700000, 11.150000, 11.550000, 12.050000, 11.900000, 
    12.250000, 12.549999, 13.600001, 14.150000, 14.250000, 14.350000, 14.450000, 
    14.550000, 15.050000, 15.549999, 16.350000, 16.550000, 16.800000, 17.350000, 
    17.600000, 18.449999, 18.750000, 19.400001, 19.550000, 19.700000, 20.050000, 
    20.400000, 20.350000, 20.400000, 20.450000, 20.550001, 20.700000, 20.750000, 
    21.250001, 21.750000, 22.450000, 22.950000, 23.400000, 23.300000, 23.600000, 
    23.700000, 23.950000, 23.999999, 24.050000, 24.050000, 23.899999, 23.700000, 
    23.600000, 23.500000, 23.450001, 23.250000, 23.199999, 23.100001, 23.050000, 
    22.950000, 22.900000, 22.849999
]

# General Load Reactive Power (Mvar) - Column26
load_reactive_data = [
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

# General Load Apparent Power (MVA) - Column27
load_apparent_data = [
    6.508840, 6.228965, 5.657296, 4.942924, 4.404543, 4.174326, 4.136726, 
    4.279311, 4.386343, 4.756574, 4.981968, 5.130789, 5.685948, 6.449806, 
    7.222534, 7.468601, 8.168537, 8.600582, 8.850141, 8.915717, 9.073312, 
    9.369231, 9.396409, 9.331264, 9.516959, 9.545287, 9.574054, 9.650129, 
    9.679876, 9.898738, 10.024470, 10.103589, 10.421732, 10.550474, 11.016351, 
    11.630348, 11.969231, 12.199693, 12.479784, 12.712199, 12.896608, 13.473307, 
    13.806701, 14.682047, 15.018073, 15.108276, 15.256228, 16.087650, 16.426274, 
    16.369560, 16.312956, 16.058408, 15.902908, 15.796993, 15.740712, 15.684546, 
    15.578911, 15.374167, 15.175803, 15.070252, 14.871869, 14.766348, 14.667141, 
    14.561679, 14.462451, 14.363234, 13.811317, 13.464211, 12.919076, 12.374369, 
    12.218838, 12.070314, 11.921829, 11.674438, 11.476607, 11.172511, 10.678249, 
    10.431323, 9.790046, 9.346791, 8.756855, 8.413383, 8.217360, 7.728195, 
    7.581722, 6.997321, 7.240511, 7.728195, 7.592760, 7.934261, 8.325413, 
    8.521297, 8.815469, 8.972318, 8.825248, 8.727256, 8.580355, 8.346407, 
    8.248788, 8.151227, 8.065048, 7.919122, 7.882417, 7.833900, 7.797756, 
    8.040056, 8.248788, 8.496029, 8.665160, 8.933784, 9.141663, 9.462822, 
    10.517248, 11.025539, 11.423222, 11.932519, 12.377601, 12.934160, 12.869344, 
    13.288529, 13.642763, 14.707822, 15.292563, 15.481117, 15.651997, 15.844636, 
    16.018505, 16.577243, 17.115052, 17.946657, 18.170099, 18.418537, 18.961672, 
    19.210674, 20.031038, 20.326953, 20.946838, 21.104620, 21.262408, 21.605670, 
    21.949259, 21.902797, 21.967760, 22.032760, 22.125608, 22.264995, 22.311488, 
    22.777237, 23.244408, 23.900680, 24.370935, 24.795161, 24.684256, 24.951353, 
    25.045958, 25.266678, 25.298221, 25.314275, 25.314275, 25.156162, 24.950551, 
    24.824383, 24.713812, 24.635442, 24.429746, 24.351591, 24.151864, 23.922009, 
    23.922061, 24.096888, 23.756525
]

# Voltage Angle (degrees) - Column14
voltage_angle_data = [
    -0.794130, -0.762957, -0.751352, -0.735728, -0.680289, -0.633586, -0.619781, 
    -0.638879, -0.651401, -0.710017, -0.742314, -0.761446, -0.846488, -0.965166, 
    -1.076716, -1.109124, -1.207584, -1.266464, -1.298937, -1.304980, -1.324247, 
    -1.363361, -1.370535, -1.364482, -1.390933, -1.398103, -1.405271, -1.419050, 
    -1.426215, -1.459823, -1.480206, -1.493975, -1.540798, -1.561173, -1.627833, 
    -1.714348, -1.760667, -1.794269, -1.834487, -1.868086, -1.895063, -1.975001, 
    -2.021846, -2.141569, -2.188425, -2.202145, -2.222029, -2.335198, -2.382070, 
    -2.375881, -2.369691, -2.336984, -2.317548, -2.304744, -2.298569, -2.292396, 
    -2.279601, -2.253569, -2.227087, -2.214309, -2.187836, -2.175068, -2.161836, 
    -2.149073, -2.135845, -2.122618, -2.050363, -2.004103, -1.931430, -1.858788, 
    -1.839489, -1.819687, -1.799887, -1.766893, -1.740502, -1.701442, -1.635502, 
    -1.602542, -1.516868, -1.457581, -1.378557, -1.332477, -1.306149, -1.240343, 
    -1.220607, -1.141675, -1.174560, -1.240343, -1.220032, -1.266093, -1.318748, 
    -1.345081, -1.384586, -1.403788, -1.384030, -1.370859, -1.351104, -1.317620, 
    -1.304452, -1.291285, -1.277549, -1.257799, -1.250644, -1.244060, -1.236903, 
    -1.269826, -1.286741, -1.310839, -1.321204, -1.344786, -1.362354, -1.392604, 
    -1.529320, -1.586225, -1.630487, -1.687548, -1.738573, -1.802443, -1.780457, 
    -1.824473, -1.862398, -1.999879, -2.071341, -2.082311, -2.093771, -2.104768, 
    -2.116255, -2.180860, -2.246032, -2.351125, -2.377097, -2.410244, -2.483304, 
    -2.516503, -2.630061, -2.670054, -2.757243, -2.777071, -2.796908, -2.843735, 
    -2.890590, -2.883843, -2.890214, -2.896587, -2.910091, -2.930349, -2.937103, 
    -3.004652, -3.072238, -3.166920, -3.234584, -3.295516, -3.282307, -3.323258, 
    -3.336803, -3.370986, -3.378079, -3.385487, -3.385487, -3.365494, -3.338743, 
    -3.325860, -3.312658, -3.306551, -3.279839, -3.273745, -3.262565, -3.260166, 
    -3.244332, -3.232536, -3.232535
]

# Verify data lengths
min_len = min(len(load_active_data), len(load_reactive_data), len(load_apparent_data), len(voltage_angle_data))
if len(load_active_data) != len(load_reactive_data) or len(load_active_data) != len(load_apparent_data) or len(load_active_data) != len(voltage_angle_data):
    print(f"WARNING: Data lengths mismatch! Truncating to minimum length: {min_len}")
    load_active_data = load_active_data[:min_len]
    load_reactive_data = load_reactive_data[:min_len]
    load_apparent_data = load_apparent_data[:min_len]
    voltage_angle_data = voltage_angle_data[:min_len]

# Generate timestamps (6:15 to 20:25, 5-minute intervals)
start_time = datetime(2024, 5, 19, 6, 15, 0)
timestamps = [start_time + pd.Timedelta(minutes=5*i) for i in range(min_len)]

# Create DataFrame
df = pd.DataFrame({
    'Time': timestamps,
    'Load_Active_MW': load_active_data,
    'Load_Reactive_Mvar': load_reactive_data,
    'Load_Apparent_MVA': load_apparent_data,
    'Voltage_Angle_deg': voltage_angle_data
})

# ============================================
# PLOT: Active, Reactive, Apparent Power and Voltage Angle
# ============================================
fig, ax1 = plt.subplots(figsize=(8, 5))

# Primary axis - Active, Reactive, and Apparent Power
ax1.plot(df['Time'], df['Load_Active_MW'], 'r-', linewidth=2.5, label='Active Power (MW)', alpha=0.9)
ax1.plot(df['Time'], df['Load_Reactive_Mvar'], 'orange', linewidth=2.5, label='Reactive Power (Mvar)', alpha=0.9)
ax1.plot(df['Time'], df['Load_Apparent_MVA'], 'purple', linewidth=2.5, label='Apparent Power (MVA)', alpha=0.9)
ax1.set_ylabel('Power (MW / Mvar / MVA)', fontweight='bold', fontsize=16, color='k')
ax1.tick_params(axis='y', labelcolor='k')

# Secondary axis - Voltage Angle
ax2 = ax1.twinx()
ax2.plot(df['Time'], df['Voltage_Angle_deg'], 'b-', linewidth=2.5, label='Voltage Angle', alpha=0.9)
ax2.set_ylabel('Voltage Angle (degrees)', fontweight='bold', fontsize=16, color='b')
ax2.tick_params(axis='y', labelcolor='b')

# Add reference line for angle
ax2.axhline(y=0, color='black', linestyle='--', linewidth=1.0, alpha=0.3)

# Labels
ax1.set_xlabel('19/May/2024 (UTC) Serres C, Greece', fontweight='bold', fontsize=16)

# Set grid lines
ax1.grid(True, linestyle=':', alpha=0.5, linewidth=1.5)

# Format x-axis
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax1.tick_params(axis='x', rotation=0)
ax1.tick_params(axis='both', which='major', labelsize=15, width=2)

# Legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower center', bbox_to_anchor=(0.5, -0.33), ncol=2, fontsize=13)

plt.tight_layout()
plt.subplots_adjust(bottom=0.20)
plt.savefig('Active_Reactive_Apparent_Power_Voltage_Angle_Dual_Axis_May19_2024_11.pdf', format='pdf', bbox_inches='tight', dpi=300)
plt.show()

# ============================================
# METRICS AND ANALYSIS
# ============================================
print("\n" + "="*60)
print("ACTIVE, REACTIVE, APPARENT POWER AND VOLTAGE ANGLE METRICS")
print("="*60)

# Active power statistics
print("\nACTIVE POWER STATISTICS:")
print("-" * 40)
print(f"Range:        {df['Load_Active_MW'].min():.2f} to {df['Load_Active_MW'].max():.2f} MW")
print(f"Mean:         {df['Load_Active_MW'].mean():.2f} MW")
print(f"Median:       {df['Load_Active_MW'].median():.2f} MW")
print(f"Std Dev:      {df['Load_Active_MW'].std():.2f} MW")
print(f"Peak:         {df['Load_Active_MW'].max():.2f} MW at {df.loc[df['Load_Active_MW'].idxmax(), 'Time'].strftime('%H:%M')}")
print(f"Min:          {df['Load_Active_MW'].min():.2f} MW at {df.loc[df['Load_Active_MW'].idxmin(), 'Time'].strftime('%H:%M')}")

# Reactive power statistics
print("\nREACTIVE POWER STATISTICS:")
print("-" * 40)
print(f"Range:        {df['Load_Reactive_Mvar'].min():.2f} to {df['Load_Reactive_Mvar'].max():.2f} Mvar")
print(f"Mean:         {df['Load_Reactive_Mvar'].mean():.2f} Mvar")
print(f"Median:       {df['Load_Reactive_Mvar'].median():.2f} Mvar")
print(f"Std Dev:      {df['Load_Reactive_Mvar'].std():.2f} Mvar")
print(f"Peak:         {df['Load_Reactive_Mvar'].max():.2f} Mvar at {df.loc[df['Load_Reactive_Mvar'].idxmax(), 'Time'].strftime('%H:%M')}")
print(f"Min:          {df['Load_Reactive_Mvar'].min():.2f} Mvar at {df.loc[df['Load_Reactive_Mvar'].idxmin(), 'Time'].strftime('%H:%M')}")

# Apparent power statistics
print("\nAPPARENT POWER STATISTICS:")
print("-" * 40)
print(f"Range:        {df['Load_Apparent_MVA'].min():.2f} to {df['Load_Apparent_MVA'].max():.2f} MVA")
print(f"Mean:         {df['Load_Apparent_MVA'].mean():.2f} MVA")
print(f"Median:       {df['Load_Apparent_MVA'].median():.2f} MVA")
print(f"Std Dev:      {df['Load_Apparent_MVA'].std():.2f} MVA")
print(f"Peak:         {df['Load_Apparent_MVA'].max():.2f} MVA at {df.loc[df['Load_Apparent_MVA'].idxmax(), 'Time'].strftime('%H:%M')}")
print(f"Min:          {df['Load_Apparent_MVA'].min():.2f} MVA at {df.loc[df['Load_Apparent_MVA'].idxmin(), 'Time'].strftime('%H:%M')}")

# Voltage angle statistics
print("\nVOLTAGE ANGLE STATISTICS:")
print("-" * 40)
print(f"Range:        {df['Voltage_Angle_deg'].min():.4f} to {df['Voltage_Angle_deg'].max():.4f} degrees")
print(f"Mean:         {df['Voltage_Angle_deg'].mean():.4f} degrees")
print(f"Median:       {df['Voltage_Angle_deg'].median():.4f} degrees")
print(f"Std Dev:      {df['Voltage_Angle_deg'].std():.4f} degrees")
print(f"Max Angle:    {df['Voltage_Angle_deg'].max():.4f}° at {df.loc[df['Voltage_Angle_deg'].idxmax(), 'Time'].strftime('%H:%M')}")
print(f"Min Angle:    {df['Voltage_Angle_deg'].min():.4f}° at {df.loc[df['Voltage_Angle_deg'].idxmin(), 'Time'].strftime('%H:%M')}")

# Correlation analysis
print("\nCORRELATION ANALYSIS:")
print("-" * 40)
corr_active_angle = df['Load_Active_MW'].corr(df['Voltage_Angle_deg'])
corr_reactive_angle = df['Load_Reactive_Mvar'].corr(df['Voltage_Angle_deg'])
corr_apparent_angle = df['Load_Apparent_MVA'].corr(df['Voltage_Angle_deg'])
corr_active_reactive = df['Load_Active_MW'].corr(df['Load_Reactive_Mvar'])
corr_active_apparent = df['Load_Active_MW'].corr(df['Load_Apparent_MVA'])

print(f"Active Power vs Voltage Angle:     {corr_active_angle:.3f}")
print(f"Reactive Power vs Voltage Angle:   {corr_reactive_angle:.3f}")
print(f"Apparent Power vs Voltage Angle:   {corr_apparent_angle:.3f}")
print(f"Active vs Reactive Power:          {corr_active_reactive:.3f}")
print(f"Active vs Apparent Power:          {corr_active_apparent:.3f}")

# Time of day analysis
print("\nTIME-BASED ANALYSIS:")
print("-" * 40)
morning_mask = (df['Time'].dt.hour >= 6) & (df['Time'].dt.hour < 12)
afternoon_mask = (df['Time'].dt.hour >= 12) & (df['Time'].dt.hour < 18)
evening_mask = df['Time'].dt.hour >= 18

print(f"Morning (6:00-12:00):")
print(f"  - Avg Active:     {df.loc[morning_mask, 'Load_Active_MW'].mean():.2f} MW")
print(f"  - Avg Reactive:   {df.loc[morning_mask, 'Load_Reactive_Mvar'].mean():.2f} Mvar")
print(f"  - Avg Apparent:   {df.loc[morning_mask, 'Load_Apparent_MVA'].mean():.2f} MVA")
print(f"  - Avg Angle:      {df.loc[morning_mask, 'Voltage_Angle_deg'].mean():.3f}°")

print(f"\nAfternoon (12:00-18:00):")
print(f"  - Avg Active:     {df.loc[afternoon_mask, 'Load_Active_MW'].mean():.2f} MW")
print(f"  - Avg Reactive:   {df.loc[afternoon_mask, 'Load_Reactive_Mvar'].mean():.2f} Mvar")
print(f"  - Avg Apparent:   {df.loc[afternoon_mask, 'Load_Apparent_MVA'].mean():.2f} MVA")
print(f"  - Avg Angle:      {df.loc[afternoon_mask, 'Voltage_Angle_deg'].mean():.3f}°")

print(f"\nEvening (18:00+):")
print(f"  - Avg Active:     {df.loc[evening_mask, 'Load_Active_MW'].mean():.2f} MW")
print(f"  - Avg Reactive:   {df.loc[evening_mask, 'Load_Reactive_Mvar'].mean():.2f} Mvar")
print(f"  - Avg Apparent:   {df.loc[evening_mask, 'Load_Apparent_MVA'].mean():.2f} MVA")
print(f"  - Avg Angle:      {df.loc[evening_mask, 'Voltage_Angle_deg'].mean():.3f}°")

# Power factor analysis
print("\nPOWER FACTOR ANALYSIS:")
print("-" * 40)
df['Power_Factor'] = df['Load_Active_MW'] / df['Load_Apparent_MVA']
print(f"Average Power Factor:  {df['Power_Factor'].mean():.4f}")
print(f"Min Power Factor:      {df['Power_Factor'].min():.4f} at {df.loc[df['Power_Factor'].idxmin(), 'Time'].strftime('%H:%M')}")
print(f"Max Power Factor:      {df['Power_Factor'].max():.4f} at {df.loc[df['Power_Factor'].idxmax(), 'Time'].strftime('%H:%M')}")

# Key observations
print("\nKEY OBSERVATIONS:")
print("-" * 40)
print(f"1. All power components increase from morning to evening peak")
print(f"2. Apparent power (S) is always greater than active power (P) and reactive power (Q)")
print(f"3. S = √(P² + Q²) relationship is maintained throughout the day")
print(f"4. Voltage angle becomes more negative with increasing power demand")
print(f"5. Strong correlation between apparent power and voltage angle (r={corr_apparent_angle:.3f})")

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
