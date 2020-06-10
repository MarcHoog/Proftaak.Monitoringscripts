import socketserver
import os
import pymssql

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        output = str(self.data, 'utf-8')
        output2 = output.split(',')  # split de string om er een array van te maken
        hostname = output2[0]
        cpu = output2[1]
        ram = output2[2]
        conn = pymssql.connect(server='145.220.75.101', user='sa', password='P@ssw0rd', database='monitoring')
        cursor = conn.cursor()
        querie1 = f"INSERT INTO Performance(Datum,hostname, CPU, RAM) VALUES (GETDATE(),'{hostname}', '{cpu}', '{ram}');"
        cursor.execute(querie1)
        conn.commit()


        print(hostname + cpu + ram)
HOST, PORT = "localhost", 9998
server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
server.serve_forever()