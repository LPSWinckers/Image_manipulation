from PIL import Image
import numpy as np

class Cursor:
    def __init__(self, parent ,image_label, Active=False):
        self.parent = parent
        self.Active = Active
        
        self.color = (0, 0, 0)

        self.image_label = image_label
        self.image_label.bind("<Button-1>", self.on_click)

    def Switch_Active(self):
        if self.Active:
            self.image_label.unbind("<Button-1>")
            self.Active = False
        else:
            self.image_label.bind("<Button-1>", self.on_click)
            self.Active = True

    def on_click(self, event):

        self.paint(event)
        self.image_label.bind("<B1-Motion>", self.paint)
        self.image_label.bind("<ButtonRelease-1>", self.reset)

    def paint(self, event):
        x, y = self.calcute_pixel(event)
        image_array = np.array(self.parent.current_image)
        image_array[y, x] = []
        self.parent.refresh_image(Image.fromarray(image_array))

    def get_color(self):
        return self.color

    def calcute_pixel(self, event):
        x = event.x
        y = event.y

        x = int(x / self.parent.image_scale)
        y = int(y / self.parent.image_scale)

        return x, y