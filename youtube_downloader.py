import tkinter as tk
from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL
import os
import subprocess
import threading
import sys

class ConsoleOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

    def flush(self):
        pass

def download_video():
    url = url_entry.get()
    download_path = path_label.cget("text")
    
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return
    
    if not download_path or download_path == "Select Download Location":
        messagebox.showerror("Error", "Please select a download location")
        return
    
    # Start the download and re-encode process in a new thread
    threading.Thread(target=process_video, args=(url, download_path)).start()

def process_video(url, download_path):
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
        
        # Construct the input and output file paths
        original_file = os.path.join(download_path, f"{video_title}.mp4")
        renamed_original_file = os.path.join(download_path, f"{video_title}_original.mp4")
        output_file = original_file  # Re-encoded file will have the original name
        
        # Rename the original file
        if os.path.exists(original_file):
            os.rename(original_file, renamed_original_file)
        
        # Re-encode the video using ffmpeg
        ffmpeg_command = [
            'ffmpeg', '-i', renamed_original_file, '-c:v', 'libx264', '-preset', 'slow', '-crf', '22',
            '-c:a', 'aac', '-b:a', '192k', '-strict', 'experimental', output_file
        ]
        
        subprocess.run(ffmpeg_command, check=True)
        
        # Remove the renamed original file
        if os.path.exists(renamed_original_file):
            os.remove(renamed_original_file)
        
        messagebox.showinfo("Success", f"Video downloaded and re-encoded successfully to {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download or re-encode video: {e}")

def select_path():
    path = filedialog.askdirectory()
    if path:
        path_label.config(text=path)

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# URL Entry
url_label = tk.Label(root, text="YouTube URL:")
url_label.pack(pady=5, padx=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5, padx=10)

# Download Path
path_button = tk.Button(root, text="Select Download Location", command=select_path)
path_button.pack(pady=5, padx=10)

# Set default download path to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
path_label = tk.Label(root, text=desktop_path)
path_label.pack(pady=5, padx=10)

# Console Output
console_output = tk.Text(root, height=10, width=70, wrap='word')
console_output.pack(pady=10, padx=10)

# Redirect stdout and stderr
sys.stdout = ConsoleOutput(console_output)
sys.stderr = ConsoleOutput(console_output)

# Download Button
download_button = tk.Button(root, text="Download Video", command=download_video)
download_button.pack(pady=20, padx=10)

# Run the application
root.mainloop() 