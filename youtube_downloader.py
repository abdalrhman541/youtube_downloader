import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
import random
import yt_dlp as youtube_dl

# List of YouTube slogans
slogans = [
    "Broadcast Yourself!",
    "Experience the World of Video.",
    "Where the World Watches.",
    "Share Your Story with the World.",
    "Tune In, Chill Out."
]

def update_progress(d):
    """Update the progress bar and status label with download progress."""
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)

        if total:
            percentage = (downloaded / total) * 100
            progress_bar['value'] = percentage
            status_label.config(text=f"Downloading... {percentage:.2f}% complete")
        else:
            status_label.config(text="Downloading... Calculating progress")

    elif d['status'] == 'finished':
        progress_bar['value'] = 100
        status_label.config(text="Download completed successfully!")

def download_video(format_type):
    """Generic function to handle video/audio downloads."""
    link = entry.get()
    filename = filename_entry.get()
    if not link:
        messagebox.showerror("Error", "Please enter a YouTube link")
        return
    if not filename:
        messagebox.showerror("Error", "Please enter a name for the video")
        return

    try:
        status_label.config(text=f"Starting {format_type} download...")
        progress_bar['value'] = 0
        options = {
            'format': format_type,
            'outtmpl': f'{filename}.%(ext)s',
            'progress_hooks': [update_progress],
            'nocolor': True,
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([link])
    except Exception as e:
        status_label.config(text="Error occurred during download")
        messagebox.showerror("Error", str(e))

def download_high_res():
    download_video('best')

def download_low_res():
    download_video('worst')

def download_audio():
    download_video('bestaudio')

def threaded_download(func):
    thread = threading.Thread(target=func)
    thread.start()

# Setting up the tkinter window
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("600x400")
root.configure(bg="red")  # Set the background color to red

# Slogan Display
slogan_label = tk.Label(root, text=random.choice(slogans), font=("Arial", 14, "bold"), bg="red", fg="white")
slogan_label.pack(pady=10)

# Input frame for link and filename
frame = tk.Frame(root, bg="red")
frame.pack(pady=10)

entry_label = tk.Label(frame, text="YouTube Link:", font=("Arial", 12), bg="red", fg="white")
entry_label.grid(row=0, column=0, padx=5, sticky="e")

entry = tk.Entry(frame, width=40, font=("Arial", 12))
entry.grid(row=0, column=1, padx=5)

filename_label = tk.Label(frame, text="Save As:", font=("Arial", 12), bg="red", fg="white")
filename_label.grid(row=1, column=0, padx=5, sticky="e")

filename_entry = tk.Entry(frame, width=40, font=("Arial", 12))
filename_entry.grid(row=1, column=1, padx=5)

# Buttons
button_style = {
    'font': ("Arial", 10, "bold"),
    'width': 20,
    'height': 2,
    'relief': "ridge",
    'bd': 3
}

button_frame = tk.Frame(root, bg="red")
button_frame.pack(pady=10)

high_res_button = tk.Button(button_frame, text="Download High-Res Video", bg="#8B0000", fg="white", command=lambda: threaded_download(download_high_res), **button_style)
high_res_button.grid(row=0, column=0, padx=10, pady=5)

low_res_button = tk.Button(button_frame, text="Download Low-Res Video", bg="#8B0000", fg="white", command=lambda: threaded_download(download_low_res), **button_style)
low_res_button.grid(row=0, column=1, padx=10, pady=5)

audio_button = tk.Button(button_frame, text="Download Audio", bg="#8B0000", fg="white", command=lambda: threaded_download(download_audio), **button_style)
audio_button.grid(row=1, column=0, columnspan=2, pady=10)

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=20)

# Status label
status_label = tk.Label(root, text="", fg="white", bg="red", font=("Arial", 12))
status_label.pack(pady=10)

# Start the tkinter event loop
root.mainloop()
