import tkinter as tk
from tkinter import filedialog, colorchooser
from tkinter import simpledialog
from PIL import Image, ImageTk


class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint App")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Initialize state
        self.current_tool = None
        self.start_x = None
        self.start_y = None
        self.current_color = "black"
        self.eraser_size = 10
        self.text_box_content = tk.StringVar()
        self.zoom_scale = 1.0

        self.init_ui()

    def init_ui(self):
        # Toolbar
        toolbar = tk.Frame(self.root, bg="lightgray")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Tool Buttons
        tool_frame = tk.LabelFrame(toolbar, text="Tools", bg="lightgray")
        tool_frame.pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(tool_frame, text="Pencil", command=self.select_pencil_tool).pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
        tk.Button(tool_frame, text="Eraser", command=self.select_eraser_tool).pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)

        # Size Spinner
        size_frame = tk.LabelFrame(toolbar, text="Size", bg="lightgray")
        size_frame.pack(side=tk.LEFT, padx=5, pady=2)
        self.size_spinner = tk.Spinbox(size_frame, from_=1, to=50, width=5, command=self.update_size)
        self.size_spinner.pack(side=tk.LEFT, padx=2, pady=2)

        # Color Buttons
        color_frame = tk.LabelFrame(toolbar, text="Colors", bg="lightgray")
        color_frame.pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(color_frame, text="Select Color", command=self.choose_color).pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
        colors = ["Red", "Green", "Blue", "Yellow", "Orange", "Purple"]
        for color in colors:
            tk.Button(color_frame, text=color, bg=color.lower(), command=lambda c=color.lower(): self.set_color(c)).pack(
                side=tk.LEFT, padx=2, pady=2
            )

        # File Operations
        file_frame = tk.LabelFrame(toolbar, text="File", bg="lightgray")
        file_frame.pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(file_frame, text="Save", command=self.save_canvas).pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
        tk.Button(file_frame, text="New", command=self.clear_canvas).pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)

        # Text Entry
        text_frame = tk.LabelFrame(toolbar, text="Text", bg="lightgray")
        text_frame.pack(side=tk.RIGHT, padx=5, pady=2)
        tk.Entry(text_frame, textvariable=self.text_box_content).pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
        tk.Button(text_frame, text="Clear", command=self.clear_text_box).pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)

        # Zoom Buttons
        zoom_frame = tk.LabelFrame(toolbar, text="Zoom", bg="lightgray")
        zoom_frame.pack(side=tk.RIGHT, padx=5, pady=2)
        tk.Button(zoom_frame, text="+", command=self.zoom_in).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(zoom_frame, text="-", command=self.zoom_out).pack(side=tk.LEFT, padx=2, pady=2)

        # Bind events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    # Tool Selection
    def select_tool(self, tool):
        self.current_tool = tool
        if tool == "pencil":
            self.canvas.config(cursor="pencil")
        elif tool == "eraser":
            self.canvas.config(cursor="circle")
        else:
            self.canvas.config(cursor="arrow")

    def select_pencil_tool(self):
        self.select_tool("pencil")

    def select_eraser_tool(self):
        self.select_tool("eraser")

    # Color Picker
    def choose_color(self):
        color = colorchooser.askcolor(title="Choose a color")[1]
        if color:
            self.set_color(color)

    def set_color(self, color):
        self.current_color = color

    # Save Canvas
    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if file_path:
            self.canvas.update()
            self.canvas.postscript(file=file_path + ".ps")
            img = Image.open(file_path + ".ps")
            img.save(file_path)

    # Clear Canvas
    def clear_canvas(self):
        self.canvas.delete("all")

    def update_size(self):
        self.eraser_size = int(self.size_spinner.get())

    def clear_text_box(self):
        self.text_box_content.set("")

    # Zoom Functions
    def zoom_in(self):
        self.zoom_scale += 0.1
        self.canvas.scale("all", 0, 0, 1.1, 1.1)

    def zoom_out(self):
        self.zoom_scale -= 0.1
        self.canvas.scale("all", 0, 0, 0.9, 0.9)

    # Mouse Event Handlers
    def on_click(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.current_tool == "pencil":
            self.last_coords = [event.x, event.y]

    def on_drag(self, event):
        if self.current_tool == "pencil":
            self.canvas.create_line(
                self.last_coords[0],
                self.last_coords[1],
                event.x,
                event.y,
                fill=self.current_color,
                width=2,
            )
            self.last_coords = [event.x, event.y]
        elif self.current_tool == "eraser":
            x1, y1 = event.x - self.eraser_size, event.y - self.eraser_size
            x2, y2 = event.x + self.eraser_size, event.y + self.eraser_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")

    def on_release(self, event):
        self.start_x, self.start_y = None, None


if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
