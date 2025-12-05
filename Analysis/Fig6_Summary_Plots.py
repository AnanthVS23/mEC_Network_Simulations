import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. File and Conversion Parameters ---

# Updated File Paths
FILE_PATH = 'Batch_Data.txt'#This can be changed based on the input file
FileID = "Summary_Figs/"

# --- 2. Conductance Array Definition ---

# Data ranges from 0 nS to 120 nS with a step of 6 nS (21 total steps)
conductance_nS = np.arange(0, 120.1, 6.0)

# Total number of unique conductance steps
num_steps = 21
# Total number of repetitions (seeds) per step
num_repetitions = 15

# Ensure the output directory exists
if not os.path.exists(FileID):
    os.makedirs(FileID)
    print(f"Created output directory: {FileID}")

# --- 3. Load and Reshape Data (21 Conductance Steps x 15 Seeds) ---

try:
    # Load the raw data
    data = np.loadtxt(FILE_PATH, comments='#', delimiter=',')
    
    # Data columns:
    # Column 0 (Index 0): Conductance (nS) -> Used for X-axis labels
    # Column 1 (Index 1): Seed Indices (1-15) -> Not used for plotting
    # Column 2 (Index 2): Average Power
    # Column 3 (Index 3): Wavelet Frequency
    # Column 4 (Index 4): ACF Frequency
    
    total_rows = data.shape[0]
    
    if total_rows != num_steps * num_repetitions:
        print(f"Error: Expected {num_steps * num_repetitions} rows (21*15), but found {total_rows}.")
        print("Cannot reshape correctly. Check data file integrity.")
        exit()

    print(f"Data check: Found {num_steps} conductance steps with {num_repetitions} seeds (repetitions) each.")
    
    # Since the data is already ordered (15 reps for 0 nS, then 15 for 6 nS, etc.),
    # we can directly reshape the relevant columns.
    
    # Reshape features from (Total Rows, 1) to (21, 15)
    # The box/violin plot function expects a list of 21 arrays, each of length 15.
    
    # Power Data (Column 2)
    power_reshaped = data[:, 2].reshape(num_steps, num_repetitions)
    power_plot_data = [power_reshaped[i] for i in range(num_steps)]

    # Wavelet Frequency Data (Column 3)
    wavelet_freq_reshaped = data[:, 3].reshape(num_steps, num_repetitions)
    wavelet_plot_data = [wavelet_freq_reshaped[i] for i in range(num_steps)]

    # Auto-correlation Frequency Data (Column 4)
    autocorr_freq_reshaped = data[:, 4].reshape(num_steps, num_repetitions)
    autocorr_plot_data = [autocorr_freq_reshaped[i] for i in range(num_steps)]

except FileNotFoundError:
    print(f"Error: Data file not found at '{FILE_PATH}'. Please check the path.")
    exit()
except Exception as e:
    print(f"An unexpected error occurred during data loading or reshaping: {e}")
    exit()

# The X-axis tick labels
x_labels = [f'{c:.0f}' for c in conductance_nS] # Use 0 decimal places for 0, 6, 12, ... 120

# --- Plotting Configuration ---

plot_config = {
    'fontsize': 14,
    'weight': 'bold',
    'xlabel': 'EI-Conductance (nS)', 
    'medianprops': dict(color='yellow', linewidth=2),
    'flierprops': dict(marker='o', markersize=3, markerfacecolor='black', alpha=0.5),
    'box_color': '#00796b', # Teal for Power
    'wavelet_color': '#d32f2f', # Red for Wavelet
    'autocorr_color': '#1976d2', # Blue for Autocorr
    'violin_alpha': 0.7,
    'violin_linecolor': 'black'
}

# ----------------------------------------------------------------------
# --- PLOT SET 1: BOX PLOTS ---
# ----------------------------------------------------------------------

# --- Plot 1A: Log(Power) vs. Conductance (Box Plot) ---
plt.figure(figsize=(12, 6))

