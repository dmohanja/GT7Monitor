# Decoding method referenced from:
# https://github.com/lmirel/mfc/blob/master/clients/gt7racedata.py

from pure_salsa20 import salsa20_xor
from config import settings

KEY = b"Simulator Interface Packet GT7 ver 0.0"
MAGIC = 0x47375330

def decrypt (data):
    
    if settings.TEST:
        return data

    oiv = data[0x40:0x44]
    iv1 = int.from_bytes(oiv, byteorder='little')
    iv2 = iv1 ^ 0xDEADBEAF

    IV = bytearray()
    IV.extend(iv2.to_bytes(4, 'little'))
    IV.extend(iv1.to_bytes(4, 'little'))

    decrypted = salsa20_xor(KEY[0:32], bytes(IV), data)

    y = int.from_bytes(decrypted[0:4], byteorder='little')
    if y != MAGIC:
        return bytearray(b'')
    else:
        return decrypted