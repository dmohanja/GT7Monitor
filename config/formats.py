# Packet breakdown referenced from:
# https://github.com/snipem/go-gt7-telemetry/blob/main/lib/gt7data.go
packet = {
    # [type (format character), start address, end address (+1)]
    'magic': ['i',0x0,0x4],
    'position_x': ['f',0x4,0x8],
    'position_y': ['f',0x8,0xC],
    'position_z': ['f',0xC,0x10],
    'velocity_x': ['f',0x10,0x14],
    'velocity_y': ['f',0x14,0x18],
    'velocity_z': ['f',0x18,0x1C],
    'rotation_pitch': ['f',0x1C,0x20],
    'rotation_yaw': ['f',0x20,0x24],
    'rotation_roll': ['f',0x24,0x28],
    'rel_orientation': ['f',0x28,0x2C],
    'agl_velocity_x': ['f',0x2C,0x30],
    'agl_velocity_y': ['f',0x30,0x34],
    'agl_velocity_z': ['f',0x34,0x38],
    'ride_height': ['f',0x38,0x3C],
    'engine_rpm': ['f',0x3C,0x40],
    'iv': ['f',0x40,0x44],
    'fuel_lvl': ['f',0x44,0x48],
    'fuel_cap': ['f',0x48,0x4C],
    'mps': ['f',0x4C,0x50],
    'boost': ['f',0x50,0x54],
    'oil_pres': ['f',0x54,0x58],
    'water_temp': ['f',0x58,0x5C],
    'oil_temp': ['f',0x5C,0x60],
    'tyre_temp_fl': ['f',0x60,0x64],
    'tyre_temp_fr': ['f',0x64,0x68],
    'tyre_temp_rl': ['f',0x68,0x6C],
    'tyre_temp_rr': ['f',0x6C,0x70],
    'packet_id': ['i',0x70,0x74],
    'lap_count': ['h',0x74,0x76],
    'lap_total': ['h',0x76,0x78],
    'best_lap': ['i',0x78,0x70],
    'last_lap': ['i',0x7C,0x70]
}

tel_data = {
    'rpm':0.0,
    'speed':0.0,
    'fuel_lvl':0.0,
    'fuel_cap':0.0
}

decrypted_sample = {
    'rpm':0.0,
    'mps':0.0,
    'fuel_lvl':0.0,
    'fuel_cap':0.0
}