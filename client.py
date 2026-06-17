import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

HOST = "127.0.0.1"
PORT = 5001

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = input("Enter your username: ")

# Username exchange
client.recv(1024)  # Receive "USERNAME"
client.send(username.encode())

# ---------------- GUI ----------------
window = tk.Tk()
window.title(f"ParaChat - {username}")
window.geometry("420x520")
window.config(bg="#1e1e1e")

# Chat box
chat_area = scrolledtext.ScrolledText(
    window,
    bg="#2b2b2b",
    fg="white",
    font=("Arial", 11),
    state='disabled'
)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(window, font=("Arial", 12))
entry.pack(padx=10, pady=5, fill=tk.X)

# ============ COLOR CONFIGURATION ============
# You can change these colors to anything you want!

# Option 1: Default Colors (Cyan for self, White for others, Green for system)
COLOR_SELF = "cyan"           # Your own messages
COLOR_OTHER = "white"         # Other people's messages  
COLOR_SYSTEM = "light green"  # Join/leave notifications

# Option 2: Warm Colors (Uncomment to use)
# COLOR_SELF = "#FF6B35"      # Orange
# COLOR_OTHER = "#F7C59F"     # Light orange/peach
# COLOR_SYSTEM = "#4ECDC4"    # Turquoise

# Option 3: Cool Colors (Uncomment to use)
# COLOR_SELF = "#00B4D8"      # Bright blue
# COLOR_OTHER = "#90E0EF"     # Light blue
# COLOR_SYSTEM = "#CAF0F8"    # Very light blue

# Option 4: Professional Colors (Uncomment to use)
# COLOR_SELF = "#2E86AB"      # Dark blue
# COLOR_OTHER = "#A23B72"     # Purple
# COLOR_SYSTEM = "#F18F01"    # Orange

# Option 5: Neon Colors (Uncomment to use)
# COLOR_SELF = "#00FF00"      # Bright green
# COLOR_OTHER = "#00FFFF"     # Cyan
# COLOR_SYSTEM = "#FF00FF"    # Magenta

# Option 6: Pastel Colors (Uncomment to use)
# COLOR_SELF = "#FFB3BA"      # Pastel pink
# COLOR_OTHER = "#B5EAD7"     # Pastel green
# COLOR_SYSTEM = "#C7CEE6"    # Pastel purple

# ============================================

def show_message(msg):
    chat_area.config(state='normal')
    
    # Color coding based on message type
    if "joined" in msg or "left" in msg:
        chat_area.insert(tk.END, msg + "\n", "system")
    elif msg.startswith(f"{username}:"):
        # Your own messages
        chat_area.insert(tk.END, msg + "\n", "self")
    else:
        # Others' messages
        chat_area.insert(tk.END, msg + "\n", "other")
    
    chat_area.config(state='disabled')
    chat_area.yview(tk.END)  # Auto-scroll to bottom

# Configure tag styles with your chosen colors
chat_area.tag_config("system", foreground=COLOR_SYSTEM)
chat_area.tag_config("self", foreground=COLOR_SELF)
chat_area.tag_config("other", foreground=COLOR_OTHER)

# Optional: Add background colors to messages (uncomment if wanted)
# chat_area.tag_config("self", foreground=COLOR_SELF, background="#1a3a3a")
# chat_area.tag_config("other", foreground=COLOR_OTHER, background="#2a2a2a")

# ---------------- RECEIVE ----------------
def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg:
                show_message(msg)
        except:
            show_message("❌ Disconnected from server")
            break

# ---------------- SEND ----------------
def send(event=None):
    message = entry.get().strip()
    if message:
        full_message = f"{username}: {message}"
        
        # Display your own message immediately
        show_message(full_message)
        
        # Send to server for others
        client.send(full_message.encode())
        
        # Clear input field
        entry.delete(0, tk.END)

# Send button
btn = tk.Button(
    window,
    text="Send",
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold"),
    command=send
)
btn.pack(pady=5)

# Bind Enter key to send
entry.bind("<Return>", send)

# Start receive thread
threading.Thread(target=receive, daemon=True).start()

# Start GUI
window.mainloop()