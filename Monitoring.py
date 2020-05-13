import tkinter as tk
from tkinter import filedialog, Text
import os

import socket, threading


def test(text):
    print(text)


def ping():
  print('merijn werkt heer heeeeeeel hard aan en gaaaaat niet met laurence de heledag werken maar ook aan zijn code')

def TCP_connect(ip, port, online, offline, delay=5):
    TCPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsocket.settimeout(delay)
    TCP_Result = TCPsocket.connect_ex((ip, port))
    if TCP_Result == 0:
        online.append(port)
    else:
        offline.append(port)
    TCPsocket.close()


def scan(addressen, port_start=135, port_end=None, delay=5):
    if port_end is None:
        port_end = port_start + 1
    elif port_end is not None:
        port_end = port_end + 1

    for ip in addressen:
        threads = []
        online = []
        offline = []
        for port in range(port_start, port_end):
            t = threading.Thread(target=TCP_connect, args=(ip, port, online, offline, delay))
            threads.append(t)
        for i in range(len(threads)):
            threads[i].start()
        for i in range(len(threads)):
            threads[i].join()

        online.sort()
        offline.sort()




        S = tk.Scrollbar(root)
        T = tk.Text(root, height=20, width=19)
        S.pack(side=tk.RIGHT, fill=tk.Y)
        T.pack(side=tk.LEFT, fill=tk.Y)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        T.insert(tk.END,"Online ports:")
        T.insert(tk.END,online)


        S = tk.Scrollbar(root)
        T = tk.Text(root, height=20, width=19)
        S.pack(side=tk.RIGHT, fill=tk.Y)
        T.pack(side=tk.LEFT, fill=tk.Y)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        T.insert(tk.END,"Offline ports:")
        T.insert(tk.END,offline)



root = tk.Tk()
root.geometry("400x240")
#canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
#canvas.pack()

#frame = tk.Frame(root, bg="White")
#frame.place(relwidth=0.8,relheight=0.8,relx=0.1, rely=0.1)

Start = tk.Button(root, text="Start", padx=10, pady=5, fg="White", bg="#263D42")
Start.pack()

ping()
scan(['192.168.1.20'], port_start=1, port_end=400)
root.mainloop()
