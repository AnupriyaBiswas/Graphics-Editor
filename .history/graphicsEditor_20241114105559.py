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

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint Application with Object Selection")
        
        # Canvas setup
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Initialize drawing settings
        self.current_tool = "pencil"
        self.color = "black"
        self.line_width = 2
        self.eraser_on = False
        self.shapes = []
        self.selected_shape = None
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Track drawing coordinates
        self.start_x, self.start_y = None, None
        self.last_x, self.last_y = None, None

        # Create toolbar
        self.create_toolbar()
        
        # Bind canvas events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bg="lightgrey")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        pencil_btn = tk.Button(toolbar, text="Pencil", command=self.use_pencil)
        pencil_btn.pack(side=tk.LEFT)

        line_btn = tk.Button(toolbar, text="Line", command=self.use_line)
        line_btn.pack(side=tk.LEFT)

        rect_btn = tk.Button(toolbar, text="Rectangle", command=self.use_rectangle)
        rect_btn.pack(side=tk.LEFT)

        oval_btn = tk.Button(toolbar, text="Oval", command=self.use_oval)
        oval_btn.pack(side=tk.LEFT)

        color_btn = tk.Button(toolbar, text="Color", command=self.choose_color)
        color_btn.pack(side=tk.LEFT)

        delete_btn = tk.Button(toolbar, text="Delete", command=self.delete_shape)
        delete_btn.pack(side=tk.LEFT)

        self.width_slider = tk.Scale(toolbar, from_=1, to=10, orient=tk.HORIZONTAL)
        self.width_slider.set(self.line_width)
        self.width_slider.pack(side=tk.LEFT)

    def use_pencil(self):
        self.current_tool = "pencil"
        self.eraser_on = False

    def use_line(self):
        self.current_tool = "line"
        self.eraser_on = False

    def use_rectangle(self):
        self.current_tool = "rectangle"
        self.eraser_on = False

    def use_oval(self):
        self.current_tool = "oval"
        self.eraser_on = False

    def choose_color(self):
        color = askcolor()[1]
        if color:
            self.color = color

    def on_canvas_click(self, event):
        self.last_x, self.last_y = event.x, event.y
        shape_id = self.canvas.find_closest(event.x, event.y)
        if shape_id:
            self.select_shape(shape_id[0])
        else:
            self.start_x, self.start_y = event.x, event.y
            self.selected_shape = None

    def on_drag(self, event):
        if self.eraser_on:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    fill="white", width=self.width_slider.get(), capstyle=tk.ROUND, smooth=True)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill="white", width=self.width_slider.get())
            self.last_x, self.last_y = event.x, event.y
        elif self.current_tool == "pencil":
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    fill=self.color, width=self.width_slider.get(), capstyle=tk.ROUND, smooth=True)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.color, width=self.width_slider.get())
            self.last_x, self.last_y = event.x, event.y
        elif self.start_x and self.start_y:
            if self.selected_shape:
                self.selected_shape.delete()
            if self.current_tool == "rectangle":
                shape_id = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y,
                                                        outline=self.color, width=self.width_slider.get())
            elif self.current_tool == "oval":
                shape_id = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y,
                                                   outline=self.color, width=self.width_slider.get())
            elif self.current_tool == "line":
                shape_id = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                                   fill=self.color, width=self.width_slider.get())
            self.selected_shape = Shape(self.canvas, shape_id, self.current_tool)

    def on_release(self, event):
        if self.start_x and self.start_y and self.selected_shape:
            self.shapes.append(self.selected_shape)
        self.start_x, self.start_y = None, None
        self.last_x, self.last_y = None, None

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

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
