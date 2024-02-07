import customtkinter as ctk
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
import os

def download_video():
    url = entry_url.get()
    resolution = resolution_var.get()
    progress_label.pack(pady=(10, 5))
    progress_bar.pack(pady=(10, 5))
    status_label.pack(pady=(10, 5))
    
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.filter(res=resolution, progressive=True, file_extension="mp4").first()
        if not stream:
            raise ValueError(f"No stream found for resolution {resolution}.")
        
        download_dir = choose_directory()
        if not download_dir:
            return
        
        file_path = os.path.join(download_dir, f"{yt.title}.mp4")
        stream.download(output_path=download_dir)
        status_label.configure(text="Downloaded!", text_color="white", fg_color="green")

    except Exception as e:
        status_label.configure(text=f"Error: {str(e)}", text_color="white", fg_color="red")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completed = bytes_downloaded / total_size * 100
    progress_label.configure(text=f"{int(percentage_completed)}%")
    progress_label.update()
    progress_bar.set(float(percentage_completed))

def choose_directory():
    download_directory = filedialog.askdirectory()
    if download_directory:
        return download_directory
    else:
        status_label.configure(text="Please select a directory.", text_color="white", fg_color="red")

#create a root window
root = ctk.CTk()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

#title of the window
root.title("Youtube Downloader!")

#set min and max width and height
root.geometry("720x480")
root.minsize(720, 480)
root.maxsize(1080, 720)

#create a frame to hold the content
content_frame = ctk.CTkFrame(root)
content_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

# create a label for the heading
heading_label = ctk.CTkLabel(content_frame, text="Youtube Downloader", font=("Arial", 20, "bold"))
heading_label.pack(pady=(10, 20))

# create a label and the entry widget for the video url
url_label = ctk.CTkLabel(content_frame, text="Enter the youtube url here :")
entry_url = ctk.CTkEntry(content_frame, width=400, height=40)
url_label.pack(pady=(10, 5))
entry_url.pack(pady=(10, 5))

# create a label for resolution selection
resolution_label = ctk.CTkLabel(content_frame, text="Select Resolution:")
resolution_label.pack(pady=(10, 5))

# create a resolutions combo box
resolutions = ["720p", "480p", "360p", "240p", "144p"]
resolution_var = ctk.StringVar()
resolution_combobox = ttk.Combobox(content_frame, values=resolutions, textvariable=resolution_var) 
resolution_combobox.pack(pady=(5, 10))
resolution_combobox.set("720p")

# create a download button
download_button = ctk.CTkButton(content_frame, text="Download", command=download_video)
download_button.pack(pady=(10, 5))

# create a label and the progress bar to display the download progress
progress_label = ctk.CTkLabel(content_frame, text="0%") 
progress_label.pack(pady=(10, 5))
progress_bar = ctk.CTkProgressBar(content_frame) 
progress_bar.set(0) 
progress_bar.pack(pady=(10, 5))

# create the status label
status_label = ctk.CTkLabel(content_frame, text="")
status_label.pack(pady=(10, 5))

# create the "Made by TK" label
made_by_label = ctk.CTkLabel(content_frame, text="Made by TK", font=("Arial", 10))
# pack the label at the bottom
made_by_label.pack(side=ctk.BOTTOM, pady=(10, 0))

# to start the app
root.mainloop()
