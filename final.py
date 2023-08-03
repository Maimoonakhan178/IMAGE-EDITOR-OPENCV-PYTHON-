from tkinter import *
from PIL import ImageTk, Image, ImageFilter, ImageDraw
from tkinter import filedialog
from collections import deque
from PIL import ImageEnhance
import numpy as np
from tkinter import messagebox
import cv2
from PIL import ImageFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import Tk, Label
from tkinter import HORIZONTAL
from tkinter import Label, Entry, Button



# Create the main window
mains = Tk()
mains.geometry("1200x800")
mains.attributes("-fullscreen", True)  # Set fullscreen attribute
mains.title("Image Editor")
style = ttk.Style()

# Load the background image
bg_image = ImageTk.PhotoImage(Image.open("C:\\Users\MBG Traders\Desktop\\PAI PROJECT\\Picture2.jpg"))

# Create a label to display the background image
bg_label = Label(mains, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Function to exit fullscreen mode
def exit_fullscreen(event):
    mains.attributes("-fullscreen", False)  # Set fullscreen attribute to False
    mains.geometry("1200x800")  # Restore the original window size

mains.bind("<Escape>", exit_fullscreen)  # Bind the Escape key to exit fullscreen mode

# Create a panel to display the image
panel = Label(mains, bg="black")
panel.grid(row=0, column=0, rowspan=12, padx=50, pady=50)

# Initialize image variables
img = None
output_image = None
drawing_image = Image.new("RGBA", (500, 500))
image_stack = deque()
undo_stack = deque()
drawing = False
last_x, last_y = 0, 0

def display_image(image):
    global disp_image  # Make disp_image a global variable
    disp_image = ImageTk.PhotoImage(image)
    panel.configure(image=disp_image)
    panel.image = disp_image

def open_image():
    global img, output_image, drawing_image
    
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    
    if file_path:
        # Open the selected image file
        img = Image.open(file_path)
        
        # Resize the image to (500, 500)
        img = img.resize((500, 500))
        
        # Create a copy of the original image
        output_image = img.copy()
        
        # Create a new RGBA image for drawing
        drawing_image = Image.new("RGBA", output_image.size)
        
        # Append a copy of the image to the image stack
        image_stack.append(img.copy())
        
        # Combine the output image and drawing image using alpha compositing
        final_image = Image.alpha_composite(output_image.convert("RGBA"), drawing_image)
        
        # Display the final image
        display_image(final_image)
        
        # Clear the undo stack when a new image is opened
        undo_stack.clear()
        
        # Show a message box indicating successful image opening
        messagebox.showinfo("Image Opened", "Image opened successfully!")
        

def adjust_brightness(brightness_pos):
    # Convert brightness_pos to a float value
    brightness_pos = float(brightness_pos)
    
    # Access the global output_image variable
    global output_image
    
    # Check if img exists (an image is selected)
    if img:
        # Convert the image pixels to a NumPy array
        pixels = np.array(img)
        
        # Adjust the brightness by multiplying each pixel with brightness_pos
        brightness_adjusted = pixels * brightness_pos
        
        # Clip the adjusted values to ensure they stay within the range of 0 to 255
        brightness_adjusted = np.clip(brightness_adjusted, 0, 255).astype(np.uint8)
        
        # Create a new image from the adjusted brightness array
        output_image = Image.fromarray(brightness_adjusted)
        
        # Display the adjusted image
        display_image(output_image)
        
        # Append a copy of the output image to the undo stack for history tracking
        undo_stack.append(output_image.copy())
        
        # Update the line plot to reflect the adjusted brightness level
    
        update_line_plot()

        
def adjust_contrast(contrast_pos):
    # Contrast position parameter is converted to a float
    contrast_pos = float(contrast_pos)

    # Access the global variable output_image
    global output_image

    # Check if img exists
    if img:
        # Convert img to a numpy array of pixels
        pixels = np.array(img)

        # Calculate the mean (average) of the pixels
        mean = np.mean(pixels)

        # Adjust the contrast by subtracting the mean, multiplying by contrast_pos, and adding the mean
        contrast_adjusted = (pixels - mean) * contrast_pos + mean

        # Clip the adjusted contrast values to be within the valid intensity range (0-255) and convert to 8-bit unsigned integers
        contrast_adjusted = np.clip(contrast_adjusted, 0, 255).astype(np.uint8)

        # Create an output image from the adjusted contrast array
        output_image = Image.fromarray(contrast_adjusted)

        # Display the output image
        display_image(output_image)

        # Append a copy of the output image to the undo stack
        undo_stack.append(output_image.copy())

        # Update the line plot to reflect the changes
        update_line_plot()


def draw_on_image(event):
    # Global variables used for drawing
    global drawing, last_x, last_y, drawing_image
    
    # If drawing flag is True
    if drawing:
        # Create an ImageDraw object on the drawing_image
        draw = ImageDraw.Draw(drawing_image)
        
        # Draw a line from last_x, last_y to event.x, event.y with red color and width of 5 pixels
        draw.line((last_x, last_y, event.x, event.y), fill="red", width=5)
        
        # Update last_x and last_y to the current event coordinates for the next drawing operation
        last_x, last_y = event.x, event.y
        
        # Combine the output_image and drawing_image using alpha compositing to get the final image
        final_image = Image.alpha_composite(output_image.convert("RGBA"), drawing_image)
        
        # Display the final_image
        display_image(final_image)

def start_drawing(event):
    # Global variables used for drawing
    global drawing, last_x, last_y
    
    # Set the drawing flag to True
    drawing = True
    
    # Set the last_x and last_y coordinates to the current event coordinates
    last_x, last_y = event.x, event.y

def stop_drawing(event):
    # Global variable used for drawing
    global drawing
    
    # Set the drawing flag to False
    drawing = False

def toggle_drawing_mode():
    # Global variable used for drawing
    global drawing
    
    # Toggle the drawing flag
    drawing = not drawing
    
    # Show a message box to indicate whether drawing mode is enabled or disabled
    if drawing:
        messagebox.showinfo("Drawing Mode", "Drawing mode is enabled!")
    else:
        messagebox.showinfo("Drawing Mode", "Drawing mode is disabled!")


        
# Function to adjust sharpness
def adjust_sharpness(sharpness_pos):
    # Convert sharpness_pos to a float
    sharpness_pos = float(sharpness_pos)
    
    # Access the global variable output_image
    global output_image
    
    # Check if img exists
    if img:
        # Apply a blur filter to img and store the result in the blurred variable
        blurred = img.filter(ImageFilter.BLUR)
        
        # Adjust the sharpness by blending img and blurred images using the sharpness_pos parameter
        # The weight of the blurred image is determined by 1 - sharpness_pos
        sharpness_adjusted = Image.blend(img, blurred, 1 - sharpness_pos)
        
        # Update the output_image with the adjusted sharpness
        output_image = sharpness_adjusted
        
        # Display the output_image
        display_image(output_image)
        
        # Append a copy of the output_image to the undo stack
        undo_stack.append(output_image.copy())
        
        # Update the line plot to reflect the changes
    
        update_line_plot()

        
def reduce_noise():
    # Access the global variable output_image
    global output_image
    
    # Check if img exists
    if img:
        # Convert img to a numpy array
        img_array = np.array(img)
        
        # Apply fastNlMeansDenoisingColored function from OpenCV to denoise the img_array
        # The parameters used are: img_array, None, 10, 10, 7, 21
        denoised_array = cv2.fastNlMeansDenoisingColored(img_array, None, 10, 10, 7, 21)
        
        # Create an output_image from the denoised_array
        output_image = Image.fromarray(denoised_array)
        
        # Display the output_image
        display_image(output_image)
        
        # Append a copy of the output_image to the undo stack
        undo_stack.append(output_image.copy())
        
        # Update the line plot to reflect the changes
        update_line_plot()
    else:
        # Call the error_msge() function (not provided in the code) to handle the error
        error_msge()

# Function to apply blur
def apply_blur():
    # Access the global variable output_image
    global output_image
    
    # Check if output_image exists
    if output_image:
        # Apply the blur filter to output_image
        output_image = output_image.filter(ImageFilter.BLUR)
        
        # Display the output_image
        display_image(output_image)
        
        # Append a copy of the output_image to the undo stack
        undo_stack.append(output_image.copy())
    else:
        # Call the error_msge()
        error_msge()

# Function to apply emboss
def apply_emboss():
    # Access the global variable output_image
    global output_image
    
    # Check if output_image exists
    if output_image:
        # Apply the emboss filter to output_image
        output_image = output_image.filter(ImageFilter.EMBOSS)
        
        # Display the output_image
        display_image(output_image)
        
        # Append a copy of the output_image to the undo stack
        undo_stack.append(output_image.copy())
    else:
        # Call the error_msge() 
        error_msge()

# Function to apply edge enhancement
def apply_edge_enhance():
    # Access the global variable output_image
    global output_image
    
    # Check if output_image exists
    if output_image:
        # Apply the edge enhancement filter to output_image
        output_image = output_image.filter(ImageFilter.FIND_EDGES)
        
        # Display the output_image
        display_image(output_image)
        
        # Append a copy of the output_image to the undo stack
        undo_stack.append(output_image.copy())
    else:
        # Call the error_msge() 
        error_msge()

# Function to resize the image
def resize_image():
    global output_image, img
    if img:
        # Store a copy of the original image for undo
        if output_image is None:
            output_image = img.copy()

        # Apply automatic enhancements to the image
        enhanced_image = img.copy()

        # Adjust contrast
        enhancer = ImageEnhance.Contrast(enhanced_image)
        enhanced_image = enhancer.enhance(1.5)  # Increase contrast

        # Adjust brightness
        enhancer = ImageEnhance.Brightness(enhanced_image)
        enhanced_image = enhancer.enhance(1.2)  # Increase brightness

        # Apply image sharpening
        enhanced_image = enhanced_image.filter(ImageFilter.SHARPEN)

        # Apply color saturation enhancement
        enhancer = ImageEnhance.Color(enhanced_image)
        enhanced_image = enhancer.enhance(1.2)  # Increase color saturation

        # Apply image smoothing
        smoothed_image = enhanced_image.filter(ImageFilter.SMOOTH_MORE)

        # Apply artistic effect - Emboss
        embossed_image = smoothed_image.filter(ImageFilter.EMBOSS)

        # Apply artistic effect - Oil Painting
        oil_painting_image = smoothed_image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        oil_painting_image = oil_painting_image.filter(ImageFilter.CONTOUR)

        # Create a composite image with different enhancements
        composite_image = Image.blend(smoothed_image, embossed_image, alpha=0.5)
        composite_image = Image.blend(composite_image, oil_painting_image, alpha=0.3)

        img = composite_image
        display_image(img)
        undo_stack.append(img.copy())
    else:
        error_msge()

# Function to crop the image
def crop_image():
    global output_image
    global image_stack

    # Initialize variables for coordinates of crop area
    starting_x = -1
    starting_y = -1
    ending_x = -1
    ending_y = -1

    # Mouse button event handler
    def mousebutton(event, x, y, flags, param):
        nonlocal starting_x, starting_y, ending_x, ending_y
        # Left button press event
        if event == cv2.EVENT_LBUTTONDOWN:
            starting_x, starting_y = x, y
        # Left button release event
        elif event == cv2.EVENT_LBUTTONUP:
            ending_x, ending_y = x, y
            cv2.destroyAllWindows()

    # Create a named window and set mouse callback function
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', mousebutton)

    # Display the output_image in the window
    cv2.imshow('image', np.array(output_image))

    # Wait for a key press
    cv2.waitKey(0)

    # Check if a crop area is selected
    if starting_x != -1 and starting_y != -1 and ending_x != -1 and ending_y != -1:
        # Determine the coordinates of the crop area
        left = min(starting_x, ending_x)
        right = max(starting_x, ending_x)
        top = min(starting_y, ending_y)
        bottom = max(starting_y, ending_y)

        # Crop the output_image using the determined coordinates
        image = output_image.crop((left, top, right, bottom))
        output_image = image.copy()

        # Append the cropped image to the image_stack
        image_stack.append(output_image)

        # Display the cropped image
        display_image(output_image)

        # Append a copy of the cropped image to the undo_stack
        undo_stack.append(output_image.copy())

        
# Function to rotate the image
def rotate_image():
    global output_image
    if output_image:
        output_image = output_image.rotate(90)
        display_image(output_image)
        undo_stack.append(output_image.copy())
    else:
        error_msge()

# Function to flip the image
def flip_image():
    global output_image
    if output_image:
        output_image = output_image.transpose(Image.FLIP_LEFT_RIGHT)
        display_image(output_image)
        undo_stack.append(output_image.copy())
    else:
        error_msge()
        
# Function to apply vignette effect
def apply_vignette():
    global output_image
    if output_image:
        # Get the width and height of the output_image
        width, height = output_image.size
        
        # Create a black mask image with the same size as the output_image
        mask = Image.new("L", (width, height), 0)
        
        # Create a draw object to draw on the mask
        draw = ImageDraw.Draw(mask)
        
        # Draw an ellipse on the mask to create the vignette effect
        draw.ellipse((0, 0, width, height), fill=255)
        
        # Apply Gaussian blur to the mask to soften the edges
        blurred_mask = mask.filter(ImageFilter.GaussianBlur(radius=width/4))
        
        # Composite the output_image with a black background using the blurred_mask as the alpha channel
        output_image = Image.composite(output_image, Image.new("RGB", (width, height), (0, 0, 0)), mask=blurred_mask)
        
        # Apply additional smoothing to the resulting image
        output_image = output_image.filter(ImageFilter.SMOOTH)
        
        # Display the modified output_image
        display_image(output_image)
        
        # Append a copy of the modified output_image to the undo_stack
        undo_stack.append(output_image.copy())
    else:
        error_msge()


def save_image():
    global output_image
    if output_image is None:
        messagebox.showerror("Error", "No image to save.")
        return

    # Open a file dialog to select a location to save the image
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"),("RGBA", "*.rgba")])
    if file_path:
        try:
            # Save the output image to the selected location
            output_image.save(file_path)
            messagebox.showinfo("Image Saved", "Image saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")


def undo_edit():
    global output_image
    if len(undo_stack) > 1:
        # Pop the last edited image from the undo stack
        redo_image = undo_stack.pop()

        # Append the redo image to the image stack
        image_stack.append(redo_image.copy())

        # Set the output image as the previous image in the undo stack
        output_image = undo_stack[-1].copy()

        # Display the output image
        display_image(output_image)

        # Update the line plot
        update_line_plot()
    else:
        messagebox.showinfo("Message!", "Nothing to Undo")


def redo_edit():
    global output_image
    if len(image_stack) > 1:
        # Pop the last edited image from the image stack
        redo_image = image_stack.pop()

        # Append the redo image to the undo stack
        undo_stack.append(redo_image.copy())

        # Set the output image as the redo image
        output_image = redo_image.copy()

        # Display the output image
        display_image(output_image)

        # Update the line plot
        update_line_plot()
    else:
        messagebox.showinfo("Message!", "Nothing to Redo")


def change_image():
    global img
    global output_image

    # Open a file dialog to select a new image
    img_name = filedialog.askopenfilename(title="Change Image")
    if img_name:
        # Open the selected image file
        img = Image.open(img_name)
        img = img.resize((520, 520))
        output_image = img.copy()

        # Clear the image stack and add the new image
        image_stack.clear()
        image_stack.append(img.copy())

        # Display the new image
        display_image(img)


def adjust_color(color_pos):
    color_pos = float(color_pos)
    global output_image
    if img:
        # Adjust the color saturation of the output image
        enhancer = ImageEnhance.Color(img)
        output_image = enhancer.enhance(color_pos)

        # Display the adjusted image
        display_image(output_image)

        # Append the output image to the undo stack
        undo_stack.append(output_image.copy())

        update_line_plot()


def apply_grayscale():
    global output_image
    if img:
        # Convert the output image to grayscale
        output_image = img.convert("L")

        # Display the grayscale image
        display_image(output_image)

        # Append the output image to the undo stack
        undo_stack.append(output_image.copy())
    else:
        error_msge()


def apply_sepia():
    global output_image
    if output_image:
        output_image = output_image.copy()
        width, height = output_image.size
        pixels = output_image.load()

        # Apply sepia filter to each pixel in the output image
        for i in range(width):
            for j in range(height):
                r, g, b = output_image.getpixel((i, j))
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[i, j] = (tr, tg, tb)

        # Display the sepia image
        display_image(output_image)

        # Append the output image to the undo stack
        undo_stack.append(output_image.copy())
    else:
        error_msge()
        
from PIL import Image, ImageOps

def apply_sepia2():
    global output_image
    if output_image:
        # Apply Sepia filter using PIL ImageOps.colorize() function
        sepia_image = ImageOps.colorize(output_image.convert("L"), "#704214", "#C0A080")

        # Update the output_image with the sepia-filtered image
        output_image = sepia_image

        # Display the updated image
        display_image(output_image)

        # Append a copy of the output image to the undo stack
        undo_stack.append(output_image.copy())

        # Update the line plot to reflect the changes
        update_line_plot()
    else:
        error_msge()
        
        
 # Function to apply resize with the chosen option
def apply_resize():
    global output_image
    if img:
        width = int(width_entry.get())
        height = int(height_entry.get())

        option = resize_option.get()
        # Resize option
        if option == "Resize":
            output_image = img.resize((width, height))
            # Thumbnail option
        elif option == "Thumbnail":
            output_image = img.copy()
            output_image.thumbnail((width, height))
            # Aspect option
        elif option == "Aspect Ratio":
            aspect_ratio = img.width / img.height
            new_width = width
            new_height = int(new_width / aspect_ratio)
            output_image = img.resize((new_width, new_height))
        # Crop option
        elif option == "Crop":
            output_image = img.crop((0, 0, width, height))
        display_image(output_image)
        undo_stack.append(output_image.copy())
    else:
        error_msge()
def error_msge():
    messagebox.showerror("Error", "No image to save.")
    
    

def update_line_plot():
    brightness = brightness_slider.get()
    contrast = contrast_slider.get()
    color = color_slider.get()
    sharpness = sharpness_slider.get()

    labels = ['Bright', 'Cont', 'Clr', 'Sharp']
    values = [brightness, contrast, color, sharpness]

    # Update the bar plot
    ax.clear()
    bars = ax.bar(labels, values)

    # Set custom colors for the bars
    colors = ['black', 'gray', 'lightgray', 'brown']
    for bar, color in zip(bars, colors):
        bar.set_color(color)

    # Calculate the mean and standard deviation for the distribution line
    mean = np.mean(values)
    std = np.std(values)

    # Add a distribution line if the standard deviation is non-zero
    if std != 0:
        x = np.linspace(min(values), max(values), 100)
        y = 1 / (std * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mean) / std) ** 2)
        ax.plot(x, y, color='purple')

    ax.set_xlabel('Adjustments')
    ax.set_ylabel('Values')
    ax.set_title('Slider Effects Visualization')
    ax.grid(True)

    # Specify the artists to include in the legend
    legend_artists = [*bars]  # Include the bars in the legend
    if std != 0:
        legend_artists.append(ax.lines[0])  # Include the distribution line in the legend

    # Add values on the bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, str(height), ha='center', va='bottom')

    canvas.draw()


    
    
