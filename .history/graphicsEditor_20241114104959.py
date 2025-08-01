import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from PIL import Image, ImageDraw

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint Application")
        
        # Canvas setup
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Initialize drawing settings
        self.current_tool = "pencil"
        self.color = "black"
        self.eraser_on = False
        self.line_width = 2
        
        # Track drawing coordinates
        self.last_x, self.last_y = None, None
        
        # Create toolbar
        self.create_toolbar()
        
        # Bind canvas events
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_draw)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Image for saving purposes
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

    def create_toolbar(self):
        # Toolbar Frame
        toolbar = tk.Frame(self.root, bg="lightgrey")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Pencil tool button
        pencil_btn = tk.Button(toolbar, text="Pencil", command=self.use_pencil)
        pencil_btn.pack(side=tk.LEFT)

        # Line tool button
        line_btn = tk.Button(toolbar, text="Line", command=self.use_line)
        line_btn.pack(side=tk.LEFT)

        # Rectangle tool button
        rect_btn = tk.Button(toolbar, text="Rectangle", command=self.use_rectangle)
        rect_btn.pack(side=tk.LEFT)

        # Circle tool button
        circle_btn = tk.Button(toolbar, text="Circle", command=self.use_circle)
        circle_btn.pack(side=tk.LEFT)

        # Color chooser button
        color_btn = tk.Button(toolbar, text="Color", command=self.choose_color)
        color_btn.pack(side=tk.LEFT)

        # Eraser button
        eraser_btn = tk.Button(toolbar, text="Eraser", command=self.use_eraser)
        eraser_btn.pack(side=tk.LEFT)

        # Line width slider
        self.width_slider = tk.Scale(toolbar, from_=1, to=10, orient=tk.HORIZONTAL)
        self.width_slider.set(self.line_width)
        self.width_slider.pack(side=tk.LEFT)

        # Save button
        save_btn = tk.Button(toolbar, text="Save", command=self.save_image)
        save_btn.pack(side=tk.LEFT)

    def use_pencil(self):
        self.current_tool = "pencil"
        self.eraser_on = False

    def use_line(self):
        self.current_tool = "line"
        self.eraser_on = False

    def use_rectangle(self):
        self.current_tool = "rectangle"
        self.eraser_on = False

    def use_circle(self):
        self.current_tool = "circle"
        self.eraser_on = False

    def use_eraser(self):
        self.current_tool = "pencil"
        self.eraser_on = True

    def choose_color(self):
        color = askcolor()[1]
        if color:
            self.color = color

    def on_button_press(self, event):
        # Save the starting coordinates for drawing
        self.last_x, self.last_y = event.x, event.y

    def on_draw(self, event):
        if self.eraser_on:
            fill_color = "white"
            width = self.width_slider.get()
        else:
            fill_color = self.color
            width = self.width_slider.get()

        if self.current_tool == "pencil":
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    fill=fill_color, width=width, capstyle=tk.ROUND, smooth=True)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=fill_color, width=width)
            self.last_x, self.last_y = event.x, event.y

    def on_button_release(self, event):
        if self.current_tool == "line":
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    fill=self.color, width=self.width_slider.get())
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.color, width=self.width_slider.get())
        elif self.current_tool == "rectangle":
            self.canvas.create_rectangle(self.last_x, self.last_y, event.x, event.y,
                                         outline=self.color, width=self.width_slider.get())
            self.draw.rectangle([self.last_x, self.last_y, event.x, event.y], outline=self.color, width=self.width_slider.get())
        elif self.current_tool == "circle":
            self.canvas.create_oval(self.last_x, self.last_y, event.x, event.y,
                                    outline=self.color, width=self.width_slider.get())
            self.draw.ellipse([self.last_x, self.last_y, event.x, event.y], outline=self.color, width=self.width_slider.get())

        # Reset coordinates after releasing the mouse
        self.last_x, self.last_y = None, None

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.image.save(file_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
