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
        self.clipboard = []
        self.pencil_coords = []

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
            ("Import", self.import_image),
            ("Save", self.save_canvas),
            ("Load", self.load_canvas),
        ]
        for text, command in tools:
            btn = tk.Button(toolbar, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Add Zoom buttons
        zoom_label = tk.Label(toolbar, text="Zoom:")
        zoom_label.pack(side=tk.LEFT, padx=2, pady=2)
        zoom_in_btn = tk.Button(toolbar, text="+", command=self.zoom_in)
        zoom_in_btn.pack(side=tk.LEFT, padx=2, pady=2)
        zoom_out_btn = tk.Button(toolbar, text="-", command=self.zoom_out)
        zoom_out_btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Bind events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def select_tool(self, tool):
        self.current_tool = tool
        # Reset cursor when changing tools
        if tool == "pencil":
            self.canvas.config(cursor="pencil")  # Custom pencil cursor
        elif tool == "eraser":
            self.canvas.config(cursor="crosshair")  # Box-like eraser cursor
        else:
            self.canvas.config(cursor="arrow")  # Default arrow for other tools

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
            self.canvas.postscript(file=file_path + ".ps")
            img = Image.open(file_path + ".ps")
            img.save(file_path)

    def load_canvas(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
        if file_path:
            img = Image.open(file_path)
            self.image = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)

    def zoom_in(self):
        self.canvas.scale("all", 0, 0, 1.2, 1.2)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom_out(self):
        self.canvas.scale("all", 0, 0, 0.8, 0.8)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_click(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.current_tool == "text":
            self.add_text(event.x, event.y)
        elif self.current_tool == "pencil":
            self.pencil_coords = [event.x, event.y]

    def on_drag(self, event):
        if self.current_tool:
            if self.current_tool == "line" and self.start_x and self.start_y:
                self.canvas.delete(self.current_item)
                self.current_item = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill="black")
            elif self.current_tool == "rectangle" and self.start_x and self.start_y:
                self.canvas.delete(self.current_item)
                self.current_item = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="black")
            elif self.current_tool == "ellipse" and self.start_x and self.start_y:
                self.canvas.delete(self.current_item)
                self.current_item = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline="black")
            elif self.current_tool == "pencil":
                self.pencil_coords += [event.x, event.y]
                self.canvas.create_line(self.pencil_coords[-4:], fill="black", smooth=True)
            elif self.current_tool == "eraser":
                size = 10  # Eraser size
                x1, y1 = event.x - size, event.y - size
                x2, y2 = event.x + size, event.y + size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")

    def on_release(self, event):
        if self.current_tool in ["pencil", "eraser"]:
            self.pencil_coords = []  # Reset pencil/eraser coordinates
        else:
            self.current_item = None
            self.start_x, self.start_y = None, None

    def add_text(self, x, y):
        # Open a dialog box to enter the text
        text = simpledialog.askstring("Insert Text", "Enter the text:")
        if text:
            self.canvas.create_text(x, y, text=text, fill="black", font=("Arial", 16))

# Main function
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicsEditor(root)
    root.mainloop()
