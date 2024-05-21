"""
Live evaluation of the model with live data readings from the sensor
"""
import socket
import threading
from Network_for_one import NeuralNetwork
import torch
global user_input
global server_running
user_input="HI"
server_running = True

 # Function for handling client(sensor)
def handle_client(client_socket,model):
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
                    decoded_data = data.decode().strip() # The input data from the sensor will be in the format of: [data_count analog_reading] 
                    splited=decoded_data.split(" ") # Splits the data with space, so the "splited" variable are now ["data_count", "analog_reading"]
                    if len(splited)==2: # Skip datas that have more then one reading due to that the server may not handle the incoming data as fast as it revceived, causing multiple data in one input
                        input=float(splited[1])
                        input_normed=input/4095
                        print(f"Predicted angle: {model(torch.tensor([input_normed], dtype=torch.float32)).detach().numpy()[0]}") # Modify the real angle value here
                elif user_input=="e": # If user input is "e" exit and close the server
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
    print("starting user thread")
    while True:
        user_input=input()
        if user_input == "e":
            print("Shutting down server...")
            server_running = False
            break

 # Main funciton for setting up and runs the server
def server():
    global server_running
    host = '172.20.10.3'  ### Replace with your device's IP
    port = 8080  # Port to listen on
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    server_socket.settimeout(1.0)
    print(f"Server listening on {host}:{port}")
    threads=[]
    user_thread=threading.Thread(target=handle_user)
    user_thread.start()
    model=NeuralNetwork()
    model.load_state_dict(torch.load('Trained_models/model_1.pth')) # Load the trained model that you want to test
    model.eval()
    try:
        while True:
            if not server_running:
                break
            try:
                client_socket, addr = server_socket.accept()
                print(f"Accepted connection from {addr}")
                client_thread = threading.Thread(target=handle_client, args=(client_socket,model))
                client_thread.start()
                threads.append(client_thread)
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