# Apply log10 transformation to the power data (filter out zeros/negatives)
log_power_plot_data = [np.log10(arr[arr > 0]) for arr in power_plot_data]

plt.boxplot(log_power_plot_data, patch_artist=True, 
            boxprops=dict(facecolor=plot_config['box_color'], color='black'), 
            medianprops=plot_config['medianprops'],
            flierprops=plot_config['flierprops'])
            
plt.xticks(ticks=np.arange(1, num_steps + 1), labels=x_labels, rotation=45, ha='right')

plt.title(r'Log$_{10}$ (Power) vs. EI-Conductance (Box Plot)', fontsize=plot_config['fontsize'], weight=plot_config['weight'])
plt.xlabel(plot_config['xlabel'], fontsize=12)
plt.ylabel(r'Log$_{10}$ (Power)', fontsize=12)
plt.grid(False) # Removed Grid
plt.tight_layout()
plt.savefig(FileID+'Box_Log_Power.png', bbox_inches='tight')
plt.savefig(FileID+'Box_Log_Power.eps', bbox_inches='tight')
plt.close()


# --- Plot 1B: Wavelet Frequency vs. Conductance (Box Plot) ---
plt.figure(figsize=(12, 6))

plt.boxplot(wavelet_plot_data, patch_artist=True, 
            boxprops=dict(facecolor=plot_config['wavelet_color'], color='black'), 
            medianprops=plot_config['medianprops'],
            flierprops=plot_config['flierprops'])
            
plt.xticks(ticks=np.arange(1, num_steps + 1), labels=x_labels, rotation=45, ha='right')

plt.title('Wavelet Frequency vs. EI-Conductance (Box Plot)', fontsize=plot_config['fontsize'], weight=plot_config['weight'])
plt.xlabel(plot_config['xlabel'], fontsize=12)
plt.ylabel('Wavelet Frequency (Hz)', fontsize=12)
plt.grid(False) # Removed Grid
plt.tight_layout()
plt.savefig(FileID+'Box_Wavelet_Frequency.png', bbox_inches='tight')
plt.savefig(FileID+'Box_Wavelet_Frequency.eps', bbox_inches='tight')
plt.close()


# --- Plot 1C: Auto-correlation Frequency vs. Conductance (Box Plot) ---
plt.figure(figsize=(12, 6))

plt.boxplot(autocorr_plot_data, patch_artist=True, 
            boxprops=dict(facecolor=plot_config['autocorr_color'], color='black'), 
            medianprops=plot_config['medianprops'],
            flierprops=plot_config['flierprops'])
            
plt.xticks(ticks=np.arange(1, num_steps + 1), labels=x_labels, rotation=45, ha='right')

plt.title('Auto-correlation Frequency vs. EI-Conductance (Box Plot)', fontsize=plot_config['fontsize'], weight=plot_config['weight'])
plt.xlabel(plot_config['xlabel'], fontsize=12)
plt.ylabel('Auto-correlation Frequency (Hz)', fontsize=12)
plt.grid(False) # Removed Grid
plt.tight_layout()
plt.savefig(FileID+'Box_Autocorr_Frequency.png', bbox_inches='tight')
plt.savefig(FileID+'Box_Autocorr_Frequency.eps', bbox_inches='tight')
plt.close()


# ----------------------------------------------------------------------
# --- PLOT SET 2: VIOLIN PLOTS ---
# ----------------------------------------------------------------------

# --- Plot 2A: Log(Power) vs. Conductance (Violin Plot) ---
plt.figure(figsize=(12, 6))

# Use the same log-transformed data
plt.violinplot(log_power_plot_data, showmeans=False, showmedians=True, showextrema=True)

# Customize violins (needs to be done on the collection returned by violinplot)
parts = plt.violinplot(log_power_plot_data, showmeans=False, showmedians=True, showextrema=False)
for pc in parts['bodies']:
    pc.set_facecolor(plot_config['box_color'])
    pc.set_edgecolor(plot_config['violin_linecolor'])
    pc.set_alpha(plot_config['violin_alpha'])
