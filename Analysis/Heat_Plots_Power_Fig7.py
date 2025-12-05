import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 1. File Paths and Setup ---

# Define input file (Adjust extension to .csv if needed, assuming .xlsx based on recent tasks)
INPUT_FILE = 'GEGI_Batch_Power_Data.xlsx' 
OUTPUT_BASE_NAME = 'Log_Power_Heatmap'
OUTPUT_DIR = 'Heat_Plots/'

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Created output directory: {OUTPUT_DIR}")

# Define column names based on your description
# Col 1: EI_Cond, Col 2: IE_Cond, Cols 3+: Power values
# We will detect power columns dynamically
try:
    # Read without header to treat all rows as data
    data = pd.read_excel(INPUT_FILE, header=None)
    
    # Rename first two columns
    data.rename(columns={0: 'EI_Cond', 1: 'IE_Cond'}, inplace=True)
    
    # Identify Power Columns (all columns from index 2 onwards)
    power_cols = data.columns[2:]
    
    print(f"Successfully loaded {len(data)} data points.")
    print(f"Detected {len(power_cols)} power columns to average.")

except FileNotFoundError:
    print(f"ERROR: File '{INPUT_FILE}' not found.")
    exit()

# --- 2. Data Transformation ---

# 1. Filter: Remove rows where IE_Cond < 33 nS
print(f"Filtering data: Removing rows where IE_Cond < 33 nS...")
data = data[data['IE_Cond'] >= 33.0]

# 2. Calculate Average Power first (arithmetic mean of power columns)
#    Then take Log10 of that average.
#    Alternatively, take Log10 of each then average? usually Average Power -> Log is standard.
#    Let's do Mean(Power) -> Log10(Mean)
avg_power = data[power_cols].mean(axis=1)

# Handle potential zeros before log
EPSILON = 1e-9
data['Log10_Power'] = np.log10(np.where(avg_power > 0, avg_power, EPSILON))

print("\n--- Metric Value Ranges ---")
print(f"Log10 Power: Min={data['Log10_Power'].min():.2f}, Max={data['Log10_Power'].max():.2f}")
print("---------------------------")

# 3. Reshape data
ei_cond_unique_sorted = np.sort(data['EI_Cond'].unique())
ie_cond_unique_sorted = np.sort(data['IE_Cond'].unique())

data['EI_Cond_C'] = pd.Categorical(data['EI_Cond'], categories=ei_cond_unique_sorted, ordered=True)
data['IE_Cond_C'] = pd.Categorical(data['IE_Cond'], categories=ie_cond_unique_sorted, ordered=True)

pivot_base = data.pivot_table(index='IE_Cond_C', columns='EI_Cond_C', values='Log10_Power')
log_power_matrix = pivot_base.values

# 4. Generate Axis Labels
# E-I (X-axis): Clean integers
ei_labels = [f'{int(x)}' for x in ei_cond_unique_sorted]
# I-E (Y-axis): Floats with 1 decimal
ie_labels = [f'{y:.1f}' for y in ie_cond_unique_sorted]

# --- 3. Plotting ---

sns.set_style("white")

# Styles for the 3 requested maps
styles = [
    ('RdYlBu_r', 'RdYlBu'),
    ('viridis', 'viridis'),
    ('plasma', 'plasma')
]

for cmap_style, suffix in styles:
    fig, ax = plt.subplots(1, 1, figsize=(9, 8), constrained_layout=True)

    sns.heatmap(
        log_power_matrix,
        ax=ax,
        cmap=cmap_style, 
        cbar_kws={'label': '$\log_{10}(\\text{Power})$ (a.u.)', 'orientation': 'vertical', 'pad': 0.05, 'shrink': 0.9},
        xticklabels=ei_labels,
        yticklabels=ie_labels,
        linewidths=0.01,
        linecolor='gray',
        square=True,
        cbar=True
    )

    # Invert Y-axis so low I-E is at bottom
    ax.invert_yaxis()

    ax.set_title(f'Average Log Power Heatmap ({suffix})', fontsize=16)
    ax.set_xlabel('E-I Conductance (nS)', fontsize=14)
    ax.set_ylabel('I-E Conductance (nS)', fontsize=14)

    ax.set_xticks(np.arange(len(ei_labels)) + 0.5, labels=ei_labels, rotation=0, fontsize=11)
    ax.set_yticks(np.arange(len(ie_labels)) + 0.5, labels=ie_labels, rotation=0, fontsize=11)

    # Save to the Output directory
    png_path = os.path.join(OUTPUT_DIR, f'{OUTPUT_BASE_NAME}_{suffix}.png')
    eps_path = os.path.join(OUTPUT_DIR, f'{OUTPUT_BASE_NAME}_{suffix}.eps')

    fig.savefig(png_path, dpi=300, bbox_inches='tight')
    fig.savefig(eps_path, bbox_inches='tight')

    plt.close(fig)
    print(f"Saved {suffix} plot to {png_path}")

print("\nVisualization complete.")

