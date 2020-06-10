import socket
import sys
import time
import psutil as psutil

def send_data():
    for i in range(10):
        CPU = psutil.cpu_times_percent(interval=0.1, percpu=False)
        CPU = (CPU.user + CPU.system + CPU.idle)
    RAM = psutil.virtual_memory().percent
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname + ".local")
    ip = 'localhost'
    port1 = 9999
    port2 = 9998

    result1 = TCP_connect(ip=ip, port=port1)
    result2 = TCP_connect(ip=ip, port=port2)
    HOST, PORT = "localhost", 9998
    data = f"{hostname},{CPU},{RAM},{result1},{result2}"

    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")

    print("Sent:     {}".format(data))

def TCP_connect(ip, port, delay=1):
    TCPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsocket.settimeout(delay)
    TCP_Result = TCPsocket.connect_ex((ip, port))
    if TCP_Result == 0:
        TCPsocket.close()
        result = f'{port},TRUE'
        return result
    else:
        TCPsocket.close()
        result = f'{port},FALSE'
        return result

def run_timer(seconds):
    # Automatic countdown mechanism
    for remaining in range(seconds, 0, -1):
        sys.stdout.write("\r")
        minutes = 0
        seconds = remaining
        if remaining > 60:
            minutes = int(seconds / 60)
            seconds = int(seconds % 60)
        else:
            seconds = remaining
        sys.stdout.write("{:2d} seconds remaining until next poll".format(seconds))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\n")
    send_data()

while True:
    run_timer(10)