parts['cmedians'].set_edgecolor(plot_config['medianprops']['color'])

# For violin plots, ticks are centered at 1, 2, 3...
plt.xticks(ticks=np.arange(1, num_steps + 1), labels=x_labels, rotation=45, ha='right')

plt.title(r'Log$_{10}$ (Power) vs. EI-Conductance (Violin Plot)', fontsize=plot_config['fontsize'], weight=plot_config['weight'])
plt.xlabel(plot_config['xlabel'], fontsize=12)
plt.ylabel(r'Log$_{10}$ (Power)', fontsize=12)
plt.grid(False) # Removed Grid
plt.tight_layout()
plt.savefig(FileID+'Violin_Log_Power.png', bbox_inches='tight')
plt.savefig(FileID+'Violin_Log_Power.eps', bbox_inches='tight')
plt.close()


# --- Plot 2B: Wavelet Frequency vs. Conductance (Violin Plot) ---
plt.figure(figsize=(12, 6))

parts = plt.violinplot(wavelet_plot_data, showmeans=False, showmedians=True, showextrema=False)
for pc in parts['bodies']:
    pc.set_facecolor(plot_config['wavelet_color'])
    pc.set_edgecolor(plot_config['violin_linecolor'])
    pc.set_alpha(plot_config['violin_alpha'])
parts['cmedians'].set_edgecolor(plot_config['medianprops']['color'])

plt.xticks(ticks=np.arange(1, num_steps + 1), labels=x_labels, rotation=45, ha='right')

plt.title('Wavelet Frequency vs. EI-Conductance (Violin Plot)', fontsize=plot_config['fontsize'], weight=plot_config['weight'])
plt.xlabel(plot_config['xlabel'], fontsize=12)
plt.ylabel('Wavelet Frequency (Hz)', fontsize=12)
plt.grid(False) # Removed Grid
plt.tight_layout()
plt.savefig(FileID+'Violin_Wavelet_Frequency.png', bbox_inches='tight')
plt.savefig(FileID+'Violin_Wavelet_Frequency.eps', bbox_inches='tight')
plt.close()


# --- Plot 2C: Auto-correlation Frequency vs. Conductance (Violin Plot) ---
plt.figure(figsize=(12, 6))

parts = plt.violinplot(autocorr_plot_data, showmeans=False, showmedians=True, showextrema=False)
for pc in parts['bodies']:
    pc.set_facecolor(plot_config['autocorr_color'])
    pc.set_edgecolor(plot_config['violin_linecolor'])
    pc.set_alpha(plot_config['violin_alpha'])
parts['cmedians'].set_edgecolor(plot_config['medianprops']['color'])

plt.xticks(ticks=np.arange(1, num_steps + 1), labels=x_labels, rotation=45, ha='right')

plt.title('Auto-correlation Frequency vs. EI-Conductance (Violin Plot)', fontsize=plot_config['fontsize'], weight=plot_config['weight'])
plt.xlabel(plot_config['xlabel'], fontsize=12)
plt.ylabel('Auto-correlation Frequency (Hz)', fontsize=12)
plt.grid(False) # Removed Grid
plt.tight_layout()
plt.savefig(FileID+'Violin_Autocorr_Frequency.png', bbox_inches='tight')
plt.savefig(FileID+'Violin_Autocorr_Frequency.eps', bbox_inches='tight')
plt.close()

print("\nAnalysis complete. Six figures (3 Box Plots and 3 Violin Plots) have been generated and saved:")
print(f"Directory: {FileID}")
print(f"Feature: Log(Power). Files: Box_Log_Power.png/eps, Violin_Log_Power.png/eps")
print(f"Feature: Wavelet Freq. Files: Box_Wavelet_Frequency.png/eps, Violin_Wavelet_Frequency.png/eps")
print(f"Feature: ACF Freq. Files: Box_Autocorr_Frequency.png/eps, Violin_Autocorr_Frequency.png/eps")
