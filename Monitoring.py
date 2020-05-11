import socket, threading


def test(text):
    print(text)


def ping():
    print('merijn werkt heer heeeeeeel hard aan en gaaaaat niet met laurence de heledag werken maar ook aan zijn code')


# Van boven naar beneden
# Er word een TCP socket aan gemaakt die packetjes kan sturen
# Als die socket binnen set time geen antwoord krijgt stopt ie met proberen
# Probeer connectie te maken met het IP/Port
# Als het resultaat ja is aka '0'
# word de port aan een lijst van alle online porten toegevoegd
# is het resultaat iets anders we geven er niet echt heel veel om wat anders
# Word de port aan een lijst van alle offline porten toegevoegd
def TCP_connect(ip, port, online, offline, delay=5):
    TCPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsocket.settimeout(delay)
    TCP_Result = TCPsocket.connect_ex((ip, port))
    if TCP_Result == 0:
        online.append(port)
    else:
        offline.append(port)
    TCPsocket.close()


# van boven naar beneden
# als port end niet is ingevuld is het niks en word er alleen gebruik gemaakt van port start
# omdat we de range van twee porten noemen moeten we nog steeds zeggen de port start + 1
# port 135 tot en met 136 = port 135
# port 135 tot en met 135 = ERROR
# na dat dat is gedaan word er voor elk appart ip address, meerdere threads aangemaakt voor elke port die hij moet scannen
# De ip's worden 1 voor 1 gedaan omdat het anders een beetje erg messie word
# Na dat de computer 1 ip heeft gedaan displayed hij dit mooi en leegt hij alle arrays
# we zouden later kunnen doen dat hij deze voordat hij ze leegt in een filestopt die wij later kunnen gebruiken
# voor het dashboard
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

        print(f'Ports from ip addres {ip}')
        print('Online ports:')
        for port in online:
            print(port)
        print('Offline ports:')
        for port in offline:
            print(port)


ping()
scan(['192.168.1.20'], port_start=50, port_end=200)
