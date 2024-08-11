import socket, sys
import logging as log
from config import udp, settings

# Set log level
if settings.DEBUG:
    log.basicConfig(stream=sys.stderr, level=log.DEBUG)
else:
    log.basicConfig(stream=sys.stderr, level=log.INFO)

def call(shared_data, lock):

    call_message = "Hello"
    locked = lock.acquire()
    try:
        if locked:
            ip = shared_data['ip']
    finally:
            lock.release()

    # Create socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as message:
        log.error("Unable to create socket. " + str(message))
    
    # Send message via UDP packet
    try:
        sock.sendto(call_message.encode(), (ip, udp.GT7_PORT_TX if settings.TEST is False else udp.GT7_PORT_RX))
    except socket.error as message:
        log.error("Unable to send message to " + ip \
                        + " at port " + str(udp.GT7_PORT_TX)\
                                + ". " + str(message))