# Display the initial image
display_image(Image.new("RGB", (520, 520), "white"))


    
button_width = 10
button_height = 2

frame = ttk.LabelFrame(mains, text=" ", style="My.TLabelframe")
frame.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

filter_frame_slider = ttk.LabelFrame(frame, text="Sliders", style="My.TLabelframe")
filter_frame_slider.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

# Configure the style for the slider
style.configure("My.Horizontal.TScale", background="white")


brightness_slider = Scale(filter_frame_slider, label="Brightness", from_=0, to=2, orient=HORIZONTAL, length=300,
                         resolution=0.1, command=adjust_brightness, bg="black", fg="white",
                         troughcolor="gray")
brightness_slider.set(1)
brightness_slider.grid(row=3, column=2)

contrast_slider = Scale(filter_frame_slider, label="Contrast", from_=0, to=2, orient=HORIZONTAL, length=300,
                       command=adjust_contrast, resolution=0.1, bg="black", fg="white",troughcolor="gray")
contrast_slider.set(1)
contrast_slider.grid(row=4, column=2)

sharpness_slider = Scale(filter_frame_slider, label="Sharpness", from_=0, to=2, orient=HORIZONTAL, length=300,
                         command=adjust_sharpness, resolution=0.1, bg="black", fg="white",
                         troughcolor="gray")
