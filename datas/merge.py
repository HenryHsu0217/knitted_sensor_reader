"""
Merging the datas for each angle into one
"""
import numpy as np
import os
def merge_npz_files(file_paths):
    all_data_values = []
    all_true_values = []

    for file_path in file_paths:
        loaded_data = np.load(file_path)
        data_values = loaded_data['data_values']
        true_values = loaded_data['true_values']
        all_data_values.append(data_values)
        all_true_values.append(true_values)
    merged_data_values = np.concatenate(all_data_values)
    merged_true_values = np.concatenate(all_true_values)
    return merged_data_values, merged_true_values
def get_all_filenames(folder_path):
    filenames = []
    for filename in os.listdir(folder_path):
        # Check if it is a file
        if os.path.isfile(os.path.join(folder_path, filename)):
            filenames.append(f"{folder_path}/{filename}")

    return filenames
file_paths = get_all_filenames('Example_ data_ wth_10x30_sensor') # Replace the directory of the data
print(file_paths)
merged_data_values, merged_true_values = merge_npz_files(file_paths)
np.savez("Merged/3x10.npz", data_values=merged_data_values, true_values=merged_true_values)