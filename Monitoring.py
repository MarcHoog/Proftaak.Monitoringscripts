import os
from os.path import sep
import socket
import sys
import threading
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Text
from tkinter.ttk import Frame, Button, Label

# Global values:
WIN = sys.platform.startswith("win")


# Netwerk tools:
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

        online.sort(), offline.sort()
        return online, offline


def ping(hostname):
    response = os.system(f"ping -{'n' if WIN else 'c'} 1 {hostname}")
    if response == 0:
        return f'{hostname} is UP'
    else:
        return f'{hostname} is DOWN'


# tkinter Events:
def getTXTinput():
    IPlist = []
    input_IPV4 = txt_IPinput.get(1.0, tk.END + '-1c')
    input_Portstart = txt_portstart.get(1.0, tk.END + '-1c')
    input_Portend = txt_portend.get(1.0, tk.END + '-1c')
    if input_IPV4.replace(' ', '') == '':
        txt_IPinput.delete(1.0, tk.END)
        return
    elif input_Portstart.replace(' ', '') == '':
        txt_portstart.delete(1.0, tk.END)
        return
    else:
        CSV_String = f"{input_IPV4},{input_Portstart},{input_Portend}"
        with open("hosts.txt", "a+") as file_object:
            file_object.seek(0)
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            file_object.write(CSV_String)

    for host in open(f".{sep}hosts.txt", "r").read().splitlines():
        print(host)
        IPlist.append(host)


def run():
    output = []
    for host in open(f".{sep}hosts.txt", "r").read().splitlines():
        x = host.split(',')
        if ping(x[0]) == f'{x[0]} is UP':
            onlineports, offlineports = scan(x[0], int(x[1]), int(x[2]))
            output.append(f'HOST:   {x[0]} is  ONLINE' + '\n' +
                          f'   ONLINE-PORTS: {onlineports}' + '\n' +
                          f'   OFFLINE-PORTS: {offlineports}' + '\n' + '\n')
        else:
            output.append(f'HOST:   {x[0]} is  OFFLINE' + '\n' + '\n')

    txt_OUTPUT.config(state='normal')
    txt_OUTPUT.delete(1.0, tk.END)
    txt_OUTPUT.insert(1.0, output)
    txt_OUTPUT.config(state='disabled')


def FORCERUN():
    textboxes = [txt_OUTPUT, txt_Result]
    for boxes in textboxes:
        boxes.config(state='normal')
        boxes.delete(1.0, tk.END)
        boxes.config(state='disabled')
    run()


# tkinter Gui:
root = tk.Tk()
root.geometry = '700x800'


def task():
    txt_Result.config(state='normal')
    txt_Result.delete(1.0, tk.END)
    txt_Result.insert(1.0, 'Gathering Information')
    txt_Result.config(state='disabled')
    run()
    txt_Result.config(state='normal')
    txt_Result.delete(1.0, tk.END)
    txt_Result.insert(1.0, 'DONE Wait for Estimate 1 minute for new Result')
    txt_Result.config(state='disabled')
    root.after(60000, task)

data = pd.read_excel(r'C:\Users\Teun\Documents\School\Vakken\ICT-Infrastructure\Proftaak\Proftaak.xlsx') #for an earlier version of Excel use 'xls'
df = pd.DataFrame(data, columns = ['Host','Ping time in sec'])

# above frame
frame1 = Frame(relief=tk.RAISED, borderwidth=1)
frame1.pack(fill=tk.X)

lbl_TITLE = Label(frame1, text="PING TEST", width=10)
lbl_TITLE.pack(side=tk.LEFT, padx=5, pady=5)

clearBtn = Button(frame1, text="FORCE", command=FORCERUN)
clearBtn.pack(side=tk.RIGHT, padx=5, pady=5)

pingBtn = Button(frame1, text="ADD", command=getTXTinput)
pingBtn.pack(side=tk.RIGHT)

txt_portend = Text(frame1, height=1, width=5)
txt_portend.pack(side=tk.RIGHT, padx=5)
lbl_portend = Label(frame1, text="P-END")
lbl_portend.pack(side=tk.RIGHT, padx=5, pady=5)

txt_portstart = Text(frame1, height=1, width=5)
txt_portstart.pack(side=tk.RIGHT, padx=5)
lbl_portstart = Label(frame1, text="P-START")
lbl_portstart.pack(side=tk.RIGHT, padx=5, pady=5)

txt_IPinput = tk.Text(frame1, height=1, width=15)
txt_IPinput.pack(side=tk.RIGHT, padx=5)
lbl_IPinput = Label(frame1, text="IPV4")
lbl_IPinput.pack(side=tk.RIGHT, padx=5, pady=5)

# Second frame
frame2 = Frame()
frame2.pack(fill=tk.X)

lbl_Result = tk.Label(frame2, text='Status', width=10)
lbl_Result.pack(side=tk.LEFT, padx=5)
txt_Result = tk.Text(frame2, height=1, state='disabled', width=40)
txt_Result.pack(side=tk.LEFT, padx=20)

# Third frame
frame3 = Frame()
frame3.pack(fill=tk.X)

lbl_Filler1 = tk.Label(frame3, width=10)
lbl_Filler1.pack(side=tk.LEFT, padx=5)
txt_OUTPUT = tk.Text(frame3, height=20, width=80)
txt_OUTPUT.pack(side=tk.LEFT, padx=20, pady=10)

root.after(60000, task)

# Bar chart
figure = plt.Figure(figsize=(6,5), dpi=100)
ax = figure.add_subplot(111)
chart_type = FigureCanvasTkAgg(figure, root)
chart_type.get_tk_widget().pack()
df = df[['Host','Ping time in sec']].groupby('Host').sum()
df.plot(kind='bar', legend=True, ax=ax)
ax.set_title('Ping Summary')

root.mainloop()
