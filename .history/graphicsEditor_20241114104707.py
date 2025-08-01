import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk

class GraphicObject:
    """Base class for graphic objects."""
    def __init__(self, canvas, x, y, color="black"):
        self.canvas = canvas
        self.color = color
        self.id = None  # Canvas object ID
        self.create(x, y)

    def create(self, x, y):
        pass

    def move(self, dx, dy):
        if self.id:
            self.canvas.move(self.id, dx, dy)

    def delete(self):
        if self.id:
            self.canvas.delete(self.id)

class Circle(GraphicObject):
    def create(self, x, y, radius=50):
        self.id = self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius, outline=self.color, width=2
        )

class Rectangle(GraphicObject):
    def create(self, x, y, width=100, height=50):
        self.id = self.canvas.create_rectangle(
            x - width//2, y - height//2, x + width//2, y + height//2, outline=self.color, width=2
        )

class GraphicsEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Graphics Editor")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.current_tool = None
        self.current_color = "black"
        self.shapes = []
        self.selected_shape = None

        self.create_toolbar()

        # Bindings for interactive actions
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bg="lightgrey")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        circle_btn = tk.Button(toolbar, text="Circle", command=self.select_circle_tool)
        circle_btn.pack(side=tk.LEFT)

        rect_btn = tk.Button(toolbar, text="Rectangle", command=self.select_rectangle_tool)
        rect_btn.pack(side=tk.LEFT)

        color_btn = tk.Button(toolbar, text="Color", command=self.choose_color)
        color_btn.pack(side=tk.LEFT)

        delete_btn = tk.Button(toolbar, text="Delete", command=self.delete_shape)
        delete_btn.pack(side=tk.LEFT)

        save_btn = tk.Button(toolbar, text="Save", command=self.save_canvas)
        save_btn.pack(side=tk.LEFT)

        load_btn = tk.Button(toolbar, text="Load", command=self.load_image)
        load_btn.pack(side=tk.LEFT)

    def select_circle_tool(self):
        self.current_tool = "circle"

    def select_rectangle_tool(self):
        self.current_tool = "rectangle"

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.current_color = color

    def on_canvas_click(self, event):
        if self.current_tool == "circle":
            shape = Circle(self.canvas, event.x, event.y, color=self.current_color)
        elif self.current_tool == "rectangle":
            shape = Rectangle(self.canvas, event.x, event.y, color=self.current_color)
        else:
            # Select shape if clicked on existing one
            self.select_shape(event.x, event.y)
            return

        self.shapes.append(shape)
        self.selected_shape = shape

    def on_drag(self, event):
        if self.selected_shape:
            dx, dy = event.x - self.canvas.coords(self.selected_shape.id)[0], event.y - self.canvas.coords(self.selected_shape.id)[1]
            self.selected_shape.move(dx, dy)

    def select_shape(self, x, y):
        shape_id = self.canvas.find_closest(x, y)
        for shape in self.shapes:
            if shape.id == shape_id[0]:
                self.selected_shape = shape
                break

    def delete_shape(self):
        if self.selected_shape:
            self.selected_shape.delete()
            self.shapes.remove(self.selected_shape)
            self.selected_shape = None

    def save_canvas(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if filename:
            self.canvas.postscript(file=filename + '.eps')
            img = Image.open(filename + '.eps')
            img.save(filename, 'png')

    def load_image(self):
        filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if filename:
            img = Image.open(filename)
            img = img.resize((self.canvas.winfo_width(), self.canvas.winfo_height()), Image.ANTIALIAS)
            self.bg_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicsEditor(root)
    root.mainloop()
