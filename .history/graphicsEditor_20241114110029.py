import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from PIL import Image, ImageDraw

class Shape:
    def __init__(self, canvas, shape_id, shape_type):
        self.canvas = canvas
        self.shape_id = shape_id
        self.shape_type = shape_type

    def move(self, dx, dy):
        self.canvas.move(self.shape_id, dx, dy)

    def delete(self):
        self.canvas.delete(self.shape_id)

    def modify(self, color=None, line_width=None, fill=None):
        options = {}
        if color:
            options["outline"] = color
        if line_width:
            options["width"] = line_width
        if fill:
            options["fill"] = fill
        self.canvas.itemconfig(self.shape_id, **options)

class GraphicsEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Graphics Editor")

        # Canvas setup
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Initialize settings
        self.current_tool = "rectangle"
        self.color = "black"
        self.fill = None
        self.line_width = 2
        self.shapes = []
        self.selected_shape = None

        # Track drawing coordinates
        self.start_x, self.start_y = None, None

        # Create toolbar
        self.create_toolbar()

        # Bind canvas events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bg="lightgrey")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        rect_btn = tk.Button(toolbar, text="Rectangle", command=self.use_rectangle)
        rect_btn.pack(side=tk.LEFT)

        oval_btn = tk.Button(toolbar, text="Oval", command=self.use_oval)
        oval_btn.pack(side=tk.LEFT)

        color_btn = tk.Button(toolbar, text="Color", command=self.choose_color)
        color_btn.pack(side=tk.LEFT)

        delete_btn = tk.Button(toolbar, text="Delete", command=self.delete_shape)
        delete_btn.pack(side=tk.LEFT)

        save_btn = tk.Button(toolbar, text="Save", command=self.save_drawing)
        save_btn.pack(side=tk.LEFT)

        load_btn = tk.Button(toolbar, text="Load", command=self.load_drawing)
        load_btn.pack(side=tk.LEFT)

    def use_rectangle(self):
        self.current_tool = "rectangle"

    def use_oval(self):
        self.current_tool = "oval"

    def choose_color(self):
        color = askcolor()[1]
        if color:
            self.color = color

    def on_canvas_click(self, event):
        shape_id = self.canvas.find_closest(event.x, event.y)
        if shape_id:
            self.select_shape(shape_id[0])
        else:
            self.start_x, self.start_y = event.x, event.y
            self.selected_shape = None

    def on_drag(self, event):
        if self.start_x and self.start_y:
            if self.selected_shape:
                self.selected_shape.delete()
            if self.current_tool == "rectangle":
                shape_id = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y,
                                                        outline=self.color, width=self.line_width)
            elif self.current_tool == "oval":
                shape_id = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y,
                                                   outline=self.color, width=self.line_width)
            self.selected_shape = Shape(self.canvas, shape_id, self.current_tool)

    def on_release(self, event):
        if self.start_x and self.start_y and self.selected_shape:
            self.shapes.append(self.selected_shape)
            self.start_x, self.start_y = None, None

    def select_shape(self, shape_id):
        for shape in self.shapes:
            if shape.shape_id == shape_id:
                self.selected_shape = shape
                self.canvas.itemconfig(shape.shape_id, outline="blue")
                return
        self.selected_shape = None

    def delete_shape(self):
        if self.selected_shape:
            self.selected_shape.delete()
            self.shapes.remove(self.selected_shape)
            self.selected_shape = None

    def save_drawing(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.canvas.update()
            self.canvas.postscript(file=file_path + ".ps")
            img = Image.open(file_path + ".ps")
            img.save(file_path)
            img.close()

    def load_drawing(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            img =
