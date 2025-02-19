import tkinter as tk
from tkinter import ttk, messagebox
import netifaces
import socket
import threading
import re
from vidstream import *
from ui import create_ui  # Make sure this matches your updated UI module

class StreamingApp:
    def __init__(self, local_port=9999, audio_port=8888, camera_port=7777, 
                 screen_port=6666, audio_send_port=5555):
        self.local_ip = self.get_local_ip()
        self.running = False
        self.active_streams = {}
        
        # Initialize servers
        self.server = StreamingServer(self.local_ip, local_port)
        self.audio_receiver = AudioReceiver(self.local_ip, audio_port)
        
        # Port configurations
        self.camera_port = camera_port
        self.screen_port = screen_port
        self.audio_send_port = audio_send_port
        
        # Initialize UI
        self.window, self.text_target_ip = create_ui(
            self.toggle_listening, 
            self.toggle_camera_stream,
            self.toggle_screen_sharing,
            self.toggle_audio_stream,
            self.local_ip
        )
        
        # UI State management
        self.setup_ui_state()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui_state(self):
        """Initialize UI component states"""
        self.listening_active = False
        self.camera_active = False
        self.screen_active = False
        self.audio_active = False

    @staticmethod
    def get_local_ip():
        """Get first non-loopback IPv4 address"""
        try:
            interfaces = netifaces.interfaces()
            for interface in interfaces:
                if interface == 'lo':
                    continue
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        if 'addr' in addr and addr['addr'] != '127.0.0.1':
                            return addr['addr']
            return '127.0.0.1'
        except Exception as e:
            messagebox.showerror("Network Error", f"Failed to get local IP: {str(e)}")
            return '127.0.0.1'

    def validate_ip(self, ip):
        """Validate IPv4 address using socket library"""
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def toggle_listening(self):
        """Toggle server listening state"""
        if not self.listening_active:
            try:
                threading.Thread(target=self.server.start_server, daemon=True).start()
                threading.Thread(target=self.audio_receiver.start_server, daemon=True).start()
                self.listening_active = True
                self.update_status("Listening for connections...")
            except Exception as e:
                messagebox.showerror("Server Error", f"Failed to start servers: {str(e)}")
                self.listening_active = False
        else:
            self.server.stop_server()
            self.audio_receiver.stop_server()
            self.listening_active = False
            self.update_status("Servers stopped")

    def toggle_stream(self, stream_type, client_class, port, button):
        """Generic toggle for stream types"""
        target_ip = self.text_target_ip.get().strip()
        
        if not self.validate_ip(target_ip):
            messagebox.showerror("Invalid IP", "Please enter a valid IPv4 address")
            return

        if not self.active_streams.get(stream_type):
            try:
                client = client_class(target_ip, port)
                thread = threading.Thread(target=client.start_stream, daemon=True)
                thread.start()
                self.active_streams[stream_type] = (client, thread)
                button.config(text=f"Stop {stream_type}")
                self.update_status(f"{stream_type} stream started")
            except Exception as e:
                messagebox.showerror("Stream Error", f"Failed to start {stream_type}: {str(e)}")
        else:
            client, thread = self.active_streams.pop(stream_type)
            client.stop_stream()
            button.config(text=f"Start {stream_type}")
            self.update_status(f"{stream_type} stream stopped")

    def toggle_camera_stream(self):
        self.toggle_stream('camera', CameraClient, self.camera_port, self.window.btn_camera)

    def toggle_screen_sharing(self):
        self.toggle_stream('screen', ScreenShareClient, self.screen_port, self.window.btn_screen)

    def toggle_audio_stream(self):
        self.toggle_stream('audio', AudioSender, self.audio_send_port, self.window.btn_audio)

    def update_status(self, message):
        """Update status bar with timestamp"""
        if hasattr(self.window, 'status_label'):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.window.status_label.config(text=f"{timestamp} - {message}")

    def on_close(self):
        """Cleanup resources on window close"""
        self.running = False
        
        # Stop all active streams
        for stream_type in list(self.active_streams.keys()):
            client, thread = self.active_streams.pop(stream_type)
            client.stop_stream()
        
        # Stop servers
        if self.listening_active:
            self.server.stop_server()
            self.audio_receiver.stop_server()
        
        self.window.destroy()

    def run(self):
        self.running = True
        try:
            self.window.mainloop()
        except KeyboardInterrupt:
            self.on_close()