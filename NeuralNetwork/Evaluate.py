"""
Evaluates the trained model with selected data set
"""
import torch
from NeuralNetwork.Network_for_one import NeuralNetwork
from NeuralNetwork.Train_for_one import CustomDataset
import numpy as np
import random
if __name__ == '__main__':
    model=NeuralNetwork()
    dataset=CustomDataset('../datas/Merged/3x10.npz') # Replace with your data
    model.load_state_dict(torch.load('Trained_models/model_1.pth')) # Replace with your model
    model.eval()
    evaluate_time=1000
    correct=0
    incorrect_5=0
    incorrect_10=0
    incorrect_20=0
    incorrect_30=0
    errors=[]
    for i in range(evaluate_time):
        test_id=random.randint(0,len(dataset.data))
        feature,lable=dataset.data[test_id]
        predict=model(torch.tensor(feature,dtype=torch.float32)).detach().numpy()[0]
        error=abs(predict-lable)
        if error>5 and error<=10:
            incorrect_5+=1
        elif error>10 and error<=20:
            incorrect_10+=1
        elif error>20 and error<=30:
            incorrect_20+=1
        elif error>30 and error<=40:
            incorrect_30+=1
        else:
            correct+=1
        errors.append(error)
    average_error=sum(errors)/evaluate_time
    print(f"Correct prediction in range of error under 5 degree: {correct}")
    print(f"Prediction in range of error over 5 degree: {incorrect_5}")
    print(f"Prediction in range of error over 10 degree: {incorrect_10}")
    print(f"Prediction in range of error over 20 degree: {incorrect_20}")
    print(f"Prediction in range of error over 30 degree: {incorrect_30}")
    print(f"Accuracy: {correct/evaluate_time}")
    print(f"Average error: {average_error}")