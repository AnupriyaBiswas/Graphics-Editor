from tkinter import *
root = Tk()
root.title("Graphics Editor App")
root.geometry("1100x600")

frame1 = Frame(root, height=100, width = 1100, bg="red")
frame1.grid(row = 0, column = 0)

frame2 = Frame(root, height=500, width = 1100, bg="red")
frame1.grid(row = 1, column = 0)

canvas = Canvas(frame2, height = 500, width = 100, bg = "white")
canvas.grid(row = 0, column = 0)

def paint():
    canvas.create_oval(100, 100, 120, 120, fill = "black")
root.resizable(False, False)
root.mainloop()