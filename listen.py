import socket, sys, struct
import logging as log
from config import udp, settings
from crypto import decrypt, packet
import call

UDP_IP = udp.LOCALHOST_IP if settings.TEST is True else udp.PS5_IP

# Set log level
if settings.DEBUG:
    log.basicConfig(stream=sys.stderr, level=log.DEBUG)
else:
    log.basicConfig(stream=sys.stderr, level=log.INFO)

# Create socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as message:
    log.error("Unable to create socket. " + str(message))

# Bind socket to IP/port
try:
    sock.bind(("0.0.0.0",udp.GT7_PORT_RX))
except socket.error as message:
    log.error("Unable to bind socket to " + "0.0.0.0" \
                  + " at port " + str(udp.GT7_PORT_RX)\
                         + ". " + str(message))

# Read to file continuously
log.info("Starting to listen for UDP packets from " + udp.PS5_IP + ":" + str(udp.GT7_PORT_RX))
packet_counter = 0

f = open("recvdat.txt", "w")

rpm_info = packet.packet_position.get("engine_rpm")
fuel_lvl_info = packet.packet_position.get("fuel_lvl")
fuel_cap_info = packet.packet_position.get("fuel_cap")
mps_info = packet.packet_position.get("mps")

call.ping()

while True:
    data, addr = sock.recvfrom(4096)
    packet_counter = packet_counter + 1
    data = decrypt.decrypt(data)
    log.debug("Received packet from " + str(addr) + ", with this data: " + str(data))
    log.info(str(packet_counter))
    f.write(str(bytes(data)))
    f.write("\n\n")
    if packet_counter > 20:
        
        rpm = struct.unpack(rpm_info[0],(data[rpm_info[1]:rpm_info[2]]))[0]
        fuel_lvl = struct.unpack(fuel_lvl_info[0],(data[fuel_lvl_info[1]:fuel_lvl_info[2]]))[0]
        fuel_cap = struct.unpack(fuel_cap_info[0],(data[fuel_cap_info[1]:fuel_cap_info[2]]))[0]
        speed = struct.unpack(mps_info[0],(data[mps_info[1]:mps_info[2]]))[0] * 3.6
        log.info("engine_rpm: " + str(rpm))
        log.info("lap_count: ")
        log.info("lap_total: ")
        log.info("fuel_level: " + str(fuel_lvl))
        log.info("fuel_capacity: " + str(fuel_cap))
        log.info("speed: " + f'{speed:.1f}' + "km/h")
        #call.ping()
        break;

f.close()
    
