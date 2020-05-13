import tkinter as tk
from tkinter import filedialog, Text
import os

root = tk.Tk()
canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
canvas.pack()
root.mainloop()

def test(text):
    print(text)

#zet je naam er even bij in de list en push dan de file Danku!

list = ['marc', 'kek', 'merijn', 'Lisa']

for words in list:
    test(words)
