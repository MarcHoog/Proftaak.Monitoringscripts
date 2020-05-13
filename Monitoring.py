import tkinter as tk
from tkinter import filedialog, Text
import os

root = tk.Tk()
canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
canvas.pack()

frame = tk.Frame(root, bg="White")
frame.place(relwidth=0.8,relheight=0.8,relx=0.1, rely=0.1)

Start = tk.Button(root, text="Start", padx=10, pady=5, fg="White", bg="#263D42")
Start.pack()

root.mainloop()


