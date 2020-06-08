import socketserver
import csv
import os


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        output = str(self.data, 'utf-8')
        output2 = output.split(',')  # split de string om er een array van te maken
        print(output2)
        CSVTOP1 = ['computer', 'ram', 'cpu']  # Maak een top row voor als een nieuwe file aangemaakt moet worden

        def CSVTHING(Filename, CSVtop=None, CSVdata=None):
            if os.path.exists('./' + Filename):  # Test of de file er al is of niet
                with open(Filename, 'a+', newline='') as F:  # zo ja schrijft de nieuwe row erbij
                    writer = csv.writer(F)
                    writer.writerow(CSVdata)
            else:
                with open(Filename, 'w', newline='') as F:  # zo niet schrijft eerst de top row en daarna de data pas
                    rowlist = [CSVtop, CSVdata]
                    writer = csv.writer(F)
                    writer.writerows(rowlist)

        CSVTHING('test.csv', CSVtop=CSVTOP1, CSVdata=output2)  # draaid de functie


HOST, PORT = "localhost", 9998
server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
server.serve_forever()
