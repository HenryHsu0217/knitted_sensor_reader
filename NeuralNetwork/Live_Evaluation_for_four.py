"""
Code for starting a sever for four sensors, please make sure that the wifi that you use is a 
private wifi(so public wifi such as aalto open won't work).
"""
import socket
import threading
import numpy as np
import queue
import sys
from Network_for_one import NeuralNetwork
import torch
 # Defining the global variables for user control
global user_input
global server_running
global file
user_input="HI"
server_running = True
file=""

 # Function for handling client(sensor)
def handle_client(client_socket,q_data_save,q_data_print, thread_id,model):
    data_to_save=[] # A list that will store the complete data
    global user_input
    global file
    try:
        while server_running:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                if user_input=="start": # If the user input is "start", then start adding the data into the data_to_save list
                    decoded_data = data.decode().strip()  # The input data from the sensor will be in the format of: [data_count analog_reading] 
                    splited=decoded_data.split(" ")  # Splits the data with space, so the "splited" variable are now ["data_count", "analog_reading"]
                    if len(splited)==2:  # Skip datas that have more then one reading due to that the server may not handle the incoming data as fast as it revceived, causing multiple data in one input
                        input=float(splited[1])
                        input_normed=input/4095
                        q_data_print.put((thread_id, "{:.4f}".format(model(torch.tensor([input_normed], dtype=torch.float32)).detach().numpy()[0]))) # Added the reading to the queue with thread ID as the device ID
                        data_to_save.append((splited[1],60)) # Modify the real angle or other lable value here
                elif user_input=="log":
                    q_data_save.put((thread_id, data_to_save)) # If user input is "log", add the entire data that want be saved for this device into the queue
                    user_input=="HI"
                elif user_input=="e":
                    client_socket.close()
                    break
                else:
                    pass
            except socket.error as e:
                print("Socket error:", e)
                break
    finally:
        client_socket.close()

 # Function for handling user inputs 
def handle_user():
    global user_input
    global server_running
    global file
    print("starting user thread")
    while True:
        user_input=input()
        if user_input == "e":
            print("Shutting down server...")
            server_running = False
            break
 # Function for handling datas from the four sensors
def handle_datas(q_data_save,q_data_print):
    global user_input
    global server_running
    global file
    latest_data = {}
    while True:
         # Print out the readings from the four sensors
        while not q_data_print.empty() and user_input!="log" and user_input!="e": # Keep getting datas from the queue untill it is empty
            thread_id, data = q_data_print.get_nowait() # Get the data accroding to the device ID
            latest_data[thread_id] = data 
            output = ' '.join(f"Device {tid}, angle: {d}" for tid,d in sorted(latest_data.items())) # Print out the readings
            sys.stdout.write(f"\r{output}")
            sys.stdout.flush()
        if not server_running or user_input=="e":
            break
def server():
    global server_running
    host = '172.20.10.3'  ### Replace with your device's IP
    port = 8080  
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    server_socket.settimeout(1.0)
    print(f"Server listening on {host}:{port}")
    q_data_save = queue.Queue()
    q_data_print = queue.Queue()
    threads=[]
    user_thread=threading.Thread(target=handle_user)
    user_thread.start()
    data_thread=threading.Thread(target=handle_datas,args=(q_data_save,q_data_print))
    data_thread.start()
    model=NeuralNetwork()
    model.load_state_dict(torch.load('Trained_models/model_1.pth')) # Load the trained model that you want to test
    model.eval()
    try:
        thread_id = 1
        while True:
            if not server_running:
                break
            try:
                client_socket, addr = server_socket.accept()
                print(f"Waiting for connection: [{len(threads)+1}/4]")
                client_thread = threading.Thread(target=handle_client, args=(client_socket,q_data_save,q_data_print,thread_id,model))
                client_thread.start()
                threads.append(client_thread)
                thread_id += 1
            except socket.timeout:
                continue
    finally:
        server_socket.close()
        print("Closing server...")
        for t in threads:
            t.join()  
        print("Server closed.")

if __name__ == "__main__":
    server()