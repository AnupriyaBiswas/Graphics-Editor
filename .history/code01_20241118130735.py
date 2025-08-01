import tkinter as tk
from tkinter import simpledialog, filedialog, colorchooser
from PIL import Image, ImageTk

# Main application class
class GraphicsEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("GraphyX - Graphics Editor")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Initialize tools and state
        self.current_tool = None
        self.start_x = None
        self.start_y = None
        self.current_item = None
        self.pencil_coords = []
        self.current_color = "black"  # Default color
        self.offset_x = 0  # Offset for panning
        self.offset_y = 0

        self.init_ui()

    def init_ui(self):
        # Toolbar
        toolbar = tk.Frame(self.root, bg="lightgray")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Tools
        tools = [
            ("Line", self.select_line_tool),
            ("Rectangle", self.select_rectangle_tool),
            ("Ellipse", self.select_ellipse_tool),
            ("Text", self.select_text_tool),
            ("Pencil", self.select_pencil_tool),
            ("Eraser", self.select_eraser_tool),
            ("Color", self.choose_color),
            ("Import", self.import_image),
            ("Save", self.save_canvas),
            ("Load", self.load_canvas),
            ("Zoom", self.select_zoom_tool),
        ]
        for text, command in tools:
            btn = tk.Button(toolbar, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Bind events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def select_tool(self, tool):
        self.current_tool = tool
        if tool == "zoom":
            self.canvas.config(cursor="hand2")  # Change cursor to hand
        elif tool in ["pencil", "eraser"]:
            self.canvas.config(cursor="crosshair")  # Crosshair for precision
        else:
            self.canvas.config(cursor="arrow")  # Default cursor

    def select_line_tool(self):
        self.select_tool("line")

    def select_rectangle_tool(self):
        self.select_tool("rectangle")

    def select_ellipse_tool(self):
        self.select_tool("ellipse")

    def select_text_tool(self):
        self.select_tool("text")

    def select_pencil_tool(self):
        self.select_tool("pencil")

    def select_eraser_tool(self):
        self.select_tool("eraser")

    def select_zoom_tool(self):
        self.select_tool("zoom")

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose a color")[1]
        if color:
            self.current_color = color

    def import_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            img = Image.open(file_path)
            self.image = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if file_path:
            self.canvas.update()
            ps_file = file_path + ".ps"
            self.canvas.postscript(file=ps_file, colormode='color')
            img = Image.open(ps_file)
            img.save(file_path)

    def load_canvas(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.canvas.delete("all")
            img = Image.open(file_path)
            self.image = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)

    def on_click(self, event):
        self.start_x, self.start_y = event.x, event.y

    def on_drag(self, event):
        if self.current_tool == "zoom" and self.start_x and self.start_y:
            # Calculate the movement delta
            dx = event.x - self.start_x
            dy = event.y - self.start_y

            # Adjust the canvas view
            self.canvas.scan_dragto(-dx, -dy, gain=1)

            # Update start positions
            self.start_x, self.start_y = event.x, event.y

    def on_release(self, event):
        self.start_x, self.start_y = None, None

    def add_text(self, x, y):
        text = simpledialog.askstring("Insert Text", "Enter the text:")
        if text:
            self.canvas.create_text(x, y, text=text, fill=self.current_color, font=("Arial", 16))


# Main function
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicsEditor(root)
    root.mainloop()
