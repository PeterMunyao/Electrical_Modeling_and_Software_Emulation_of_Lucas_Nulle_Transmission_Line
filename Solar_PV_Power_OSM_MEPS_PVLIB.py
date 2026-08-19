import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pvlib
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PV POWER CALCULATION FOR MAY 19, 2024 (5:00 - 20:00)
# ============================================================================

def calculate_pv_power_may19(file_path, target_date='2024-05-19'):
    """
    Calculate PV power for May 19, 2024 using both methods
    Time range: 5:00 to 20:00 (UTC+3)
    """
    print("\n" + "="*80)
    print(f"PV POWER CALCULATION - {target_date}")
    print("Time Range: 5:00 to 20:00 (UTC+3)")
    print("="*80)
    
    # Load data
    df = pd.read_csv(file_path)
    df['period_end'] = pd.to_datetime(df['period_end'])
    df.set_index('period_end', inplace=True)
    
    # Convert to UTC+3
    df.index = df.index + pd.Timedelta(hours=3)
    
    # Filter for specific date
    df = df[df.index.date == pd.Timestamp(target_date).date()]
    
    # Filter for extended daylight hours (5 AM to 8 PM)
    df = df[(df.index.hour >= 5) & (df.index.hour <= 20)]
    
    print(f"\nLoaded {len(df)} timesteps for {target_date}")
    print(f"Time range: {df.index[0]} to {df.index[-1]}")
    
    # === System configuration ===
    tilt = 25
    azimuth = 180
    panel_power_max = 390  # W
    system_capacity_kw = 1010.88
    inverter_efficiency = 0.99
    temp_coeff = -0.005
    stc_irradiance = 1000  # W/m²
    
    num_panels = int(system_capacity_kw * 1000 / panel_power_max)
    
    print(f"\nSystem Configuration:")
    print(f"  Panels: {num_panels}")
    print(f"  Capacity: {system_capacity_kw} kW")
    print(f"  Inverter Efficiency: {inverter_efficiency*100}%")
    print(f"  Temperature Coefficient: {temp_coeff*100}%/°C")
    
    # === PVLIB Method ===
    print("\n" + "-"*40)
    print("PVLIB METHOD")
    print("-"*40)
    
    solar_position = pvlib.solarposition.get_solarposition(df.index, 40.886273, 23.912687)
    
    poa = pvlib.irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=azimuth,
        dni=df['dni'],
        ghi=df['ghi'],
        dhi=df['dhi'],
        solar_zenith=solar_position['apparent_zenith'],
        solar_azimuth=solar_position['azimuth']
    )
    poa_irradiance = poa['poa_global']
    
    # SAPM temperature model
    temp_cell = pvlib.temperature.sapm_cell(
        poa_irradiance, df['air_temp'], df['wind_speed_10m'], -3.47, -0.0594, 3
    )
    
    dc_power_pvlib = (poa_irradiance / stc_irradiance * 
                      num_panels * panel_power_max * 
                      (1 + temp_coeff * (temp_cell - 25)))
    ac_power_pvlib = dc_power_pvlib * inverter_efficiency
    
    # Ensure no negative values
    ac_power_pvlib = np.maximum(ac_power_pvlib, 0)
    
    # === OSM-MEPS Method ===
    print("\n" + "-"*40)
    print("OSM-MEPS METHOD")
    print("-"*40)
    
    tilt_rad = np.radians(tilt)
    azimuth_panel_rad = np.radians(azimuth)
    
    # Solar position already calculated above
    zenith_rad = np.radians(solar_position['apparent_zenith'])
    azimuth_rad = np.radians(solar_position['azimuth'])
    
    # Angle of incidence
    aoi = np.degrees(np.arccos(
        np.cos(zenith_rad) * np.cos(tilt_rad) +
        np.sin(zenith_rad) * np.sin(tilt_rad) * 
        np.cos(azimuth_rad - azimuth_panel_rad)
    ))
    aoi = np.clip(aoi, 0, 180)
    
    # POA components
    poa_direct = df['dni'] * np.cos(np.radians(aoi)) * (1 - df['cloud_opacity'] / 100)
    poa_direct = poa_direct.clip(lower=0)
    poa_diffuse = df['dhi'] * (1 + np.cos(tilt_rad)) / 2
    poa_sky_diffuse = df['ghi'] * df['albedo'] * (1 - np.cos(tilt_rad)) / 2
    poa_total = poa_direct + poa_diffuse + poa_sky_diffuse
    
    # Module temperature
    nominal_operating_cell_temp = 45
    module_temp = nominal_operating_cell_temp + poa_total / 800 * (28 - df['air_temp'])
    
    # DC power calculation
    dc_power_osmmeps = panel_power_max * (1 + temp_coeff * (module_temp - 25))
    dc_power_osmmeps *= poa_total / stc_irradiance
    dc_power_osmmeps *= (1 - 0.0005 * df['relative_humidity'])
    
    # AC power with inverter efficiency
    ac_power_osmmeps = dc_power_osmmeps * inverter_efficiency
    
    # Scale to system and apply losses
    scaled_power = ac_power_osmmeps * num_panels
    actual_power = scaled_power * (1 - 0.10)  # Empirical losses
    
    # Ensure no negative values
    actual_power = np.maximum(actual_power, 0)
    
    # === Create Results DataFrames ===
    print("\n" + "-"*40)
    print("CREATING RESULTS")
    print("-"*40)
    
    # PVLIB results
    df_pvlib = pd.DataFrame({
        'Time': df.index.strftime('%H:%M'),
        'P (MW)': (ac_power_pvlib / 1e6).round(3),
        'Q (MVAr)': 0
    })
    df_pvlib = df_pvlib[df_pvlib['P (MW)'] > 0]
    
    # OSM-MEPS results
    df_osmmeps = pd.DataFrame({
        'Time': df.index.strftime('%H:%M'),
        'P (MW)': (actual_power / 1e6).round(3),
        'Q (MVAr)': 0
    })
    df_osmmeps = df_osmmeps[df_osmmeps['P (MW)'] > 0]
    
    # Print statistics
    print(f"\nPVLIB Results:")
    print(f"  Timesteps: {len(df_pvlib)}")
    print(f"  Peak Power: {df_pvlib['P (MW)'].max():.3f} MW")
    print(f"  Total Energy: {df_pvlib['P (MW)'].sum() * (5/60):.2f} MWh")
    
    print(f"\nOSM-MEPS Results:")
    print(f"  Timesteps: {len(df_osmmeps)}")
    print(f"  Peak Power: {df_osmmeps['P (MW)'].max():.3f} MW")
    print(f"  Total Energy: {df_osmmeps['P (MW)'].sum() * (5/60):.2f} MWh")
    
    return df_pvlib, df_osmmeps, df

