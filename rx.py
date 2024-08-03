import socket, sys, struct, time
import logging as log
from config import formats, udp, settings
from crypto import decrypt
import tx

UDP_IP = udp.LOCALHOST_IP if settings.TEST is True else udp.PS5_IP

# Set log level
if settings.DEBUG:
    log.basicConfig(stream=sys.stderr, level=log.DEBUG)
else:
    log.basicConfig(stream=sys.stderr, level=log.INFO)

def update_shared_data(data, shared_data, lock):

    if not settings.TEST:
        # Get indexing info from packet dictionary
        rpm_info = formats.packet.get("engine_rpm")
        fuel_lvl_info = formats.packet.get("fuel_lvl")
        fuel_cap_info = formats.packet.get("fuel_cap")
        mps_info = formats.packet.get("mps")

        # Get and interpret data from incoming data
        rpm = struct.unpack(rpm_info[0],(data[rpm_info[1]:rpm_info[2]]))[0]
        fuel_lvl = struct.unpack(fuel_lvl_info[0],(data[fuel_lvl_info[1]:fuel_lvl_info[2]]))[0]
        fuel_cap = struct.unpack(fuel_cap_info[0],(data[fuel_cap_info[1]:fuel_cap_info[2]]))[0]
        speed = struct.unpack(mps_info[0],(data[mps_info[1]:mps_info[2]]))[0] * 3.6

        log.debug("engine_rpm: " + str(rpm))
        log.debug("speed: " + f'{speed:.1f}' + "km/h")

        # Update shared data
        locked = lock.acquire()
        try:
            if locked:
                shared_data['rpm'] = rpm
                shared_data['speed'] = speed
                shared_data['fuel_lvl'] = fuel_lvl
                shared_data['fuel_cap'] = fuel_cap
        finally:
            lock.release()

    else:
        locked = lock.acquire()
        try:
            if locked:
                # TODO: test some time formats here
                if shared_data['rpm'] < 12000.0:
                    shared_data['rpm'] += 100.0
                else:
                    shared_data['rpm'] = 0.0
                if shared_data['speed'] < 500.0:
                    shared_data['speed'] += 0.1
                else:
                    shared_data['speed'] = 0.0
                if shared_data['fuel_lvl'] > 0:
                    shared_data['fuel_lvl'] -= 0.1
                else:
                    shared_data['fuel_lvl'] = 100
                log.debug(shared_data['rpm'])
                log.debug(shared_data['speed'])
                log.debug(shared_data['fuel_lvl'])
        finally:
            lock.release()

def listen(shared_data,lock):
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
        
    # Set timeout
    sock.settimeout(settings.RX_TIMEOUT)
    
    # Read to file continuously
    log.info("Starting to listen for UDP packets from " + udp.PS5_IP + ":" + str(udp.GT7_PORT_RX))

    tx.call()
    packet_count = 0

    while not shared_data['stop']:
        if shared_data['continue']:
            try:
                data, addr = sock.recvfrom(4096)
            except:
                continue
            data = decrypt.decrypt(data)

            if len(data) > 0x40:
                log.debug("Received packet from " + str(addr) + ", with this data: " + str(data))

                # Update everything
                update_shared_data(data, shared_data, lock)

                #time.sleep(1)
                if packet_count > 300:
                    tx.call()
                    packet_count = 0
                    data = {}
                else:
                    packet_count = packet_count + 1
            
            elif settings.TEST:
                time.sleep(0.1)
                tx.call()
                update_shared_data(data, shared_data, lock)
            else:
                log.error("Insufficient data received")
        else:
            time.sleep(0.5)

