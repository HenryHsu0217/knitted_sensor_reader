"""
Code for starting a sever for only one sensor, please make sure that the wifi that you use is a 
private wifi(so public wifi such as aalto open won't work).
"""
import socket
import threading
import numpy as np
 # Defining the global variables for user control
global user_input
global server_running
global file
user_input="HI"
server_running = True
file=""

 # Function for handling client(sensor)
def handle_client(client_socket):
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
                    if decoded_data:
                        print(f"Logging: {decoded_data}")
                    splited=decoded_data.split(" ") # Splits the data with space, so the "splited" variable are now ["data_count", "analog_reading"]
                    if len(splited)==2: # Skip datas that have more then one reading due to that the server may not handle the incoming data as fast as it revceived, causing multiple data in one input
                        data_to_save.append((splited[1],60)) # Modify the real angle value here
                elif user_input=="log": # If user input is log then save the data
                    data_values, true_values = zip(*data_to_save)
                    np.savez(file, data_values=data_values, true_values=true_values)
                    user_input="Hi"
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
    global file
    print("starting user thread")
    file=input("Please input the file location for the data: ") # Enter the file location that you want to save your data
    while True:
        if file!="" and user_input=="log":
            file=input("Please input the file location for the data: ")
        user_input=input()
        if user_input == "e":
            print("Shutting down server...")
            server_running = False
            break

 # Main funciton for setting up and runs the server
def server():
    global server_running
    host = '172.20.10.3'  # Change the IP address to your server address
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
    try:
        while True:
            if not server_running:
                break
            try:
                client_socket, addr = server_socket.accept()
                print(f"Accepted connection from {addr}")
                client_thread = threading.Thread(target=handle_client, args=(client_socket,))
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