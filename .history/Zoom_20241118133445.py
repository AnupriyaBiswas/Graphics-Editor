import tkinter as tk
from tkinter import simpledialog, filedialog, colorchooser, font
from tkinter import ttk
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
        if self.current_tool == "text":
            self.add_text(event.x, event.y)

    def on_drag(self, event):
        if self.current_tool == "zoom" and self.start_x and self.start_y:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas.scan_dragto(-dx, -dy, gain=1)
            self.start_x, self.start_y = event.x, event.y
        else:
            if self.current_tool == "line" and self.start_x and self.start_y:
                self.canvas.delete(self.current_item)
                self.current_item = self.canvas.create_line(
                    self.start_x, self.start_y, event.x, event.y, fill=self.current_color
                )
            elif self.current_tool == "rectangle" and self.start_x and self.start_y:
                self.canvas.delete(self.current_item)
                self.current_item = self.canvas.create_rectangle(
                    self.start_x, self.start_y, event.x, event.y, outline=self.current_color
                )
            elif self.current_tool == "ellipse" and self.start_x and self.start_y:
                self.canvas.delete(self.current_item)
                self.current_item = self.canvas.create_oval(
                    self.start_x, self.start_y, event.x, event.y, outline=self.current_color
                )
            elif self.current_tool == "pencil":
                self.pencil_coords += [event.x, event.y]
                self.canvas.create_line(self.pencil_coords[-4:], fill=self.current_color, smooth=True)
            elif self.current_tool == "eraser":
                size = 10
                x1, y1 = event.x - size, event.y - size
                x2, y2 = event.x + size, event.y + size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")

    def on_release(self, event):
        if self.current_tool in ["pencil", "eraser"]:
            self.pencil_coords = []
        else:
            self.current_item = None
            self.start_x, self.start_y = None, None

    def add_text(self, x, y):
        dialog = tk.Toplevel(self.root)
        dialog.title("Insert Text")

        # Text entry
        tk.Label(dialog, text="Enter Text:").grid(row=0, column=0, padx=5, pady=5)
        text_entry = tk.Entry(dialog)
        text_entry.grid(row=0, column=1, padx=5, pady=5)

        # Font style
        tk.Label(dialog, text="Font:").grid(row=1, column=0, padx=5, pady=5)
        font_family = ttk.Combobox(dialog, values=font.families(), state="readonly")
        font_family.set("Arial")
        font_family.grid(row=1, column=1, padx=5, pady=5)

        # Font size
        tk.Label(dialog, text="Size:").grid(row=2, column=0, padx=5, pady=5)
        font_size = ttk.Spinbox(dialog, from_=8, to=72, width=5)
        font_size.set(16)
        font_size.grid(row=2, column=1, padx=5, pady=5)

        # Bold, Italic, Underline
        bold_var = tk.BooleanVar()
        italic_var = tk.BooleanVar()
        underline_var = tk.BooleanVar()
        tk.Checkbutton(dialog, text="Bold", variable=bold_var).grid(row=3, column=0, padx=5, pady=5)
        tk.Checkbutton(dialog, text="Italic", variable=italic_var).grid(row=3, column=1, padx=5, pady=5)
        tk.Checkbutton(dialog, text="Underline", variable=underline_var).grid(row=3, column=2, padx=5, pady=5)

        def apply_text():
            text = text_entry.get()
            if text:
                style = ""
                if bold_var.get():
                    style += "bold"
                if italic_var.get():
                    style += " italic"
                if underline_var.get():
                    style += " underline"
                selected_font = font.Font(
                    family=font_family.get(), size=int(font_size.get()), weight="bold" if "bold" in style else "normal", slant="italic" if "italic" in style else "roman", underline=underline_var.get()
                )
                self.canvas.create_text(x, y, text=text, fill=self.current_color, font=selected_font)
            dialog.destroy()

        # Buttons
        tk.Button(dialog, text="Apply", command=apply_text).grid(row=4, column=0, columnspan=3, pady=10)

# Main function
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicsEditor(root)
    root.mainloop()
