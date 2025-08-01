from tkinter import *
root = Tk()
root.title("Graphics Editor App")
root.geometry("1100x600")

frame1 = Frame(root, height=100, width = 1100, bg="red")
frame1.grid(row = 0, column = 0)
root.resizable(False, False)
root.mainloop()