import numpy as np
import matplotlib.pyplot as plt
import glob, os
from netpyne.analysis.tools import loadData

# --- GLOBAL CONFIGURATION ---
# Removed np.random.seed(42) as random selection is no longer used for SCs

# Raster plot specific parameters
theta_cycle_duration_ms_single = 125 # Duration of a single theta cycle
raster_plot_window_duration_ms = 250 # Total duration for raster plot (2 * 125ms = 2 cycles)
marker_size_val = 5 # Marker size set to 5 for all plots

# Base directory for saving plots
base_output_dir = 'Raster_Plots/' # Changed output directory to distinguish these plots

# Neuron ID ranges (used for defining contiguous sets)
PV_CELL_IDS_MIN = 1
SC_CELL_IDS_MIN = 101

# Define fixed sets for the combined plot (selected once globally)
fixed_pv_ids_for_combined_plot = np.arange(PV_CELL_IDS_MIN, PV_CELL_IDS_MIN + 30) # IDs 1-30

# Changed back to contiguous SC cells for easier labeling
fixed_sc_ids_for_combined_plot = np.arange(SC_CELL_IDS_MIN, SC_CELL_IDS_MIN + 60) # IDs 101-160


# Ensure the base output directory exists
if not os.path.exists(base_output_dir):
    os.makedirs(base_output_dir)
    print(f"Created output directory: {base_output_dir}")
else:
    print(f"Output directory already exists: {base_output_dir}")

# --- Main loop to process files ---
file_pattern = "../output/Varying_Seeds/*_data.pkl" #Make the filename explicit to make sure you plot rasters for each simulation at once. Otherwise modify to get different filenames
simulation_files = glob.glob(file_pattern)

if not simulation_files:
    print(f"No simulation files found matching pattern: {file_pattern}")
    print("Please check the path and filename pattern.")
else:
    print(f"Found {len(simulation_files)} simulation files. Generating combined raster plots only.")

for file_path in simulation_files:
    print(f"\nProcessing file: {file_path}")
    
    # Extract the base filename without extension to use as a generic identifier
    base_name_with_ext = os.path.basename(file_path)
    file_id_suffix, _ = os.path.splitext(base_name_with_ext)

    print(f"  Extracted identifier: {file_id_suffix}")

    if not os.path.exists(file_path):
        print(f"  Error: File not found at '{file_path}'. Skipping this file.")
        continue

    fileInfo = loadData(file_path)
    
    sim_duration = fileInfo['simConfig']['duration'] # Simulation duration in ms

    # Get all spike times and cell IDs from the simulation
    spkt_all = np.array(fileInfo['simData']['spkt'])
    spkid_all = np.array(fileInfo['simData']['spkid'])

    # --- Identify and extract data for the LAST TWO theta cycles ---
    total_num_cycles_in_sim = int(np.floor(sim_duration / theta_cycle_duration_ms_single))

    if total_num_cycles_in_sim < 2:
        print(f"  Skipping {file_path}: Simulation duration too short for two complete theta cycles ({sim_duration:.0f}ms).")
        continue

    # Calculate start and end times for the last 2 cycles
    start_time_window_ms = (total_num_cycles_in_sim - 2) * theta_cycle_duration_ms_single
    end_time_window_ms = start_time_window_ms + raster_plot_window_duration_ms

    print(f"  Plotting for the last two theta cycles (Time: {start_time_window_ms:.0f}ms - {end_time_window_ms:.0f}ms)")

    # Filter all spikes for events within this specific 2-cycle window
    spikes_in_window_mask = (spkt_all >= start_time_window_ms) & (spkt_all < end_time_window_ms)
    spkts_in_window = spkt_all[spikes_in_window_mask]
    spkids_in_window = spkid_all[spikes_in_window_mask]

    # Convert spike times to be relative to the start of the 2-cycle window
    relative_spikes_ms = spkts_in_window - start_time_window_ms

    # --- Generate the Combined Fixed PV and SC Cells Plot ---
    print(f"  Generating Combined Fixed Raster Plot for {file_id_suffix} (PVs: 1-30, SCs: 101-160)...")
    combined_fig = plt.figure(figsize=(10, 6))
    ax = plt.gca()

    # Create a single sorted list of all target cell IDs for the Y-axis mapping
    all_combined_target_ids = np.sort(np.concatenate((fixed_pv_ids_for_combined_plot, fixed_sc_ids_for_combined_plot)))
    combined_cell_id_to_serial_map = {cell_id: i + 1 for i, cell_id in enumerate(all_combined_target_ids)}

    # Filter spikes for the fixed PV cells
    fixed_pv_spikes_mask = np.isin(spkids_in_window, fixed_pv_ids_for_combined_plot)
    pv_plot_y_positions = np.array([combined_cell_id_to_serial_map[cid] for cid in spkids_in_window[fixed_pv_spikes_mask]])
    ax.plot(relative_spikes_ms[fixed_pv_spikes_mask], 
            pv_plot_y_positions, '|', 
            color='blue', markersize=marker_size_val, markeredgewidth=1.5, label=f'PV+ Cells (IDs {fixed_pv_ids_for_combined_plot.min()}-{fixed_pv_ids_for_combined_plot.max()})')

    # Filter spikes for the fixed SC cells
    fixed_sc_spikes_mask = np.isin(spkids_in_window, fixed_sc_ids_for_combined_plot)
    sc_plot_y_positions = np.array([combined_cell_id_to_serial_map[cid] for cid in spkids_in_window[fixed_sc_spikes_mask]])
    ax.plot(relative_spikes_ms[fixed_sc_spikes_mask], 
            sc_plot_y_positions, '|', 
            color='red', markersize=marker_size_val, markeredgewidth=1.5, label=f'SC Cells (IDs {fixed_sc_ids_for_combined_plot.min()}-{fixed_sc_ids_for_combined_plot.max()})')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xlabel('Time (ms)')
    plt.xlim([0, raster_plot_window_duration_ms])
    plt.ylabel('Neuron ID') # Label reflects actual ID, though position is serial

    # Set y-axis limits to cover the entire serial range of combined cells with padding
    plt.ylim([0.5, len(all_combined_target_ids) + 0.5])
    
    # Set y-ticks and labels to show the actual Neuron IDs at their serial positions
    # Choose an appropriate interval for ticks based on the total number of combined neurons (90 here)
    y_tick_positions_serial = np.arange(1, len(all_combined_target_ids) + 1, 10) # Adjust interval (e.g., 5, 10, 15) as needed
    y_tick_labels_actual_id = [str(all_combined_target_ids[pos - 1]) for pos in y_tick_positions_serial]
    plt.yticks(y_tick_positions_serial, y_tick_labels_actual_id)


    plt.title(f'Raster Fixed PV+ & SC Cells for {file_id_suffix}\n(Last Two Theta Cycles)')
    plt.legend(loc='upper right', frameon=False)
    plt.tight_layout()
    
    # Save the combined plot
    plt.savefig(os.path.join(base_output_dir, f'Combined_Fixed_Raster_{file_id_suffix}.png'), dpi=300)
    plt.savefig(os.path.join(base_output_dir, f'Combined_Fixed_Raster_{file_id_suffix}.eps'), dpi=300)
    plt.close(combined_fig)
    print(f"  Saved combined raster plot for: Combined_Fixed_Raster_{file_id_suffix}.png")
    
print("\nAll combined raster plot generation complete across all specified files.")
