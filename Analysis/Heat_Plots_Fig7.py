"""
@author: Ananth

Extracts and analyzes data for single simulation

This code extracts .pkl file

This code calculates the spike time histograms and wavelet scalograms corresponding to that.

Using the Histograms, the auto-correlation is also calculated
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 1. File Paths and Setup ---

# Define the directory and file paths
OUTPUT_DIR = '1120_Swami/'
INPUT_FILE = os.path.join('1120_Alt_Batch/', '1120_Data_0.csv')
OUTPUT_BASE_NAME = 'conductance_heatmap' # Base name for individual figures

# FIX: The sample data shows the values are ALREADY in nS/umho.
# Therefore, the scaling factor to get clean integers is 1.0.
SCALING_FACTOR_X = 1.0 
SCALING_FACTOR_Y = 1.0 

# Ensure the output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Created output directory: {OUTPUT_DIR}")


# Define column names based on your description.
COLUMN_NAMES = [
    'EI_Cond',       # Column 1: E-I conductance (nS)
    'IE_Cond',       # Column 2: I-E conductance (nS)
    'Power',         # Column 3: Power
    'Wavelet_Freq',  # Column 4: Wavelet frequency
    'ACF_Freq'       # Column 5: ACF Frequency
]

try:
    # Load your actual data.
    data = pd.read_csv(INPUT_FILE, header=None, names=COLUMN_NAMES)
    print(f"Successfully loaded {len(data)} data points from '{INPUT_FILE}'.")
    
except FileNotFoundError:
    print(f"ERROR: File '{INPUT_FILE}' not found. Please ensure the CSV file is in the correct directory.")
    exit()

# --- 2. Data Transformation and Reshaping (MODIFIED) ---

# 1. Calculate log10(Power)
EPSILON = 1e-9
data['Log10_Power'] = np.log10(np.where(data['Power'] > 0, data['Power'], EPSILON))

# NEW ADDITION: Print min/max values for scaling reference
print("\n--- Metric Value Ranges for Color Scaling ---")
print(f"Log10 Power Range: Min={data['Log10_Power'].min():.2f}, Max={data['Log10_Power'].max():.2f}")
print(f"Wavelet Frequency Range: Min={data['Wavelet_Freq'].min():.2f} Hz, Max={data['Wavelet_Freq'].max():.2f} Hz")
print(f"ACF Frequency Range: Min={data['ACF_Freq'].min():.2f} Hz, Max={data['ACF_Freq'].max():.2f} Hz")
print("---------------------------------------------")

# --- FILTERING STEP REMOVED ---
# The previous code filtered out rows where EI_Cond = 0.0 or IE_Cond = 0.0.
# Since the new data is pre-filtered, we use the original 'data' DataFrame directly.
data_plot = data.copy()
# ------------------------------

# 2. Get unique, *sorted* conductance values for precise matrix creation
# !!! USING 'data_plot' (which is now the full, unfiltered dataset) !!!
ei_cond_unique_sorted = np.sort(data_plot['EI_Cond'].unique())
ie_cond_unique_sorted_filtered = np.sort(data_plot['IE_Cond'].unique())

# Report the new matrix dimensions
EI_DIM = len(ei_cond_unique_sorted)
IE_DIM = len(ie_cond_unique_sorted_filtered)
print(f"\n--- Matrix Dimensions ---")
print(f"E-I Conductance (Columns): {EI_DIM}")
print(f"I-E Conductance (Rows): {IE_DIM}")
print(f"Total points expected: {EI_DIM} x {IE_DIM} = {EI_DIM * IE_DIM}")
print(f"Total data points loaded: {len(data_plot)}")
print("-------------------------")


# 3. Reshape the data using Categorical types to ensure the pivot table
#    maintains the custom sorted order.
data_plot['EI_Cond_C'] = pd.Categorical(data_plot['EI_Cond'], categories=ei_cond_unique_sorted, ordered=True)
data_plot['IE_Cond_C'] = pd.Categorical(data_plot['IE_Cond'], categories=ie_cond_unique_sorted_filtered, ordered=True)

# 4. Pivot the filtered data to create the 2D matrices
# !!! USING 'data_plot' (which is now the full, unfiltered dataset) !!!
pivot_base = data_plot.pivot_table(index='IE_Cond_C', columns='EI_Cond_C', values=['Log10_Power', 'Wavelet_Freq', 'ACF_Freq'])

power_matrix = pivot_base['Log10_Power'].values
wavelet_freq_matrix = pivot_base['Wavelet_Freq'].values
acf_freq_matrix = pivot_base['ACF_Freq'].values

# --- Axis Labels (Scaled Integers) ---
# E-I labels must be based on the unique, sorted list
ei_labels_int = [f'{int(x * SCALING_FACTOR_X)}' for x in ei_cond_unique_sorted]
# I-E labels must be based on the unique, sorted list
ie_labels_int = [f'{int(y * SCALING_FACTOR_Y)}' for y in ie_cond_unique_sorted_filtered]

# --- 3. Plotting (Separate, Large Heatmaps) ---

# Set a clean plotting style
sns.set_style("white")

# List of all matrices and their properties
plot_data = [
    (power_matrix, 'RdYlBu_r', 'LogPower', '$\log_{10}(\\text{Power})$ (a.u.)'),
    (wavelet_freq_matrix, 'RdYlBu_r', 'WaveletFreq_1', 'Wavelet Frequency (Hz)'),
    (wavelet_freq_matrix, 'viridis', 'WaveletFreq_2', 'Wavelet Frequency (Hz)'),
    (wavelet_freq_matrix, 'plasma', 'WaveletFreq_3', 'Wavelet Frequency (Hz)'),
    (acf_freq_matrix, 'viridis', 'AutoCorrFreq1', 'Auto Corr Frequency (Hz)'),
    (acf_freq_matrix, 'plasma', 'AutoCorrFreq2', 'AutoCorr (Hz)') ,
    (acf_freq_matrix, 'RdYlBu_r', 'AutoCorrFreq3', 'Auto Corr Frequency (Hz)')
]

# Use a step to show every label (step=1) since the labels are now clean integers.
step = 1

for matrix, cmap_style, file_suffix, cbar_label in plot_data:
    
    # Create NEW figure with size adjusted for potentially larger matrix
    fig, ax = plt.subplots(1, 1, figsize=(EI_DIM * 0.5, IE_DIM * 0.5), constrained_layout=True)
    
    # Plot Heatmap
    sns.heatmap(
        matrix,
        ax=ax,
        cmap=cmap_style,
        cbar_kws={'label': cbar_label, 'orientation': 'vertical', 'pad': 0.05, 'shrink': 0.9},
        # Use the clean integer labels
        xticklabels=ei_labels_int,
        yticklabels=ie_labels_int,
        linewidths=0.01, # Reduced line width for cleaner look
        linecolor='gray',
        square=False, # Set to False for non-square matrices (16x20 is not square)
        cbar=True
    )
    
    # FIX: Invert Y-axis so I-E Conductance increases from bottom to top (standard cartesian)
    ax.invert_yaxis()
    
    # Set Labels and Ticks
    ax.set_title(f'{cbar_label} Heatmap ({EI_DIM}x{IE_DIM})', fontsize=16) # Title updated with dynamic dimensions
    ax.set_xlabel(f'E-I Conductance (nS)', fontsize=14)
    ax.set_ylabel(f'I-E Conductance (nS)', fontsize=14)
    
    # Apply custom tick locations using the integer-based lists
    ax.set_xticks(np.arange(len(ei_labels_int)) + 0.5, labels=ei_labels_int, rotation=90, fontsize=10) # Rotated X-ticks for potentially many labels
    ax.set_yticks(np.arange(len(ie_labels_int)) + 0.5, labels=ie_labels_int, rotation=0, fontsize=10)
    
    # 4. Save the separate figure files
    png_path = os.path.join(OUTPUT_DIR, f'{OUTPUT_BASE_NAME}_{file_suffix}.png')
    eps_path = os.path.join(OUTPUT_DIR, f'{OUTPUT_BASE_NAME}_{file_suffix}.eps')
    
    fig.savefig(png_path, dpi=300, bbox_inches='tight')
    fig.savefig(eps_path, bbox_inches='tight')
    
    print(f"Saved separate figures for {file_suffix} to:\n  - {png_path}\n  - {eps_path}")
    
    # Close the figure
    plt.close(fig)

print("\nAll visualizations complete. Heatmaps based on all data points saved.")
