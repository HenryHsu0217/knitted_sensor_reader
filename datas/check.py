"""
Print out the data for checking
"""
import numpy as np
import matplotlib.pyplot as plt
def print_npz_contents(file_path):
    loaded_data = np.load(file_path)
    print("Keys in the .npz file:", loaded_data.files)
    datas=[]
    for key in loaded_data.files:
        print(f"Array '{key}':")
        array_data = loaded_data[key]
        datas.append(array_data)
        print("Shape:", array_data.shape)
        print("Data:")
        print(array_data)
        print()  
file_path = "test.npz" # Enter the file you want to check 
print_npz_contents(file_path)