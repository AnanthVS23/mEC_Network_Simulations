import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns # Import seaborn for enhanced plotting

def analyze_and_plot_data(excel_file_path):
    """
    Reads data from an Excel file, performs analysis, and generates two box plots.

    Args:
        excel_file_path (str): The path to the Excel file.

    Returns:
        None: The function displays the plots.
    """
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(excel_file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {excel_file_path}")
        return
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Print the column names from the DataFrame to debug
    print("Column names in your Excel file:")
    print(df.columns)

    # Check for the required columns
    # Ensure 'Conductance' is in the list, based on previous debugging
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
        # Optionally, you might want to drop rows with NaN in 'Conductance' if they are critical
        df = df.dropna(subset=['Conductance'])

    # Convert 'Power' to numeric, handle errors, and address non-positive values
    df['Power'] = pd.to_numeric(df['Power'], errors='coerce')  # Convert to numeric first
    if df['Power'].isnull().any():
        print("Warning: Non-numeric values found in 'Power' column. These have been converted to NaN.")

    # Replace any non-positive (zero or negative) Power values with NaN, as log10 is undefined for them
    df['Power'] = df['Power'].apply(lambda x: x if x > 0 else np.nan)
    if df['Power'].isnull().any():
        print("Warning: Zero or negative 'Power' values found and converted to NaN for log transformation.")
    
    # Drop rows where 'Power' or 'Conductance' is NaN after conversion
    df = df.dropna(subset=['Power', 'Conductance'])

    # Multiply Conductance by 10^6 for pico-Siemens and update the column
    df['Conductance (pS)'] = df['Conductance'] * 1e6

    # Print data types after cleaning
    print("Data types after cleaning:")
    print(df.dtypes)
    # --- End Data Cleaning and Type Conversion ---

    # 1. Conductance vs. Frequency Box Plot
    plt.figure(figsize=(12, 7)) # Slightly larger figure for better appearance
    if 'Conductance (pS)' in df.columns and 'Frequency' in df.columns:
        try:
            # Use seaborn for better styling and color control
            sns.boxplot(data=df, x='Conductance (pS)', y='Frequency', palette='viridis') # 'viridis' is a color palette
            plt.title('Conductance vs. Frequency')
            plt.xlabel('Conductance (pS)') # Updated label for pico-Siemens
            plt.ylabel('Frequency')
            plt.grid(False) # Remove grid
            plt.xticks(rotation=45, ha='right') # Rotate x-axis labels if they overlap
            plt.tight_layout() # Adjust layout to prevent labels from being cut off
        except Exception as e:
            print(f"An unexpected error occurred during Frequency plot: {e}")
    else:
        print("Error: 'Conductance (pS)' or 'Frequency' column is missing or became empty after cleaning. Skipping Conductance vs. Frequency plot.")

    # 2. Conductance vs. Log(Power) Box Plot
    plt.figure(figsize=(12, 7)) # Slightly larger figure
    if 'Power' in df.columns and pd.api.types.is_numeric_dtype(df['Power']) and (df['Power'] > 0).all():
        df['LogPower'] = np.log10(df['Power'])
        if 'Conductance (pS)' in df.columns and 'LogPower' in df.columns:
            try:
                # Use seaborn for better styling and color control
                sns.boxplot(data=df, x='Conductance (pS)', y='LogPower', palette='magma') # Using a different palette
                plt.title('Conductance vs. Log10(Power)')
                plt.xlabel('Conductance (pS)') # Updated label for pico-Siemens
                plt.ylabel('Log10(Power)')
                plt.grid(False) # Remove grid
                plt.xticks(rotation=45, ha='right') # Rotate x-axis labels if they overlap
                plt.tight_layout() # Adjust layout
            except Exception as e:
                print(f"An unexpected error occurred during Log(Power) plot: {e}")
        else:
            print("Error: 'Conductance (pS)' or 'LogPower' column is missing or became empty after cleaning. Skipping Conductance vs Log(Power) plot.")
    else:
        print("Error: The 'Power' column is not numeric or contains non-positive values after cleaning. Skipping the Log(Power) plot.")

    # Show the plots
    plt.show()
    print("Analysis attempt completed. Check console for warnings/errors and plots.")


if __name__ == "__main__":
    # Replace 'your_file.xlsx' with the actual path to your Excel file
    excel_file_path = 'Power_Frequency_0519.xlsx'
    analyze_and_plot_data(excel_file_path)


