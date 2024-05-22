# Knitted Sensor Reader

## Introduction
This project contains the code and hardware setup for collecting data from knitted sensors. It includes simple examples of collected data with a 3x10 size sensor and a trained neural network for predicting the angle of the tested sensor. Additionally, code is provided for live evaluation for one or four sensors at a time with the trained neural network model.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Setup](#setup)
    - [Hard ware setup](#hard-ware-setup)
        - [Robot arm setup and control](#robot-arm-setup-and-control)
        - [Xiao Seeed setup](#xiao-seeed-setup)
    - [WiFi setup](#wifi-setup)
- [Usage](#usage)
  - [Data Collection](#data-collection)
    - [Data Collection for one sensor](#data-collection-for-one-sensor)
    - [Data Collection for four sensor](#data-collection-for-four-sensor)
  - [Model Training](#model-training)
  - [Live Evaluation](#live-evaluation)
- [Examples](#examples)
## Features
- Collect data from knitted sensors
- Simple examples with 3x10 size sensor data
- Trained neural network model for angle prediction
- Live evaluation for one or four sensors simultaneously
## Installation
1. Clone the repository to your local machine:
   ```sh
   git clone https://github.com/HenryHsu0217/knitted_sensor_reader.git
    ```
2. Navigate to the project directory
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
## Setup
### Hard ware setup
To set up the hardware for this project, you will need:  
- Knitted sensors
- Xiao Seeed ESP32C with custom PCB
- Connection wires
- Batteries
- Arduino Tinkerkit robot arm with sleeve and Ardino Uno
#### Robot arm setup and control
To setup and control the robot arm, please first go to https://docs.arduino.cc/retired/getting-started-guides/Braccio/ to check the essential library for the robot, after downloading the library, upload `Robot_arm.cpp` to the braod controling the arm. After uploading, you can control the robot arm to certain angle with serial input. Before entering the angle, please keep in mind that we are only controlling the ELBOW of the robot, and due to the setting of the arm, the arm will be at 0 degree with a setting of 45, so when entering the desired angle remember to add 45 to it. For example if you want the ELBOW to got to 60 degree, please enter 105 instead.
  
Attach the knitted sensor to the robot arm as shown to finish the robot arm setup.
### WiFi setup
The device that you are running the code with will be the server for the system, and make sure you are connected to private network, pubic network may cuase problem in connection.  

After your device is connected to a private netwrok and get your device's IP address update the SSID, password, and host ID accroding to your device in the `WiFi_Client.cpp` file for the Xiao Seeed broad. And also remember to update the host IP in `server_for_one.py`, `server_for_four.py`, `Live_Evalution_for_one.py`, and `live_Evalution_for_four.py` before running them with your device's IP.
#### Xiao Seeed setup
Upload `WiFi_Client.cpp` to the broad with the WiFi set correctly, insert the wires from the knitted sensor into the terminal and screw it tight. Plug in the battery and after the server is running press reset button on the broad to connect to the server.
## Usage
### Data collection 
#### Data collection for one sensor
Before running the file `server_for_one.py` once again make sure the WiFi has been setup properly so that the port and host IP in `server_for_one.py` are the same in `WiFi_Client.cpp`. After uploading `WiFi_Client.cpp` to the braod and `server_for_one.py`.  

Run the server with:
```sh
python server_for_one.py
```  
After running the command line would show:
```sh
Server listening on 172.20.10.3:8080
starting user thread
Please input the file location for the data: 
```  
Enter the file location that you want to save the data(Ex: `datas/test_file`). After entering the file location the command line will ask to enter the current angle:
```sh
Please input angle: 
```
 After entering the angle, connect power to the Xiao Seed broad, if nothing happens press the reset button on the broad to make it retry on connecting to the WiFi. After it is connected to WiFi and connected to the server, the command line would show:
```sh
Server listening on 172.20.10.3:8080
starting user thread
Please input the file location for the data: test_file
Accepted connection from ('172.20.10.5', 51490)
```  
Than you can start collecting by entering `start` in the command line and press enter. Then the data will start logging and show the datas in the command line as:
```sh
Logging: 651 4088
Logging: 652 4090
Logging: 653 4092
Logging: 654 4091
Logging: 655 4092
```  
When finished, to save the file, simpliy enter `log` and press enter to save the file(the command line will keep refreshing the output so don't worry if your input is over write by the out put). Then you can find the data in the location that you defined earlier.  
  
After entering `log`, the process will stop, saving the file and start asking you for file location agian, you can continue with the next data collection directly with the same step: enter the desired location, enter start(no need for rest of the broad), enter `log` if finished. And if done with the entire process, enter `e` to stop the program and shut down the server.
#### Data collection for four sensor
For collecting data for four sensor, the process is simillar with the previous one, be fore running the `sever_for_four.py` file make sure the IP, port and other requirements are enter correclty for `sever_for_four.py` and `WiFi_Client.cpp`.  
  
Prepare 4 Xiao Seeed broad with code uploded to them, connect power to them and start the server with:
```sh
python sever_for_four.py
```  
After running the command line will show the same thing as:
```sh
Server listening on 172.20.10.3:8080
starting user thread
Please input the file location for the data: 
```  
Then same enter the file name and location you want to save the data. Then the command line will ask to enter the angles for the 4 sensors:
```sh
Please input angles separate with space: 
```
Enter the angle(Ex:10 20 30 40), the angles are the real angle of each broads, and how the broads are labeled is accroding to the sequence of the broad is connected to the server. For example is board 1 is connected first then it will be asigned with the angle label of 10 and so on.

Next press the reset button on the broads, and as they reset and connected to the server, the command line will output:
```sh
Waiting for connection: [1/4]
Waiting for connection: [2/4]
Waiting for connection: [3/4]
Waiting for connection: [4/4]
```
When all broad is connected, enter `start` and enter to start the data collection, then the command line will output the readings of the 4 broad:
```sh
Device  1 : 4092 Device  2 : 4089 Device  3 : 4094 Device  4 : 4091
```  
To save the data first enter `log`, this will stop the process and fetch the datas from all 4 broads, then enter `save` to save the file to the location entered earlier. And same after saving, the command line will ask you to enter the location for saving the data again, you can then start your next collection direclty by repeating the same process(there some time will have output bugs, which the output of the command line doesn't match what is mentioned above, but you can ignore it and follow the same input process).
### Model Training for one sensor
After data collection, a model can be trained with the data to predict the angle of the knitted senor. In the `NeuralNetwork` directory there is a pre-defined netwrork `Network_for_one.py` for training a model to predict the angle for only one sensor.  

Before training, since the data for one sensor is stored separated with different angle, we will want to mege them. To merge the data into single one for training, use the `merge.py` file in `datas/` which replace the file name in the code with the file directoryof your data, and it will merge the data into one and store into `datas/Merged`.  
  
After merging the data, you can replace the file name in `Train_for_one.py` to your merged data for training, and you can tune the hyperparameter there. After training, the trained model will be saved in `./NerualNetwork/Trained_models`.
### Evaluating the trained model
To evaluate the trained model, you can use `Evaluate.py` to evaluate the trained model's performence on a specific dataset, for `Live_Evaluation_for_one.py` and `Live_Evaluation_for_four.py` you can see the prediction of the reading with the sensor in action.  
  
The usage of `Evaluate.py` is straight forward, replace the path to your dataset that you want to use for testing the model and the model you want to test. The code will test the model with your dataset and count the number of prediction that has errors under 5, 10, 20, and 30 degree, if the errors are under 5 then we see it as correct otherwise incorrect. At the end the code will output the number of correct predictions and incorrect predictions and the accuraccy of the model.  
  
To run `Live_Evaluation_for_one.py` and `Live_Evaluation_for_four.py`, refer to the [Data Collection](#data-collection) section which it is very simillar. After the broads are connected to the server, enter `start` and the code will then output the prediction of the angle of the sensor, and enter `e` to stop.




