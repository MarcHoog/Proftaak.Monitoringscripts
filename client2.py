import socket
import sys
import time
import psutil as psutil
import pymssql


global ip
global poort


def send_data():
    global cpu
    global hostname
    global ram
    global ip
    for i in range(10):
        CPU = psutil.cpu_times_percent(interval=0.1, percpu=False)
        cpu = (CPU.user + CPU.system + CPU.idle)
    ram = psutil.virtual_memory().percent

    hostname = socket.gethostname()
    print(cpu)
    print(ram)
    print(hostname)

    ip_address = socket.gethostbyname(hostname + ".local")
    ip = 'localhost'


def TCP_connect(ip, port, delay=1):
    TCPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsocket.settimeout(delay)
    TCP_Result = TCPsocket.connect_ex((ip, port))
    if TCP_Result == 0:
        TCPsocket.close()
        result = f'TRUE'
        return result
    else:
        TCPsocket.close()
        result = f'FALSE'
        return result


conn = pymssql.connect(server='145.220.75.101', user='sa', password='P@ssw0rd', database='monitoring')
cursor = conn.cursor()


def poort1():
    global poort
    poort = 9998
    global poort_status
    poort_status = TCP_connect(ip=ip, port=poort)
    check_db()
    if database_waarde == 1:
        Insert_Poort()
        print("test")
    if database_waarde == poort:
        update_Poort()
        print("geen sfeer")


def poort2():
    global poort
    poort = 9999
    global poort_status
    poort_status = TCP_connect(ip=ip, port=poort)
    check_db()
    if database_waarde == 1:
        Insert_Poort()
        print("goedemiddag")
    if database_waarde == poort:
        update_Poort()
        print("totale escalatie")


def Insert_Performance():
    querie1 = f"INSERT INTO Performance(Datum,hostname, CPU, RAM) VALUES (GETDATE(),'{hostname}', '{cpu}', '{ram}');"
    cursor.execute(querie1)
    conn.commit()
    print('sfeer')


def Insert_Poort():
    querie1 = f"INSERT INTO Poorten(Datum,hostname, poort, staat) VALUES (GETDATE(),'{hostname}', '{poort}', '{poort_status}');"
    cursor.execute(querie1)
    conn.commit()


def update_Poort():
    querie1 = f"UPDATE Poorten SET Staat ='{poort_status}', datum = GETDATE() where poort ={poort};"
    cursor.execute(querie1)
    conn.commit()


def check_db():
    querie = F"Select Poort from poorten where poort = {poort}"
    cursor.execute(querie)
    result = cursor.fetchone()
    global database_waarde

    if result is None:
        database_waarde=+1
    else:
        database_waarde = result[0]


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
    Insert_Performance()
    poort1()
    poort2()


while True:
    run_timer(10)
