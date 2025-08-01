def on_canvas_click(self, event):
    # Use event.x and event.y directly
    shape_id = self.canvas.find_closest(event.x, event.y)
    if shape_id:
        # Pass event.x and event.y to select_shape
        self.select_shape(event.x, event.y, shape_id[0])
    else:
        self.start_x, self.start_y = event.x, event.y
        self.selected_shape = None

def select_shape(self, x, y, shape_id):
    tolerance = 5
    selected_shape = None
    for shape in self.shapes:
        bbox = self.canvas.bbox(shape.shape_id)
        
        expanded_bbox = (bbox[0] - tolerance, bbox[1] - tolerance, bbox[2] + tolerance, bbox[3] + tolerance)
        
        # Check if the click is within the expanded bounding box
        if x >= expanded_bbox[0] and y >= expanded_bbox[1] and x <= expanded_bbox[2] and y <= expanded_bbox[3]:
            selected_shape = shape
            break

    # Update selection
    if selected_shape:
        if self.selected_shape:
            # Reset outline color for the previously selected shape
            self.canvas.itemconfig(self.selected_shape.shape_id, outline=self.color)
        self.selected_shape = selected_shape
        # Highlight the new selection in blue
        self.canvas.itemconfig(self.selected_shape.shape_id, outline="blue")
    else:
        # Deselect if clicked outside any shape
        if self.selected_shape:
            self.canvas.itemconfig(self.selected_shape.shape_id, outline=self.color)
        self.selected_shape = None
