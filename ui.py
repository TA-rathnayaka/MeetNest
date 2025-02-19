import tkinter as tk
from tkinter import ttk, font

def create_ui(start_listening, start_camera_stream, start_screen_sharing, 
              start_audio_stream, local_ip):
    # Configure main window
    window = tk.Tk()
    window.title("MeetNest")
    window.geometry("800x600")
    window.configure(bg="#2d2d2d")
    
    # Custom fonts
    bold_font = font.Font(family="Helvetica", size=12, weight="bold")
    regular_font = font.Font(family="Helvetica", size=11)
    small_font = font.Font(family="Helvetica", size=10)
    
    # Header Section
    header_frame = tk.Frame(window, bg="#2d2d2d")
    header_frame.pack(fill=tk.X, padx=20, pady=10)
    
    title_label = tk.Label(header_frame, 
                         text="MeetNest",
                         font=bold_font,
                         fg="white",
                         bg="#2d2d2d")
    title_label.pack(side=tk.LEFT)
    
    # Connection Panel
    connection_frame = ttk.LabelFrame(window, 
                                    text=" Connection ",
                                    style="Dark.TLabelframe",
                                    padding=(20, 10))
    connection_frame.pack(fill=tk.X, padx=20, pady=10)
    
    ip_entry = ttk.Entry(connection_frame,
                       width=40,
                       style="Dark.TEntry",
                       font=regular_font)
    ip_entry.pack(side=tk.LEFT, padx=(0, 10))
    
    connect_btn = ttk.Button(connection_frame,
                           text="Connect",
                           style="Accent.TButton",
                           command=lambda: start_listening())
    connect_btn.pack(side=tk.LEFT)
    
    # Media Controls
    controls_frame = ttk.LabelFrame(window,
                                  text=" Media Controls ",
                                  style="Dark.TLabelframe",
                                  padding=(20, 15))
    controls_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    btn_style = {"style": "Dark.TButton", "width": 20}
    
    btn_grid = tk.Frame(controls_frame, bg="#404040")
    btn_grid.pack(expand=True)
    
    btn_camera = ttk.Button(btn_grid,
                          text="📷 Start Camera",
                          command=start_camera_stream,
                          **btn_style)
    btn_camera.grid(row=0, column=0, padx=10, pady=5)
    
    btn_screen = ttk.Button(btn_grid,
                          text="🖥️ Start Sharing",
                          command=start_screen_sharing,
                          **btn_style)
    btn_screen.grid(row=0, column=1, padx=10, pady=5)
    
    btn_audio = ttk.Button(btn_grid,
                         text="🎙️ Start Audio",
                         command=start_audio_stream,
                         **btn_style)
    btn_audio.grid(row=1, column=0, padx=10, pady=5)
    
    btn_listen = ttk.Button(btn_grid,
                          text="👂 Start Listening",
                          command=start_listening,
                          **btn_style)
    btn_listen.grid(row=1, column=1, padx=10, pady=5)
    
    # Status Bar
    status_bar = tk.Frame(window, bg="#404040", height=25)
    status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    status_label = tk.Label(status_bar,
                          text=f"Local IP: {local_ip} • Ready",
                          fg="#888888",
                          bg="#404040",
                          font=small_font)
    status_label.pack(side=tk.LEFT, padx=10)
    
    # Style Configuration
    style = ttk.Style()
    style.theme_use('clam')
    
    # Dark theme colors
    style.configure("Dark.TButton",
                    foreground="white",
                    background="#404040",
                    bordercolor="#404040",
                    relief="flat",
                    padding=8,
                    font=regular_font)
    style.map("Dark.TButton",
            background=[('active', '#505050'), ('pressed', '#606060')])
    
    style.configure("Accent.TButton",
                  foreground="white",
                  background="#007AFF",
                  bordercolor="#007AFF",
                  relief="flat")
    style.map("Accent.TButton",
            background=[('active', '#298EFF'), ('pressed', '#0066CC')])
    
    style.configure("Dark.TEntry",
                  fieldbackground="#404040",
                  foreground="white",
                  insertcolor="white",
                  bordercolor="#505050",
                  relief="flat")
    
    style.configure("Dark.TLabelframe",
                  background="#2d2d2d",
                  foreground="white",
                  bordercolor="#404040")
    style.configure("Dark.TLabelframe.Label",
                  background="#2d2d2d",
                  foreground="white")
    
    return window, ip_entry