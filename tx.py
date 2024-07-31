import socket, sys
import logging as log
from config import udp, settings

UDP_IP = udp.LOCALHOST_IP if settings.TEST is True else udp.PS5_IP

# Set log level
if settings.DEBUG:
    log.basicConfig(stream=sys.stderr, level=log.DEBUG)
else:
    log.basicConfig(stream=sys.stderr, level=log.INFO)

def call():
    call = "Hello"

    # Create socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as message:
        log.error("Unable to create socket. " + str(message))
    
    # Send message via UDP packet
    try:
        sock.sendto(call.encode(), (UDP_IP, udp.GT7_PORT_TX if settings.TEST is False else udp.GT7_PORT_RX))
    except socket.error as message:
        log.error("Unable to send message to " + UDP_IP \
                        + " at port " + str(udp.GT7_PORT_TX)\
                                + ". " + str(message))

