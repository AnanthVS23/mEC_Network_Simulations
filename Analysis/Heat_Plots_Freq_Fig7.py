import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 1. File Paths and Setup ---

INPUT_FILE = 'GEGI_Batch_Freq_Data.xlsx'
OUTPUT_BASE_NAME = 'Avg_Freq_Heatmap'

OUTPUT_DIR = 'Heat_Plots/'

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Created output directory: {OUTPUT_DIR}")

# Define column names: 2 Conductance columns + 9 Frequency columns (Cols 3-11)
# range(1, 10) generates 1, 2, ..., 9
COLUMN_NAMES = ['EI_Cond', 'IE_Cond'] + [f'Freq_{i}' for i in range(1, 10)]

try:
    data = pd.read_excel(INPUT_FILE, header=None, names=COLUMN_NAMES)
    print(f"Successfully loaded {len(data)} data points.")
    
except FileNotFoundError:
    print(f"ERROR: File '{INPUT_FILE}' not found.")
    exit()

# --- 2. Data Transformation ---

# Calculate Average Frequency across all 9 frequency columns
freq_cols = [col for col in COLUMN_NAMES if col.startswith('Freq')]
data['Avg_Freq'] = data[freq_cols].mean(axis=1)

# Filter: Remove rows where IE_Cond < 33 nS
print(f"Filtering data: Removing rows where IE_Cond < 33 nS...")
data = data[data['IE_Cond'] >= 33.0]

print("\n--- Metric Value Ranges ---")
print(f"Average Frequency: Min={data['Avg_Freq'].min():.2f} Hz, Max={data['Avg_Freq'].max():.2f} Hz")
print("---------------------------")

# Reshape data
ei_cond_unique_sorted = np.sort(data['EI_Cond'].unique())
ie_cond_unique_sorted = np.sort(data['IE_Cond'].unique())

data['EI_Cond_C'] = pd.Categorical(data['EI_Cond'], categories=ei_cond_unique_sorted, ordered=True)
data['IE_Cond_C'] = pd.Categorical(data['IE_Cond'], categories=ie_cond_unique_sorted, ordered=True)

pivot_base = data.pivot_table(index='IE_Cond_C', columns='EI_Cond_C', values='Avg_Freq')
avg_freq_matrix = pivot_base.values

# Generate Axis Labels
ei_labels = [f'{int(x)}' for x in ei_cond_unique_sorted]
ie_labels = [f'{y:.1f}' for y in ie_cond_unique_sorted]

# --- 3. Plotting ---

sns.set_style("white")

styles = [
    ('RdYlBu_r', 'RdYlBu'),
    ('viridis', 'viridis'),
    ('plasma', 'plasma')
]

for cmap_style, suffix in styles:
    fig, ax = plt.subplots(1, 1, figsize=(9, 8), constrained_layout=True)

    sns.heatmap(
        avg_freq_matrix,
        ax=ax,
        cmap=cmap_style, 
        cbar_kws={'label': 'Average Frequency (Hz)', 'orientation': 'vertical', 'pad': 0.05, 'shrink': 0.9},
        xticklabels=ei_labels,
        yticklabels=ie_labels,
        linewidths=0.01,
        linecolor='gray',
        square=True,
        cbar=True
    )

    ax.invert_yaxis()

    ax.set_title(f'Average Oscillation Frequency Heatmap ({suffix})', fontsize=16)
    ax.set_xlabel('E-I Conductance (nS)', fontsize=14)
    ax.set_ylabel('I-E Conductance (nS)', fontsize=14)

    ax.set_xticks(np.arange(len(ei_labels)) + 0.5, labels=ei_labels, rotation=0, fontsize=11)
    ax.set_yticks(np.arange(len(ie_labels)) + 0.5, labels=ie_labels, rotation=0, fontsize=11)

    png_path = os.path.join(OUTPUT_DIR, f'{OUTPUT_BASE_NAME}_{suffix}.png')
    eps_path = os.path.join(OUTPUT_DIR, f'{OUTPUT_BASE_NAME}_{suffix}.eps')

    fig.savefig(png_path, dpi=300, bbox_inches='tight')
    fig.savefig(eps_path, bbox_inches='tight')

    plt.close(fig)

print("\nVisualization complete.")