sharpness_slider.set(1)
sharpness_slider.grid(row=5, column=2)

color_slider = Scale(filter_frame_slider, label="Color", from_=0, to=2, orient=HORIZONTAL, length=300,
                     command=adjust_color, resolution=0.1, bg="black", fg="white",
                     troughcolor="gray")
color_slider.set(1)
color_slider.grid(row=6, column=2)

style = ttk.Style()
style.configure("My.TLabelframe", background="white")
style.configure("My.TLabelframe.Label", foreground="black", font=("Times", 9, "bold italic"))

# Create buttons for applying filters and operations
filter_frame = ttk.LabelFrame(frame,  text="Filters", style="My.TLabelframe")
filter_frame.grid(row=1, column=1, padx=1, pady=5, sticky="nsew")

blur_button = Button(filter_frame, text="Blur", command=apply_blur, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
blur_button.grid(row=0, column=0, padx=10, pady=10)

emboss_button = Button(filter_frame, text="Emboss", command=apply_emboss, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
emboss_button.grid(row=0, column=1, padx=10, pady=10)

edge_enhance_button = Button(filter_frame, text="E.Enhance", command=apply_edge_enhance, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
edge_enhance_button.grid(row=1, column=0, padx=10, pady=10)

vignette_button = Button(filter_frame, text="Vignette", command=apply_vignette, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
vignette_button.grid(row=1, column=1, padx=10, pady=10)

grayscale_button = Button(filter_frame, text="Grayscale", command=apply_grayscale, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
grayscale_button.grid(row=2, column=1, padx=10, pady=10)

sepia_button = Button(filter_frame, text="Sepia", command=apply_sepia, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
sepia_button.grid(row=2, column=0, padx=10, pady=10)

brown_button = Button(filter_frame, text="brownie", command=apply_sepia2, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
brown_button.grid(row=0, column=2, padx=10, pady=10)
# Create buttons for image editing operations
operation_frame = ttk.LabelFrame(frame, text="Operations", style="My.TLabelframe")
operation_frame.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

resize_button = Button(operation_frame, text="Auto", command=resize_image, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
resize_button.grid(row=0, column=0, padx=10, pady=10)

crop_button = Button(operation_frame, text="Crop", command=crop_image, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
crop_button.grid(row=0, column=1, padx=10, pady=10)


undo_button = Button(operation_frame, text="Undo", command=undo_edit, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
undo_button.grid(row=1, column=0, padx=10, pady=10)


redo_button = Button(operation_frame, text="Redo", command=redo_edit, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
redo_button.grid(row=1, column=1, padx=10, pady=10)


rotate_button = Button(operation_frame, text="Rotate", command=rotate_image, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
rotate_button.grid(row=2, column=1, padx=10, pady=10)

flip_button = Button(operation_frame, text="Flip", command=flip_image, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
flip_button.grid(row=2, column=0, padx=10, pady=10)


reduce_noise_button = Button(operation_frame, text="Reduce Noise", command=reduce_noise, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
reduce_noise_button.grid(row=0, column=2, pady=10)


# Create a button to save the edited image
save_button = Button(operation_frame, text="Save", command=save_image, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
save_button.grid(row=1, column=2, padx=20, pady=20)
#save_button['font'] = ('Arial', 12, 'bold')

change_image_button = Button(operation_frame, text="Change", command=change_image, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
change_image_button.grid(row=2, column=2,padx=20, pady = 10)
#change_image_button['font'] = ('Arial', 12, 'bold')

style = ttk.Style()
style.configure("My.TLabel", foreground="black", font=("Times", 9, "bold italic"))

# Create buttons for image editing operations
resize_frame = ttk.LabelFrame(mains, text="Resize", style="My.TLabelframe")
resize_frame.grid(row=10, column=1, padx=5, pady=5, sticky="nsew")

# Create resize label
resize_label = ttk.Label(resize_frame, text="Resize", style="My.TLabel")
resize_label.grid(row=1, column=1)

# Create resize option combobox
resize_option = ttk.Combobox(resize_frame, values=["Resize", "Thumbnail", "Aspect Ratio", "Crop"], width=20)
resize_option.current(0)
resize_option.grid(row=1, column=2, pady=10)

# Create width label
width_label = ttk.Label(resize_frame, text="Width", style="My.TLabel")
width_label.grid(row=2, column=1)

# Create width entry
width_entry = ttk.Entry(resize_frame, width=20)
width_entry.grid(row=2, column=2, pady=10)

# Create height label
height_label = ttk.Label(resize_frame, text="Height", style="My.TLabel")
height_label.grid(row=3, column=1)

# Create height entry
height_entry = ttk.Entry(resize_frame, width=20)
height_entry.grid(row=3, column=2, pady=10)


# Create apply_resize_button
apply_resize_button = Button(resize_frame, text="Apply Resize", command=apply_resize, bg="black", fg="white", width=button_width, height=button_height, relief="raised")
apply_resize_button.grid(row=4, column=2, pady=10)

# Bind events to the panel
panel.bind("<B1-Motion>", draw_on_image)
panel.bind("<Button-1>", start_drawing)
panel.bind("<ButtonRelease-1>", stop_drawing)

draw_button = Button(resize_frame, text="Drawing", command=toggle_drawing_mode, bg="black", fg="white", width=button_width, height=button_height)
draw_button.grid(row=4, column=4, pady=10)

# Create a button to open the image
open_button = Button(resize_frame, text="Open", command=open_image, bg="black", fg="white", width=10, height=2)
open_button.grid(row=4, column=6, padx=20, pady=10)

#Graphs
line_plot_frame = Frame(frame, bg="black")
line_plot_frame.grid(row=3, column=2, rowspan=5, padx=20, pady=10)

fig = plt.Figure(figsize=(4, 2))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=line_plot_frame)
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

update_line_plot()


# Start the main loop
mains.mainloop()
