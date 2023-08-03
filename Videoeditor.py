import tkinter as tk
from tkinter import filedialog
import cv2
import PIL.Image, PIL.ImageTk
from collections import deque
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
from tkinter import ttk
import moviepy.editor as mp

import tkinter as tk
from PIL import ImageTk, Image


# Create the main window
root = tk.Tk()
root.title("Video Editing App")
root.attributes("-fullscreen", True)
audio_clip = None
# Make the window fullscreen


# Load the image
bg_image = Image.open(""C:\\Users\MBG Traders\Desktop\\PAI PROJECT\\Pict.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a Frame for the video player
video_frame = tk.Frame(root, bg="black")
video_frame.grid(row=0, column=0, sticky="nsew")


# Create a Frame for the options
options_frame = tk.Frame(root, bg="black")
options_frame.grid(row=0, column=1, sticky="nsew")

# Create a Label with the image as the background
options_frame_bg = tk.Label(options_frame, image=bg_photo)
options_frame_bg.place(x=0, y=0, relwidth=1, relheight=1)



# Divide the window evenly between the two frames
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480

# Global variables
video_path = ""  # Variable to store the video file path
video_capture = None  # Variable to store the video capture object
speed_values = {"Fast": 10, "Normal": 1, "Slow": 0.1}  # Mapping of speed values
filter_stack = deque()  # Stack to store applied filters
frame_stack = deque()  # Stack to store video frames
speed_var = tk.StringVar()  # Variable to store the selected speed

def open_video():
    global video_path, video_capture, audio_clip
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
    if video_path:
        video_capture = cv2.VideoCapture(video_path)
        update_button_visibility()  # Call the function to update button visibility
        play_video()
# Function to apply the selected filter to the frame
def apply_filter(frame):
    if filter_stack:
        filter_code = filter_stack[-1]
        if filter_code is not None:
            frame = filter_code(frame)
    return frame

import time
import tkinter as tk
from tkinter import filedialog
import moviepy.editor as mp

def stop_preview(preview_window):
    # Function to stop the preview
    preview_window.close()

def add_music():
    global video_path, audio_clip

    if video_path:
        audio_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3")])
        if audio_path:
            # Load the video and audio clips
            video_clip = mp.VideoFileClip(video_path)
            audio_clip = mp.AudioFileClip(audio_path)

            # Set the audio for the video clip
            video_clip = video_clip.set_audio(audio_clip)

            # Resize the audio clip to match the video clip duration
            video_duration = video_clip.duration
            audio_clip = audio_clip.subclip(0, video_duration)

            # Preview the video with added music
            preview_window = video_clip.preview(fullscreen=False, newindowkey=0)  # Open the preview window in non-fullscreen mode

            # Create a button to stop the preview
            stop_button = tk.Button(text="Cut", command=lambda: stop_preview(preview_window))
            stop_button.pack()

            # Start the Tkinter event loop
            root.mainloop()
        else:
            print("Audio file not selected.")
    else:
        print("Video file not selected.")




# Define a global variable to keep track of the video playback state
is_playing = True
# Rest of the code...

def play_video():
    global video_capture, audio_clip, is_playing, is_audio_playing, photo, rotation_angle

    if video_path:
        if video_capture is None:
            video_capture = cv2.VideoCapture(video_path)

        speed = speed_var.get()
        speed_value = speed_values.get(speed, 1)

        if is_playing:
            ret, frame = video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Rest of the code to process and display the frame

                # Rotate the frame based on the current angle
                if rotation_angle == 90:
                    rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                elif rotation_angle == 180:
                    rotated_frame = cv2.rotate(frame, cv2.ROTATE_180)
                elif rotation_angle == 270:
                    rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                else:
                    rotated_frame = frame

                # Apply the selected filter to the rotated frame
                filtered_frame = apply_filter(rotated_frame)

                if audio_clip is not None and is_audio_playing:
                    # Calculate the video frame time in seconds
                    video_time = video_capture.get(cv2.CAP_PROP_POS_MSEC) / 1000

                    # Resize audio frame to match video frame dimensions
                    audio_frame = audio_clip.get_frame(t=video_time)
                    audio_frame = cv2.resize(audio_frame, (filtered_frame.shape[1], filtered_frame.shape[0]))

                    # Convert audio frame to compatible depth
                    audio_frame = cv2.convertScaleAbs(audio_frame)

                    # Convert audio frame to RGB format
                    audio_frame = cv2.cvtColor(audio_frame, cv2.COLOR_BGR2RGB)

                    # Mix audio and video frames
                    mixed_frame = cv2.addWeighted(filtered_frame, 0.8, audio_frame, 0.2, 0)

                    # Convert mixed frame to PIL Image
                    mixed_image = PIL.Image.fromarray(mixed_frame.astype(np.uint8))

                    # Create video clip from mixed frame
                    video_clip = mp.VideoClip(lambda t: np.array(mixed_image), duration=1.0 / video_capture.get(cv2.CAP_PROP_FPS))

                    # Set audio for the video clip
                    video_clip = video_clip.set_audio(audio_clip)

                    # Convert video clip to a format compatible with tkinter
                    video_clip = video_clip.resize((VIDEO_WIDTH, VIDEO_HEIGHT))

                    # Convert video frame to PIL Image
                    frame_image = PIL.Image.fromarray(video_clip.get_frame(0))
                else:
                    # Convert frame to PIL Image
                    frame_image = PIL.Image.fromarray(filtered_frame.astype(np.uint8))

                # Create PhotoImage from the PIL Image
                image = PIL.ImageTk.PhotoImage(frame_image)

                video_label.config(image=image)
                photo = image  # Store a reference to the PhotoImage object

            else:
                video_capture.release()
                return

        # Calculate the delay based on speed
        delay = int(1000 / (video_capture.get(cv2.CAP_PROP_FPS) * speed_value))
        root.after(delay, play_video)

def restart_video():
    global video_capture, is_playing
    if video_capture is not None:
        video_capture.release()
        video_capture = cv2.VideoCapture(video_path)
        is_playing = True
        play_video()
        
def toggle_playback():
    global is_playing

    if is_playing:
        is_playing = False
        play_button.config(text="Play")
    else:
        is_playing = True
        play_button.config(text="Pause")
        play_video()

def update_button_visibility():
    global is_playing

    if root.winfo_exists():  # Check if the root window still exists
        if is_playing:
            play_button.place_forget()
        else:
            play_button.place(x=10, y=10)  # Adjust the coordinates according to your layout       
# Create a button for play/pause
play_button = tk.Button(video_frame, text="Play", command=toggle_playback)
# Place the button at the bottom center of the video frame
play_button.pack(side="bottom", pady=20)
# Call the update_button_visibility function before calling play_video
# Create a label to display the video
video_label = tk.Label(video_frame, bg="black")
video_label.pack(expand=True)



# Function to apply the grayscale filter
def apply_grayscale_filter(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Function to undo the last applied filter
def undo_filter():
    if filter_stack:
        filter_stack.pop()

# Function to redo the previously undone filter
def redo_filter():
    if frame_stack and len(frame_stack) > len(filter_stack):
        frame_stack.pop()

# Function to apply the Sepia filter
def apply_sepia_filter(frame):
    sepia_kernel = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    sepia_frame = cv2.transform(frame, sepia_kernel)
    sepia_frame = cv2.cvtColor(sepia_frame, cv2.COLOR_BGR2RGB)
    return sepia_frame

# Function to apply the Blur filter
def apply_blur_filter(frame):
    return cv2.GaussianBlur(frame, (15, 15), 0)

# Function to apply the Canny Edge Detection filter
def apply_canny_edge_filter(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    return edges


        
def add_original_audio():
    global video_path
    if video_path:
        video_clip = mp.VideoFileClip(video_path)
        video_clip.preview()


def on_closing():
    global video_capture
    if video_capture is not None:
        video_capture.release()
    root.destroy()

rotation_angle = 0
def rotate_video():
    global video_capture, video_label, rotation_angle

    if video_capture is not None:
        # Read the current frame
        ret, frame = video_capture.read()
        if ret:
            # Update the rotation angle
            rotation_angle += 90
            rotation_angle %= 360  # Keep the angle within 0 to 359 degrees

            # Rotate the frame based on the current angle
            if rotation_angle == 90:
                rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            elif rotation_angle == 180:
                rotated_frame = cv2.rotate(frame, cv2.ROTATE_180)
            elif rotation_angle == 270:
                rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            else:
                rotated_frame = frame

            # Apply the selected filter to the rotated frame
            filtered_frame = apply_filter(rotated_frame)

            # Convert the filtered frame to PIL Image
            frame_image = PIL.Image.fromarray(filtered_frame.astype(np.uint8))

            # Create PhotoImage from the PIL Image
            image = PIL.ImageTk.PhotoImage(frame_image)

            # Update the video label with the rotated and filtered frame
            video_label.config(image=image)
            video_label.image = image  # Update the reference to the PhotoImage object
        else:
            print("No frame available.")
    else:
        print("Video file not selected.")






# Update the button visibility
update_button_visibility()

# Call the play_video function initially to start playing the video
play_video()



# Create a frame for the square buttons
square_frame = tk.Frame(options_frame, bg="white")
square_frame.pack(pady=10)

# Create the Play Again button
play_again_button = tk.Button(square_frame, text="Play Again", command=restart_video, bg="black", fg="white")
play_again_button.grid(row=0, column=1, padx=25, pady=23)

# Create the Open Video button
open_button = tk.Button(square_frame, text="Open Video", command=open_video, bg="black", fg="white")
open_button.grid(row=0, column=0, pady=23)

# Create button for original audio
original_audio_button = tk.Button(square_frame, text="Original Audio", bg="black", fg="white", command=add_original_audio)
original_audio_button.grid(row=1, column=0, padx=5, pady=5)

# Create button for adding music
add_music_button = tk.Button(square_frame, text="Add Music", command=add_music, bg="black", fg="white")
add_music_button.grid(row=1, column=1, padx=5, pady=5)





# Create a frame for the undo, redo, and rotate buttons
button_frame = tk.Frame(options_frame ,  bg="white")
button_frame.pack(pady=10)

# Create undo button
undo_button = tk.Button(button_frame, text="Undo", command=undo_filter, bg="#FF9800", fg="white", padx=10, pady=5)
undo_button.pack(side="left", padx=5)

# Create redo button
redo_button = tk.Button(button_frame, text="Redo", command=redo_filter, bg="#FF9800", fg="white", padx=10, pady=5)
redo_button.pack(side="left", padx=5)

# Create rotate button
rotate_button = tk.Button(button_frame, text="Rotate", command=rotate_video, bg="#4CAF50", fg="white", padx=10, pady=5)
rotate_button.pack(side="left", padx=5)

# Create a frame for the filter buttons
filter_frame = tk.Frame(options_frame, bg="white")
filter_frame.pack(pady=10)

# Configure uniform size for the filter buttons
filter_frame.columnconfigure(0, weight=1)
filter_frame.columnconfigure(1, weight=1)
filter_frame.rowconfigure(0, weight=1)
filter_frame.rowconfigure(1, weight=1)

# Create grayscale filter button
grayscale_button = tk.Button(filter_frame, text="Grayscale Filter", command=lambda: filter_stack.append(apply_grayscale_filter),
                             bg="#2196F3", fg="white", padx=10, pady=5)
grayscale_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Create Sepia filter button
sepia_button = tk.Button(filter_frame, text="Sepia Filter", command=lambda: filter_stack.append(apply_sepia_filter),
                         bg="#E91E63", fg="white", padx=10, pady=5)
sepia_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

# Create Blur filter button
blur_button = tk.Button(filter_frame, text="Blur Filter", command=lambda: filter_stack.append(apply_blur_filter),
                        bg="#9C27B0", fg="white", padx=10, pady=5)
blur_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# Create Canny Edge Detection filter button
canny_button = tk.Button(filter_frame, text="Canny Edge Filter", command=lambda: filter_stack.append(apply_canny_edge_filter),
                         bg="#607D8B", fg="white", padx=10, pady=5)
canny_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")



# Create a label and dropdown menu for the speed selection
speed_label = tk.Label(options_frame, text="Speed:", font=("Helvetica", 12, "bold"), fg="#333333" , bg = "white")
speed_label.pack(pady=10)

speed_var = tk.StringVar()
speed_var.set("Normal")  # Set the initial speed to "Normal"

speed_dropdown = tk.OptionMenu(options_frame, speed_var, "Slow", "Normal", "Fast")
speed_dropdown.config(font=("Helvetica", 12), bg="white", fg="#555555", activebackground="#e0e0e0", highlightthickness=0)
speed_dropdown.pack(pady=5)





# Run the application
root.mainloop()
