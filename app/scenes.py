import tkinter as tk
from tkinter import filedialog, colorchooser
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from collections import deque

from .imageFilters import blur_image, grayscale_image, brightness_image, horizontal_derivative
from .imageCursor import Cursor

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Viewer App")
        self.geometry("1200x800")
        self.current_image = None
        self.image_history = deque(maxlen=10)
        self.paint_mode = False
        self.color = (0, 0, 0)
        self.image_scale = 1

        self.create_gui_elements()

        paint_cursor = Cursor(self, self.image_label)


    def create_gui_elements(self):
        """
        Create the GUI elements for the application.
        """
        top_frame = tk.Frame(self, bg='lightgray')
        top_frame.pack(side=tk.TOP, fill=tk.X)

        self.load_image_button = tk.Button(top_frame, text="Load Image", command=self.open_image)
        self.load_image_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.blur_image_button = tk.Button(top_frame, text="Blur Image", command=self.blur_image)
        self.blur_image_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.blur_scale = tk.Scale(top_frame, from_=0, to=10, orient=tk.HORIZONTAL)
        self.blur_scale.pack(side=tk.LEFT, padx=5, pady=5)

        self.grayscale_image_button = tk.Button(top_frame, text="Grayscale Image", command=self.grayscale_image)
        self.grayscale_image_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.brightness_scale_button = tk.Button(top_frame, text="Brightness", command=self.brightness_image)
        self.brightness_scale_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.brightness_scale = tk.Scale(top_frame, from_=0, to=20, orient=tk.HORIZONTAL)
        self.brightness_scale.set(10)
        self.brightness_scale.pack(side=tk.LEFT, padx=5, pady=5)

        self.derivative_image_button = tk.Button(top_frame, text="Derivative", command=self.derivative_image)
        self.derivative_image_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.cursor_button = tk.Button(top_frame, text="Paint", command=self.paint_image)
        self.cursor_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.color_picker = tk.Button(top_frame, text="Color", command=self.change_color)
        self.color_picker.pack(side=tk.LEFT, padx=5, pady=5)

        self.opacity_scale = tk.Scale(top_frame, from_=100, to=0, orient=tk.VERTICAL)
        self.opacity_scale.set(100)
        self.opacity_scale.pack(side=tk.LEFT, padx=5, pady=5)
        self.opacity_label = tk.Label(top_frame, text="Opacity")
        self.opacity_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.revert_image_button = tk.Button(top_frame, text="Revert", command=self.revert_image)
        self.revert_image_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.image_label = tk.Label(self)
        self.image_label.pack(side=tk.LEFT, padx=5, pady=5)

    def resize_image(self, image):
        """
        Resize the given image to fit within the window dimensions.

        Args:
            image (PIL.Image.Image): The image to resize.

        Returns:
            PIL.Image.Image: The resized image.
        """
        width, height = image.size

        window_width = int(self.winfo_width() * 0.8)
        window_height = int(self.winfo_height() * 0.8)

        height_ratio = window_height / height
        width_ratio = window_width / width

        scale_factor = min(height_ratio, width_ratio)

        self.image_scale = scale_factor

        resized_width = int(width * scale_factor)
        resized_height = int(height * scale_factor)

        resized_image = image.resize((resized_width, resized_height))

        return resized_image

    def refresh_image(self, image):
        """
        Refresh the displayed image with the given image.
        """
        self.image_history.append(image)
        resized_image = self.resize_image(image)
        tk_image = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image
        self.current_image = image

    def blur_image(self):
        """
        Apply a blur effect to the current image.
        """
        new_image = blur_image(self.current_image, self.blur_scale.get())
        self.refresh_image(new_image)

    def brightness_image(self):
        """
        Adjust the brightness of the current image.
        """
        new_image = brightness_image(self.current_image, self.brightness_scale.get())
        self.refresh_image(new_image)

    def grayscale_image(self):
        """
        Convert the current image to grayscale.
        """
        new_image = grayscale_image(self.current_image)
        self.refresh_image(new_image)

    def revert_image(self):
        """
        Revert to the previous image in the history.
        """
        if len(self.image_history) > 1:
            self.image_history.pop()
            self.refresh_image(self.image_history.pop())

    def open_image(self):
        """
        Open a file dialog to select an image file and display it.
        """
        file_path = filedialog.askopenfilename()
        image = Image.open(file_path)
        self.current_image = image.convert("RGB")
        self.refresh_image(self.current_image)

    def derivative_image(self):
        """
        Apply a horizontal derivative to the current image.
        """
        new_image = horizontal_derivative(self.current_image)
        self.refresh_image(new_image)

    def paint_image(self):
        """
        Enable painting on the current image.
        """
        if self.paint_mode:
            self.paint_mode = False
            self.cursor_button.config(text="Paint")

        else:
            self.paint_mode = True
            self.cursor_button.config(text="Stop Painting")

    def change_color(self):
        """
        Change the color of the paint cursor.
        """
        self.color = colorchooser.askcolor(title="Choose color")

