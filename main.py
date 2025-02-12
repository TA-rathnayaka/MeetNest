from vidstream import *
import netifaces
import tkinter as tk
import socket
import threading
import re

# Function to validate the entered IP address
def is_valid_ip(ip):
    regex = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(regex, ip) is not None

def get_local_ip():
    # Use netifaces to fetch the local IP address of the default network interface
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        # Check if the interface has an 'inet' (IPv4) address
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            ip_info = netifaces.ifaddresses(interface)[netifaces.AF_INET]
            for addr in ip_info:
                # If an IP address exists, return it
                return addr['addr']
    return '127.0.0.1'  # Fallback to localhost if no IP address is found

local_ip_address = get_local_ip()
print("Local IP Address:", local_ip_address)

# Create server and receiver instances
server = StreamingServer(local_ip_address, 9999) 
receiver = AudioReceiver(local_ip_address, 8888)

# Function to start the listening process
def start_listening():
    t1 = threading.Thread(target=server.start_server)
    t2 = threading.Thread(target=receiver.start_server)
    t1.start()
    t2.start()

# Function to start the camera stream
def start_camera_stream():
    target_ip = text_target_ip.get()
    if is_valid_ip(target_ip):
        camera_client = CameraClient(target_ip, 7777)
        t3 = threading.Thread(target=camera_client.start_stream)
        t3.start()
    else:
        print("Invalid IP Address")

# Function to start screen sharing
def start_screen_sharing():
    target_ip = text_target_ip.get()
    if is_valid_ip(target_ip):
        screen_client = ScreenShareClient(target_ip, 7777)
        t4 = threading.Thread(target=screen_client.start_stream)
        t4.start()
    else:
        print("Invalid IP Address")

# Function to start audio stream
def start_audio_stream():
    target_ip = text_target_ip.get()
    if is_valid_ip(target_ip):
        audio_client = AudioSender(target_ip, 6666)
        t5 = threading.Thread(target=audio_client.start_stream)
        t5.start()
    else:
        print("Invalid IP Address")

# GUI setup
window = tk.Tk()
window.title("MeetNest")
window.geometry("300x200")

label_target_ip = tk.Label(window, text="Target IP:") 
label_target_ip.pack()

text_target_ip = tk.Entry(window, width=30)
text_target_ip.pack()

btn_listen = tk.Button(window, text="Start Listening", width=50, command=start_listening)
btn_listen.pack(anchor=tk.CENTER, expand=True)  

btn_camera = tk.Button(window, text="Start Camera Stream", width=50, command=start_camera_stream)
btn_camera.pack(anchor=tk.CENTER, expand=True)  

btn_screen = tk.Button(window, text="Start Screen Sharing", width=50, command=start_screen_sharing)
btn_screen.pack(anchor=tk.CENTER, expand=True)

btn_audio = tk.Button(window, text="Start Audio Stream", width=50, command=start_audio_stream)
btn_audio.pack(anchor=tk.CENTER, expand=True)  

window.mainloop()