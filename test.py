import socket
import logging

hostname='google.com'
port=442

try:
    sock = socket.create_connection((hostname, port), timeout=0.1)

except socket.timeout as err:
    logging.error(err)
    print('errror')

except socket.error as err:
    logging.error(err)
    print ('errror')