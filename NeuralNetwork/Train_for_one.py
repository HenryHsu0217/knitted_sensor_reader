"""
Training models for predicting the angle 
"""
import numpy as np
from Network_for_one import NeuralNetwork
import torch
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim

 # Creat a dataset for passing the datas
class CustomDataset(Dataset):
    def __init__(self, npz_file):
        loaded_data = np.load(npz_file)
        self.data = []
        for key in loaded_data:
            numeric_data = np.array(loaded_data[key], dtype=np.float32)
            if numeric_data.ndim == 1: 
                numeric_data = numeric_data.reshape(-1, 1)  
            self.data.append(numeric_data)
        self.data = np.array([[self.normalize(data_values,4095,0), true_values] for data_values, true_values in zip(self.data[0],self.data[1])]) # Normalize the data 
    def __len__(self):
        return len(self.data)
    def __getitem__(self, idx):
        sample = self.data[idx]
        if sample.ndim == 0: 
            raise ValueError(f"Sample at index {idx} is a scalar. Data might be corrupted or improperly formatted.")
        features = torch.tensor(sample[:-1], dtype=torch.float32)  # Getting the features(sensor reading)
        label = torch.tensor(sample[-1], dtype=torch.float32)  # Getting the labels(correct angle)
        return features, label
     # Normalization funciton
    def normalize(self, x, max_val, min_val):
        return (x - min_val) / (max_val - min_val)

 # main training loop
if __name__ == '__main__':
    dataset = CustomDataset('../datas/Merged/3x10.npz') # Replace it with your merged data
    data_loader = DataLoader(dataset, batch_size=32, shuffle=True) 
    model = NeuralNetwork()
    criterion = torch.nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=25, gamma=0.1)
    num_epochs = 200
     # Training loop
    for epoch in range(num_epochs):
        model.train() 
        for i, (inputs, labels) in enumerate(data_loader):
            outputs = model(inputs)
            loss = criterion(outputs, labels.unsqueeze(1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        scheduler.step() 
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.20f}')
    torch.save(model.state_dict(), f'./Trained_models/model_1.pth') # Save the model
