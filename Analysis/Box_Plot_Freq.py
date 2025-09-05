import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns # Import seaborn for enhanced plotting

def analyze_and_plot_data_split_100pS_os_independent(excel_file_path):
    """
    Reads data from an Excel file, performs analysis, and generates a box plot
    for Conductance vs. Frequency, splitting the 100 pS data into two groups,
    with High Freq appearing before Low Freq, saving plots to the current directory.

    Args:
        excel_file_path (str): The path to the Excel file.

    Returns:
        None: The function displays and saves the plot.
    """
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(excel_file_path)
    except FileNotFoundError: # <--- MODIFIED: Relying on this for file existence check
        print(f"Error: File not found at {excel_file_path}")
        return
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Print the column names from the DataFrame to debug
    print("Column names in your Excel file:")
    print(df.columns)

    # Check for the required columns
    required_columns = ['Conductance', 'Seed', 'Power', 'Frequency']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: The Excel file is missing the following columns: {', '.join(missing_columns)}")
        return

    # --- Data Cleaning and Type Conversion ---

    # Convert 'Conductance' to numeric, handle errors
    df['Conductance'] = pd.to_numeric(df['Conductance'], errors='coerce')
    if df['Conductance'].isnull().any():
        print("Warning: Non-numeric values found in 'Conductance' column. These have been converted to NaN.")
    df = df.dropna(subset=['Conductance']) # Drop rows with NaN in 'Conductance'

    # Convert 'Power' to numeric (even if not plotted, needed for general cleaning)
    df['Power'] = pd.to_numeric(df['Power'], errors='coerce')
    df = df.dropna(subset=['Power']) # Drop rows with NaN in 'Power')

    # Multiply Conductance by 10^6 for pico-Siemens
    df['Conductance (pS)'] = df['Conductance'] * 1e6

    # --- MODIFICATION FOR SPLITTING 100 pS DATA ---
    # Define a new column for plotting to handle the split
    df['Conductance_Plot_Label'] = df['Conductance (pS)'].astype(str)

    # Apply the splitting logic for 100 pS
    split_threshold_freq = 100 
    
    # Assign labels: High Freq if >= threshold, Low Freq if < threshold
    df.loc[(df['Conductance (pS)'] == 100) & (df['Frequency'] >= split_threshold_freq), 'Conductance_Plot_Label'] = '100 pS (High Freq)'
    df.loc[(df['Conductance (pS)'] == 100) & (df['Frequency'] < split_threshold_freq), 'Conductance_Plot_Label'] = '100 pS (Low Freq)'
    
    # Ensure other conductance values are still represented by their original string
    df['Conductance_Plot_Label'] = df['Conductance_Plot_Label'].apply(lambda x: str(x).replace('.0', '') if x is not None else x)

    # Custom sort for a more intuitive order of split labels (e.g., 100 pS (High Freq) before 100 pS (Low Freq))
    def custom_sort_key_for_split(label):
        if 'pS' in label:
            val = float(label.split(' ')[0])
            if 'High Freq' in label:
                return (val, 0) # Sort high freq first
            elif 'Low Freq' in label:
                return (val, 1) # Sort low freq second
            return (val, 0.5) # Fallback for other 100 pS labels
        try:
            return (float(label), 0.5) # For other numeric labels (e.g., 50 pS)
        except ValueError:
            return (float('inf'), 0.5) # Fallback for unparseable labels
    
    sorted_labels = sorted(df['Conductance_Plot_Label'].unique(), key=custom_sort_key_for_split)
    # --- END MODIFICATION ---

    # Print data types after cleaning
    print("Data types after cleaning:")
    print(df.dtypes)
    # --- End Data Cleaning and Type Conversion ---

    # 1. Conductance vs. Frequency Box Plot (with split 100 pS)
    plt.figure(figsize=(15, 7)) # Larger figure to accommodate more x-axis labels
    if 'Conductance_Plot_Label' in df.columns and 'Frequency' in df.columns:
        try:
            sns.boxplot(data=df, x='Conductance_Plot_Label', y='Frequency', 
                        palette=None, # Removed color gradient
                        order=sorted_labels) # Use custom sorted order
            
            plt.title('Conductance vs. Frequency (100 pS Split)')
            plt.xlabel('Conductance (pS) / Group')
            plt.ylabel('Frequency (Hz)')
            plt.grid(False)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            # --- MODIFIED: Save plots to current directory ---
            plot_filename_base = "conductance_frequency_split_100pS"
            plt.savefig(f"{plot_filename_base}.png", dpi=300)
            plt.savefig(f"{plot_filename_base}.eps", format='eps')
            print(f"Plot saved to {plot_filename_base}.png and .eps in current directory.")
            # --- END MODIFIED ---

        except Exception as e:
            print(f"An unexpected error occurred during Frequency plot with split 100 pS: {e}")
    else:
        print("Error: 'Conductance_Plot_Label' or 'Frequency' column is missing or became empty after cleaning. Skipping plot.")

    # Show the plot
    plt.show()
    print("Analysis attempt completed. Check console for warnings/errors and plots.")


if __name__ == "__main__":
    excel_file_path = 'Power_Frequency_0519.xlsx'#I converted the .csv into .xlsx and used pandas+seaborn to plot the box-plots. 
    analyze_and_plot_data_split_100pS_os_independent(excel_file_path)
