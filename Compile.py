from tkinter import Tk, Button, Label
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk


class CollageMakerApp:
    def __init__(self, root):
        self.root = root
        self.images = []
        self.image_objects = []
        self.collage_image = None

        self.root.title("Collage Maker")

        # Set the background image
        bg_image = Image.open("C:\\Users\MBG Traders\Desktop\\PAI PROJECT\\Picture2.jpg")
        self.background_image = ImageTk.PhotoImage(bg_image)

        # Set the window size equal to the image size
        self.root.geometry(f"{bg_image.width}x{bg_image.height}")

        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas.pack(pady=20)

        self.add_button = tk.Button(self.root, text="Add Image", command=self.add_image, font=("Arial", 12, "bold"), relief="raised", bg="black", fg="white")
        self.add_button.pack(pady=10)

        self.layout_frame = tk.Frame(self.root, bg="white")
        self.layout_frame.pack(pady=10)

        self.layout_label = tk.Label(self.layout_frame, text="Select Layout:", font=("Arial", 12, "bold"), fg="black", bg="white")
        self.layout_label.grid(row=0, column=0)

        self.layout_var = tk.StringVar()
        self.layout_var.set("Grid")

        style = ttk.Style()
        style.configure("TRadiobutton", font=("Arial", 10))

        self.grid_radio = ttk.Radiobutton(self.layout_frame, text="Grid", variable=self.layout_var, value="Grid", style="TRadiobutton")
        self.grid_radio.grid(row=0, column=1, padx=10)

        self.horizontal_radio = ttk.Radiobutton(self.layout_frame, text="Horizontal", variable=self.layout_var, value="Horizontal", style="TRadiobutton")
        self.horizontal_radio.grid(row=0, column=2, padx=10)

        self.create_button = tk.Button(self.root, text="Create Collage", command=self.create_collage, font=("Arial", 12, "bold"), relief="raised", bg="black", fg="white")
        self.create_button.pack(pady=10)

    def add_image(self):
        filetypes = (("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*"))
        filename = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
        if filename:
            image = Image.open(filename)
            image = image.resize((200, 200))
            self.images.append(image)
            photo = ImageTk.PhotoImage(image)
            self.image_objects.append(photo)
        self.display_images()

    def display_images(self):
        self.canvas.delete("all")

        rows = 2
        columns = (len(self.image_objects) + 1) // rows

        x = 10
        y = 10
        spacing = 10

        for i, photo in enumerate(self.image_objects):
            self.canvas.create_image(x, y, image=photo, anchor=tk.NW)
            x += 210 + spacing

            # Move to the next row if the current row is filled
            if (i + 1) % columns == 0:
                x = 10
                y += 210 + spacing

    def create_collage(self):
        if len(self.images) < 2:
            return

        layout = self.layout_var.get()

        if layout == "Grid":
            self.create_grid_collage()
        elif layout == "Horizontal":
            self.create_horizontal_collage()

        if self.collage_image:
            self.collage_image.show()

    def create_grid_collage(self):
        num_images = len(self.images)
        num_rows = int(num_images ** 0.5)
        num_cols = (num_images + num_rows - 1) // num_rows

        collage_width = 400
        collage_height = 400
        image_width = collage_width // num_cols
        image_height = collage_height // num_rows

        collage = Image.new("RGB", (collage_width, collage_height))

        x = 0
        y = 0

        for i, image in enumerate(self.images):
            image = image.resize((image_width, image_height))
            collage.paste(image, (x, y))

            x += image_width
            if x >= collage_width:
                x = 0
                y += image_height

        self.collage_image = collage

    def create_horizontal_collage(self):
        collage_width = 400
        collage_height = 400

        total_width = sum(image.width for image in self.images)
        max_height = max(image.height for image in self.images)

        scale_factor = collage_width / total_width
        scaled_height = int(max_height * scale_factor)

        collage = Image.new("RGB", (collage_width, scaled_height))

        x = 0

        for image in self.images:
            image = image.resize((int(image.width * scale_factor), scaled_height))
            collage.paste(image, (x, 0))

            x += image.width

        self.collage_image = collage


def open_second_page(root):
    root.destroy()

    second_page = Tk()
    second_page.title("Programming For Artificial Intelligence")

    jpeg_image = Image.open(""C:\\Users\MBG Traders\Desktop\\PAI PROJECT\\Picture2.jpg")
    png_image = jpeg_image.convert("RGBA")
    image = ImageTk.PhotoImage(png_image)

    second_page.geometry(f"{image.width()}x{image.height()}")

    img = Label(second_page, image=image)
    img.place(x=0, y=0, relwidth=1, relheight=1)

    button_bg_color = "black"
    button_fg_color = "white"
    button_font = ("Arial", 12, "bold")

    button1 = Button(
        second_page,
        text="VIDEO",
        relief="raised",
        bg=button_bg_color,
        fg=button_fg_color,
        font=button_font,
        width=20,
        height=3,
        activebackground=button_bg_color,
        activeforeground=button_fg_color,
    )
    button1.place(relx=0.2, rely=0.3, anchor="center")

    button2 = Button(
        second_page,
        text="PHOTO",
        relief="raised",
        bg=button_bg_color,
        fg=button_fg_color,
        font=button_font,
        width=20,
        height=3,
        activebackground=button_bg_color,
        activeforeground=button_fg_color,
    )
    button2.place(relx=0.2, rely=0.5, anchor="center")

    button3 = Button(
        second_page,
        text="COLLAGE",
        relief="raised",
        bg=button_bg_color,
        fg=button_fg_color,
        font=button_font,
        width=20,
        height=3,
        activebackground=button_bg_color,
        activeforeground=button_fg_color,
        command=lambda: open_collage_maker(second_page),
    )
    button3.place(relx=0.2, rely=0.7, anchor="center")

    second_page.mainloop()
    
def open_collage_maker(root):
    root.destroy()
    collage_root = Tk()
    collage_root.title("Collage Maker")
    collage_maker = CollageMakerApp(collage_root)
    collage_root.mainloop()


def main_page():
    root = Tk()
    root.title("Programming For Artificial Intelligence")

    jpeg_image = Image.open(""C:\\Users\MBG Traders\Desktop\\PAI PROJECT\\Pict.jpg")
    png_image = jpeg_image.convert("RGBA")
    image = ImageTk.PhotoImage(png_image)

    root.geometry(f"{image.width()}x{image.height()}")

    img_label = Label(root, image=image)
    img_label.place(x=0, y=0, relwidth=1, relheight=1)

    button_bg_color = "black"
    button_fg_color = "white"
    button_font = ("Arial", 12, "bold")

    button1 = Button(
        root,
        text="OPEN",
        relief="raised",
        bg=button_bg_color,
        fg=button_fg_color,
        font=button_font,
        width=20,
        height=3,
        activebackground=button_bg_color,
        activeforeground=button_fg_color,
        command=lambda: open_second_page(root),
    )
    button1.place(relx=0.52, rely=0.75, anchor="center")

    root.mainloop()


    
if __name__ == "__main__":
    main_page()

