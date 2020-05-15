import tkinter as tk
from tkinter import filedialog, Text
import os
from os.path import sep
import sys
import socket, threading



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
        T.insert(tk.END,"Online ports:")
        P.insert(tk.END,"Offline ports:")
        T.insert(tk.END,online)
        P.insert(tk.END,offline)

WIN = sys.platform.startswith("win")

def ping(hostname):
    response = os.system(f"ping -{'n' if WIN else 'c'} 1 {hostname}")


    if response == 0:

        up.insert(tk.END,hostname +" Up")
        up.pack(side=tk.LEFT, fill=tk.Y)

    else:

        down.pack(side=tk.LEFT, fill=tk.Y)
        up.insert(tk.END,hostname + " Down")






def run():
    for host in open(f".{sep}hosts.txt", "r").read().splitlines():
        print(f"Host gevonden in TXT-file: {host}")
        ping(host)
        print("\n")



root = tk.Tk()
root.geometry("800x400")
root.title("Monitoring FIND3")

def getTextInput():
    result1 = []
    result=textExample.get(1.0, tk.END+"-1c")
    result1.append(result)
    scan(result1, port_start=400, port_end=600)

textExample=tk.Text(root, height= 1)
textExample.pack()
btnRead=tk.Button(root, height=1, width=10, text="Kies IP", command=getTextInput)
btnRead.pack()

S = tk.Scrollbar(root)
T = tk.Text(root, height=20, width=19)
S.pack(side=tk.RIGHT, fill=tk.Y)
T.pack(side=tk.LEFT, fill=tk.Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)

Z = tk.Scrollbar(root)
P = tk.Text(root, height=20, width=19)
Z.pack(side=tk.RIGHT, fill=tk.Y)
P.pack(side=tk.LEFT, fill=tk.Y)
Z.config(command=T.yview)
P.config(yscrollcommand=S.set)

up = tk.Text(root, height=20, width=19)
down = tk.Text(root, height=20, width=19)


def clearTextInput():
  P.delete("1.0","end")
  T.delete("1.0","end")


btnRead=tk.Button(root, height=1, width=10, text="Clear", command=clearTextInput).place(x=0, y=20)
run()
root.mainloop()
