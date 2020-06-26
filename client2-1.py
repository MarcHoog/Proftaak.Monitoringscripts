import socket
import sys
import time
import psutil as psutil
import pymssql
 
global hostname
global ip
global poort
 
def send_data():
    global cpu
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
        result = f'{port},TRUE'
        return result
    else:
        TCPsocket.close()
        result = f'{port},FALSE'
        return result
 
conn = pymssql.connect(server='145.220.75.101', user='sa', password='P@ssw0rd', database='monitoring')
cursor = conn.cursor()
 
 
 
 
 
 
def poort1(self):
        poort = 9999
        global poort_status
        poort_status = TCP_connect(ip=ip, port=poort)
        check_db()
        if database_waarde == 0:
                Insert_Poort()
        if database_waarde == poort:
            delete_Poort()
            print('regel verwijderd')
            Insert_Poort()
            print('regel ingevoerd')
def poort2(self):
    poort = 9999
    global poort_status
    poort_status = TCP_connect(ip=ip, port=poort)
    check_db()
    if database_waarde == 0:
        Insert_Poort()
    if database_waarde == poort:
        delete_Poort()
        print('regel verwijderd')
        Insert_Poort()
        print('regel ingevoerd')
 
def Insert_Performance():
    querie1 = f"INSERT INTO Performance(Datum,hostname, CPU, RAM) VALUES (GETDATE(),'{hostname}', '{cpu}', '{ram}');"
    cursor.execute(querie1)
    conn.commit()
    print('sfeer')
 
 
def Insert_Poort(self):
    querie1 = f"INSERT INTO Performance(Datum,hostname, poort, staat) VALUES (GETDATE(),'{hostname}', '{poort}', '{poort_status}');"
    cursor.execute(querie1)
    conn.commit()
 
 
def delete_Poort(self):
    querie1 = f"DElete from Poorten where poort = {poort} and Hostname = {hostname};"
    cursor.execute(querie1)
    conn.commit()
 
 
def check_db(self):
    querie = F"Select Poort from poorten where poort = {poort}"
    cursor.execute(querie)
    result = cursor.fetchone()
    global database_waarde
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
 
while True:
    run_timer(10)
