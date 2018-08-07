
import socket


def portscan(ip_address, port):
    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    try:
        portconn = s.connect ((ip_address, port))
        print ('port', port, 'is open!')
        portconn.close()
    except:
        pass

def ipgen():
    ip_file = open('ip_file.txt', 'w')
    ip_address = ip_file.readline()
    ip_file.close ()
    print(ip_address)



while True:

    target = input ('введите ip: ')
    ports = (22, 23, 8291, 64231)
    for x in ports:
        if portscan (target, x):
            print ('port', x, 'is open!')
