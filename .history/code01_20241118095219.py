import tkinter as tk
from tkinter import filedialog, colorchooser
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
            ("Import", self.import_image),
            ("Save", self.save_canvas),
            ("Load", self.load_canvas),
            ("Zoom", self.zoom_canvas),
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

    def select_line_tool(self):
        self.select_tool("line")

    def select_rectangle_tool(self):
        self.select_tool("rectangle")

    def select_ellipse_tool(self):
        self.select_tool("ellipse")

    def select_text_tool(self):
        self.select_tool("text")

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

    def zoom_canvas(self):
        self.canvas.scale("all", 0, 0, 1.2, 1.2)

    def on_click(self, event):
        self.start_x, self.start_y = event.x, event.y

    def on_drag(self, event):
        if self.current_tool and self.start_x and self.start_y:
            self.canvas.delete(self.current_item)
            if self.current_tool == "line":
                self.current_item = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill="black")
            elif self.current_tool == "rectangle":
                self.current_item = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="black")
            elif self.current_tool == "ellipse":
                self.current_item = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline="black")

    def on_release(self, event):
        self.current_item = None
        self.start_x, self.start_y = None, None

# Main function
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicsEditor(root)
    root.mainloop()