# ============================================================================
# SAVE RESULTS TO CSV
# ============================================================================

def save_results(df_pvlib, df_osmmeps, target_date='2024-05-19'):
    """
    Save results to CSV files
    """
    print("\n" + "="*80)
    print("SAVING RESULTS")
    print("="*80)
    
    # Save PVLIB results
    filename_pvlib = f'pv_power_{target_date}_PVLIB_5to20.csv'
    df_pvlib[['Time', 'P (MW)', 'Q (MVAr)']].to_csv(filename_pvlib, index=False)
    print(f"\nPVLIB results saved to '{filename_pvlib}'")
    print(f"  Total timesteps: {len(df_pvlib)}")
    
    # Save OSM-MEPS results
    filename_osmmeps = f'pv_power_{target_date}_OSM-MEPS_5to20.csv'
    df_osmmeps[['Time', 'P (MW)', 'Q (MVAr)']].to_csv(filename_osmmeps, index=False)
    print(f"OSM-MEPS results saved to '{filename_osmmeps}'")
    print(f"  Total timesteps: {len(df_osmmeps)}")
    
    # Create comparison CSV
    if len(df_pvlib) > 0 and len(df_osmmeps) > 0:
        comparison_df = pd.merge(
            df_pvlib[['Time', 'P (MW)']],
            df_osmmeps[['Time', 'P (MW)']],
            on='Time',
            suffixes=('_PVLIB', '_OSM-MEPS')
        )
        comparison_df['Q (MVAr)_PVLIB'] = 0
        comparison_df['Q (MVAr)_OSM-MEPS'] = 0
        
        # Reorder columns
        comparison_df = comparison_df[[
            'Time',
            'P (MW)_PVLIB', 'Q (MVAr)_PVLIB',
            'P (MW)_OSM-MEPS', 'Q (MVAr)_OSM-MEPS'
        ]]
        
        filename_comparison = f'pv_power_comparison_{target_date}_PVLIB_vs_OSM-MEPS_5to20.csv'
        comparison_df.to_csv(filename_comparison, index=False)
        print(f"Comparison saved to '{filename_comparison}'")
        return filename_pvlib, filename_osmmeps, filename_comparison
    else:
        print("Warning: One or both methods have no data for comparison")
        return filename_pvlib, filename_osmmeps, None

