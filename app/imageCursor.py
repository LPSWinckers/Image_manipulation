from PIL import Image
import numpy as np

class Cursor:
    def __init__(self, parent ,image_label, Active=False):
        """
        Args:
            parent (tkinter.Frame): The parent frame.
            image_label (tkinter.Label): The label to display the image.
            Active (bool): Whether the cursor is active.
        """

        self.parent = parent
        self.Active = Active
        
        self.color = [0, 0, 0]
        self.brush_size = 10

        self.image_label = image_label
        self.image_label.bind("<Button-1>", self.on_click)

    def Switch_Active(self):
        """
        switch the active state of the cursor
        """
        if self.Active:
            self.image_label.unbind("<Button-1>")
            self.Active = False
        else:
            self.image_label.bind("<Button-1>", self.on_click)
            self.Active = True

    def on_click(self, event):
        """
        handle the click event

        Args:
            event (tkinter.Event): The event that triggered the function.
        """
        self.paint(event)
        self.image_label.bind("<B1-Motion>", self.paint)

    def paint(self, event):
        """
        paint the image

        Args:
            event (tkinter.Event): The event that triggered the function.
        """
        center_x, center_y = self.calcute_pixel(event)
        image_array = np.array(self.parent.current_image)

        x, y = np.meshgrid(np.arange(image_array.shape[1]), np.arange(image_array.shape[0]))

        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)

        mask = distance <= int(self.brush_size)

        image_array[mask] = self.color 

        self.parent.refresh_image(Image.fromarray(image_array))

    def change_size(self, size):
        """
        change the size of the brush

        args:
            size (int): The size of the brush.
        """
        self.brush_size = size

    def change_opacity(self, opacity):
        """
        change the opacity of the brush

        Args:
            opacity (int): The opacity of the brush.
        """
        self.brush_opacity = opacity

    def calcute_pixel(self, event):
        """
        calculate the pixel

        Args:
            event (tkinter.Event): The event that triggered the function.

        Returns:
            tuple: The pixel coordinates.
        """
        x = event.x
        y = event.y

        x = int(x / self.parent.image_scale)
        y = int(y / self.parent.image_scale)

        return x, y