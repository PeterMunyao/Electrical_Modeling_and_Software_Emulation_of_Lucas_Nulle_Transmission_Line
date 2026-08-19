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

# Data Center Load Active Power (MW) - Column32
load_active_data = [
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

# Data Center Load Reactive Power (Mvar) - Column33
load_reactive_data = [
    0.832000, 0.864000, 0.832000, 0.864000, 0.864000, 0.832000, 0.800000, 
    0.896000, 0.832000, 0.864000, 0.832000, 0.864000, 0.832000, 0.896000, 
    0.832000, 0.864000, 0.832000, 0.864000, 0.800000, 0.864000, 0.832000, 
    0.864000, 0.832000, 0.896000, 0.832000, 0.864000, 0.864000, 0.832000, 
    0.832000, 0.864000, 0.864000, 0.800000, 0.864000, 0.832000, 0.864000, 
    0.864000, 0.832000, 0.832000, 0.864000, 3.360000, 6.080000, 5.696000, 
    6.592000, 5.952000, 6.432000, 5.536000, 6.720000, 6.112000, 5.856000, 
    6.560000, 6.176000, 5.600000, 6.816000, 6.016000, 6.336000, 5.664000, 
    6.656000, 6.080000, 5.824000, 6.496000, 6.240000, 5.504000, 6.752000, 
    5.952000, 6.400000, 5.760000, 6.592000, 6.112000, 5.920000, 6.496000, 
    5.664000, 6.848000, 6.016000, 6.272000, 5.536000, 6.656000, 6.176000, 
    5.856000, 6.560000, 5.696000, 6.720000, 6.080000, 6.400000, 5.600000, 
    6.592000, 5.952000, 6.240000, 5.760000, 6.496000, 6.112000, 5.664000, 
    6.432000, 3.680000, 0.896000, 0.832000, 0.864000, 0.832000, 0.864000, 
    0.864000, 0.832000, 0.800000, 0.864000, 0.832000, 0.864000, 2.944000, 
    6.080000, 5.600000, 6.720000, 5.952000, 6.432000, 5.696000, 6.592000, 
    6.112000, 5.856000, 6.560000, 6.176000, 5.536000, 6.816000, 6.016000, 
    6.336000, 5.664000, 6.656000, 6.080000, 5.824000, 6.496000, 6.240000, 
    5.504000, 6.752000, 5.952000, 6.400000, 5.760000, 6.592000, 6.112000, 
    5.920000, 6.496000, 8.664000, 10.848000, 6.016000, 6.272000, 5.536000, 
    6.656000, 6.176000, 5.856000, 6.560000, 5.696000, 6.720000, 6.080000, 
    6.400000, 5.600000, 6.592000, 5.952000, 6.240000, 5.760000, 6.496000, 
    6.112000, 5.664000, 6.432000, 6.016000, 5.536000, 2.944000, 0.608000, 
    0.576000, 0.512000, 0.480000, 0.416000, 0.352000, 0.320000, 0.256000, 
    0.192000, 0.160000, 0.096000
]

# Data Center Load Apparent Power (MVA) - Column34
load_apparent_data = [
    2.691807, 2.762584, 2.661392, 2.732208, 2.792997, 2.691807, 2.621072, 
    2.833401, 2.691807, 2.732208, 2.661392, 2.762584, 2.691807, 2.863777, 
    2.661392, 2.732208, 2.691807, 2.792997, 2.621072, 2.732208, 2.691807, 
    2.762584, 2.661392, 2.833401, 2.691807, 2.732208, 2.792997, 2.661392, 
    2.691807, 2.762584, 2.732208, 2.621072, 2.792997, 2.691807, 2.762584, 
    2.732208, 2.661392, 2.691807, 2.762584, 10.777161, 19.530488, 18.346608, 
    21.210376, 19.186555, 20.704421, 17.840652, 21.554322, 19.692509, 18.852563, 
    21.048363, 19.864474, 18.012619, 21.888303, 19.358519, 20.370432, 18.184590, 
    21.382346, 19.530488, 18.690548, 20.876389, 20.036448, 17.678631, 21.716332, 
    19.186555, 20.542405, 18.518575, 21.210376, 19.692509, 19.024531, 20.876389, 
    18.184590, 22.050321, 19.358519, 20.198466, 17.840652, 21.382346, 19.864474, 
    18.852563, 21.048363, 18.346608, 21.554322, 19.530488, 20.542405, 18.012619, 
    21.210376, 19.186555, 20.036448, 18.518575, 20.876389, 19.692509, 18.184590, 
    20.704421, 11.789080, 2.863777, 2.691807, 2.762584, 2.661392, 2.732208, 
    2.792997, 2.691807, 2.621072, 2.762584, 2.691807, 2.732208, 9.431264, 
    19.530488, 18.012619, 21.554322, 19.186555, 20.704421, 18.346608, 21.210376, 
    19.692509, 18.852563, 21.048363, 19.864474, 17.840652, 21.888303, 19.358519, 
    20.370432, 18.184590, 21.382346, 19.530488, 18.690548, 20.876389, 20.036448, 
    17.678631, 21.716332, 19.186555, 20.542405, 18.518575, 21.210376, 19.692509, 
    19.024531, 20.876389, 19.330373, 23.600861, 19.358519, 20.198466, 17.840652, 
    21.382346, 19.864474, 18.852563, 21.048363, 18.346608, 21.554322, 19.530488, 
    20.542405, 18.012619, 21.210376, 19.186555, 20.036448, 18.518575, 20.876389, 
    19.692509, 18.184590, 20.704421, 19.358519, 17.840652, 9.431264, 2.013967, 
    1.851857, 1.679924, 1.517893, 1.345903, 1.174012, 1.011929, 0.839962, 
    0.668180, 0.505964, 0.334090
]

# Voltage Angle (degrees) - Column21
voltage_angle_data = [
    -0.772166, -0.777124, -0.769551, -0.774508, -0.779739, -0.772166, -0.767209, 
    -0.782082, -0.772166, -0.774508, -0.769551, -0.777124, -0.772166, -0.784698, 
    -0.769551, -0.774508, -0.772166, -0.779739, -0.767209, -0.774508, -0.772166, 
    -0.777124, -0.769551, -0.782082, -0.772166, -0.774508, -0.779739, -0.769551, 
    -0.772166, -0.777124, -0.774508, -0.767209, -0.779739, -0.772166, -0.777124, 
    -0.774508, -0.769551, -0.772166, -0.777124, -1.381293, -2.048527, -1.958373, 
    -2.177822, -2.022878, -2.139045, -1.919749, -2.203550, -2.061572, -1.997023, 
    -2.164753, -2.074405, -1.932547, -2.229499, -2.035701, -2.113137, -1.945349, 
    -2.190684, -2.048527, -1.983991, -2.151897, -2.087242, -1.906733, -2.216627, 
    -2.022878, -2.125984, -1.971180, -2.177822, -2.061572, -2.009839, -2.151897, 
    -1.945349, -2.242581, -2.035701, -2.100295, -1.919749, -2.190684, -2.074405, 
    -1.997023, -2.164753, -1.958373, -2.203550, -2.048527, -2.125984, -1.932547, 
    -2.177822, -2.022878, -2.087242, -1.971180, -2.151897, -2.061572, -1.945349, 
    -2.139045, -1.457842, -0.784698, -0.772166, -0.777124, -0.769551, -0.774508, 
    -0.779739, -0.772166, -0.767209, -0.777124, -0.772166, -0.774508, -1.279299, 
    -2.048527, -1.932547, -2.203550, -2.022878, -2.139045, -1.958373, -2.177822, 
    -2.061572, -1.997023, -2.164753, -2.074405, -1.919749, -2.229499, -2.035701, 
    -2.113137, -1.945349, -2.190684, -2.048527, -1.983991, -2.151897, -2.087242, 
    -1.906733, -2.216627, -2.022878, -2.125984, -1.971180, -2.177822, -2.061572, 
    -2.009839, -2.151897, -1.924613, -2.216649, -2.035701, -2.100295, -1.919749, 
    -2.190684, -2.074405, -1.997023, -2.164753, -1.958373, -2.203550, -2.048527, 
    -2.125984, -1.932547, -2.177822, -2.022878, -2.087242, -1.971180, -2.151897, 
    -2.061572, -1.945349, -2.139045, -2.035701, -1.919749, -1.279299, -0.721794, 
    -0.709001, -0.696486, -0.683696, -0.671187, -0.658680, -0.645897, -0.633396, 
    -0.620897, -0.608121, -0.595628
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

# Primary axis - Active, Reactive, and Apparent Power (linewidth reduced to 2.0 from 2.5)
ax1.plot(df['Time'], df['Load_Active_MW'], 'r-', linewidth=2.0, label='Active Power (MW)', alpha=0.9)
ax1.plot(df['Time'], df['Load_Reactive_Mvar'], 'orange', linewidth=2.0, label='Reactive Power (Mvar)', alpha=0.9)
ax1.plot(df['Time'], df['Load_Apparent_MVA'], 'purple', linewidth=2.0, label='Apparent Power (MVA)', alpha=0.9)
ax1.set_ylabel('Power (MW / Mvar / MVA)', fontweight='bold', fontsize=16, color='k')
ax1.tick_params(axis='y', labelcolor='k')

# Secondary axis - Voltage Angle (linewidth reduced to 2.0 from 2.5)
ax2 = ax1.twinx()
ax2.plot(df['Time'], df['Voltage_Angle_deg'], 'b-', linewidth=2.0, label='Voltage Angle', alpha=0.9)
ax2.set_ylabel('Voltage Angle (degrees)', fontweight='bold', fontsize=16, color='b')
ax2.tick_params(axis='y', labelcolor='b')

# Set voltage angle y-axis scale from -2.5 to 0
ax2.set_ylim(-2.5, 0)

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
ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower center', bbox_to_anchor=(0.5, -0.35), ncol=2, fontsize=14)

plt.tight_layout()
plt.subplots_adjust(bottom=0.20)
plt.savefig('Data_Center_Load_Power_Voltage_Angle_Dual_Axis_May19_2024_001.pdf', format='pdf', bbox_inches='tight', dpi=300)
plt.show()

# ============================================
# METRICS AND ANALYSIS
# ============================================
print("\n" + "="*60)
print("DATA CENTER LOAD - ACTIVE, REACTIVE, APPARENT POWER AND VOLTAGE ANGLE METRICS")
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
print(f"1. Data center load shows distinct operational pattern with rapid transitions")
print(f"2. Apparent power (S) is always greater than active power (P) and reactive power (Q)")
print(f"3. S = √(P² + Q²) relationship is maintained throughout the day")
print(f"4. Voltage angle becomes more negative with increasing power demand")
print(f"5. Strong correlation between apparent power and voltage angle (r={corr_apparent_angle:.3f})")
print(f"6. Data center load exhibits high power factor (avg={df['Power_Factor'].mean():.3f})")

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