# ============================================================================
# PLOT RESULTS
# ============================================================================

def plot_results(df_pvlib, df_osmmeps, target_date='2024-05-19'):
    """
    Plot PV power profiles for both methods
    """
    if len(df_pvlib) == 0 and len(df_osmmeps) == 0:
        print("No data to plot!")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f'PV Power Comparison - {target_date} (5:00 - 20:00 UTC+3)', 
                 fontsize=16, fontweight='bold')
    
    # Plot 1: PVLIB Power Profile
    ax = axes[0, 0]
    if len(df_pvlib) > 0:
        x = np.arange(len(df_pvlib))
        ax.plot(x, df_pvlib['P (MW)'], 'b-', linewidth=2)
        ax.fill_between(x, 0, df_pvlib['P (MW)'], alpha=0.3, color='blue')
        # Set x-ticks at 1-hour intervals
        tick_indices = np.arange(0, len(df_pvlib), 12)  # Every 12 timesteps = 1 hour
        ax.set_xticks(tick_indices)
        ax.set_xticklabels(df_pvlib['Time'].iloc[tick_indices].values, rotation=45)
    ax.set_xlabel('Time')
    ax.set_ylabel('Power (MW)')
    ax.set_title('PVLIB Method')
    ax.grid(True, alpha=0.3)
    
    # Plot 2: OSM-MEPS Power Profile
    ax = axes[0, 1]
    if len(df_osmmeps) > 0:
        x = np.arange(len(df_osmmeps))
        ax.plot(x, df_osmmeps['P (MW)'], 'r-', linewidth=2)
        ax.fill_between(x, 0, df_osmmeps['P (MW)'], alpha=0.3, color='red')
        tick_indices = np.arange(0, len(df_osmmeps), 12)
        ax.set_xticks(tick_indices)
        ax.set_xticklabels(df_osmmeps['Time'].iloc[tick_indices].values, rotation=45)
    ax.set_xlabel('Time')
    ax.set_ylabel('Power (MW)')
    ax.set_title('OSM-MEPS Method')
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Comparison
    ax = axes[1, 0]
    if len(df_pvlib) > 0 and len(df_osmmeps) > 0:
        merged = pd.merge(df_pvlib, df_osmmeps, on='Time', suffixes=('_PVLIB', '_OSM-MEPS'))
        if len(merged) > 0:
            x = np.arange(len(merged))
            ax.plot(x, merged['P (MW)_PVLIB'], 'b-', label='PVLIB', linewidth=2)
            ax.plot(x, merged['P (MW)_OSM-MEPS'], 'r-', label='OSM-MEPS', linewidth=2)
            tick_indices = np.arange(0, len(merged), 12)
            ax.set_xticks(tick_indices)
            ax.set_xticklabels(merged['Time'].iloc[tick_indices].values, rotation=45)
    ax.set_xlabel('Time')
    ax.set_ylabel('Power (MW)')
    ax.set_title('Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Difference
    ax = axes[1, 1]
    if len(df_pvlib) > 0 and len(df_osmmeps) > 0:
        merged = pd.merge(df_pvlib, df_osmmeps, on='Time', suffixes=('_PVLIB', '_OSM-MEPS'))
        if len(merged) > 0:
            diff = merged['P (MW)_PVLIB'] - merged['P (MW)_OSM-MEPS']
            x = np.arange(len(merged))
            colors = ['g' if d >= 0 else 'r' for d in diff]
            ax.bar(x, diff, color=colors, alpha=0.6)
            ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            tick_indices = np.arange(0, len(merged), 12)
            ax.set_xticks(tick_indices)
            ax.set_xticklabels(merged['Time'].iloc[tick_indices].values, rotation=45)
    ax.set_xlabel('Time')
    ax.set_ylabel('Power Difference (MW)')
    ax.set_title('PVLIB - OSM-MEPS')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# PRINT SUMMARY STATISTICS
# ============================================================================

def print_summary(df_pvlib, df_osmmeps, target_date='2024-05-19'):
    """
    Print summary statistics
    """
    print("\n" + "="*80)
    print(f"SUMMARY STATISTICS - {target_date} (5:00 - 20:00)")
    print("="*80)
    
    print(f"\n{'Metric':<30} {'PVLIB':<15} {'OSM-MEPS':<15} {'Difference':<15}")
    print("-" * 75)
    
    # Peak Power
    peak_pvlib = df_pvlib['P (MW)'].max() if len(df_pvlib) > 0 else 0
    peak_osmmeps = df_osmmeps['P (MW)'].max() if len(df_osmmeps) > 0 else 0
    print(f"{'Peak Power (MW)':<30} {peak_pvlib:<15.3f} {peak_osmmeps:<15.3f} {peak_pvlib - peak_osmmeps:<15.3f}")
    
    # Average Power
    mean_pvlib = df_pvlib['P (MW)'].mean() if len(df_pvlib) > 0 else 0
    mean_osmmeps = df_osmmeps['P (MW)'].mean() if len(df_osmmeps) > 0 else 0
    print(f"{'Average Power (MW)':<30} {mean_pvlib:<15.3f} {mean_osmmeps:<15.3f} {mean_pvlib - mean_osmmeps:<15.3f}")
    
    # Total Energy
    energy_pvlib = df_pvlib['P (MW)'].sum() * (5/60) if len(df_pvlib) > 0 else 0
    energy_osmmeps = df_osmmeps['P (MW)'].sum() * (5/60) if len(df_osmmeps) > 0 else 0
    print(f"{'Total Energy (MWh)':<30} {energy_pvlib:<15.2f} {energy_osmmeps:<15.2f} {energy_pvlib - energy_osmmeps:<15.2f}")
    
    # Number of Timesteps
    timesteps_pvlib = len(df_pvlib) if len(df_pvlib) > 0 else 0
    timesteps_osmmeps = len(df_osmmeps) if len(df_osmmeps) > 0 else 0
    print(f"{'Timesteps':<30} {timesteps_pvlib:<15} {timesteps_osmmeps:<15} {timesteps_pvlib - timesteps_osmmeps:<15}")
    
    # Correlation if both have data
    if len(df_pvlib) > 0 and len(df_osmmeps) > 0:
        merged = pd.merge(df_pvlib, df_osmmeps, on='Time', suffixes=('_PVLIB', '_OSM-MEPS'))
        if len(merged) > 0:
            correlation = merged['P (MW)_PVLIB'].corr(merged['P (MW)_OSM-MEPS'])
            print(f"\nCorrelation between PVLIB and OSM-MEPS: {correlation:.4f}")
    
    print("="*80)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    file_path = "csv_40.886273_23.912687_fixed_23_180_PT5M.csv"
    target_date = '2024-05-19'
    
    try:
        # Calculate PV power (5:00 to 20:00)
        df_pvlib, df_osmmeps, df_weather = calculate_pv_power_may19(file_path, target_date)
        
        # Save results
        filename_pvlib, filename_osmmeps, filename_comparison = save_results(
            df_pvlib, df_osmmeps, target_date
        )
        
        # Plot results
        plot_results(df_pvlib, df_osmmeps, target_date)
        
        # Print summary
        print_summary(df_pvlib, df_osmmeps, target_date)
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE")
        print("="*80)
        print("Files generated:")
        print(f"  1. {filename_pvlib}")
        print(f"  2. {filename_osmmeps}")
        if filename_comparison:
            print(f"  3. {filename_comparison}")
        
    except FileNotFoundError:
        print(f"ERROR: Could not find file '{file_path}'")
        print("Please update the file_path variable with the correct path.")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
