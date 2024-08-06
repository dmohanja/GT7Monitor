# Packet breakdown referenced from:
# https://github.com/snipem/go-gt7-telemetry/blob/main/lib/gt7data.go
packet = {
    # [type (format character), start address, end address (+1)]
    # c: char
    # i: int32
    # I: uint32
    # h: int16
    # H: uint16
    # f: float (32b)
    # d: double (64b)
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
    'mps': ['f',0x4C,0x50], # m/s, x3.6 for km/h
    'boost': ['f',0x50,0x54],
    'oil_pres': ['f',0x54,0x58],
    'water_temp': ['f',0x58,0x5C],
    'oil_temp': ['f',0x5C,0x60],
    'tyre_temp_fl': ['f',0x60,0x64],
    'tyre_temp_fr': ['f',0x64,0x68],
    'tyre_temp_rl': ['f',0x68,0x6C],
    'tyre_temp_rr': ['f',0x6C,0x70],
    'packet_id': ['i',0x70,0x74],
    'lap_count': ['H',0x74,0x76],
    'lap_total': ['H',0x76,0x78],
    'best_lap': ['I',0x78,0x7C],
    'last_lap': ['I',0x7C,0x80],
    'lap_time': ['I',0x80,0x84],
    'position': ['H',0x84,0x86],
    'total_positions': ['H',0x86,0x88],
    'rpm_redline': ['H',0x88,0x8A],
    'rpm_limiter': ['H',0x8A,0x8C],
    'top_speed': ['H',0x8C,0x8E],
    'flags': ['H',0x8E,0x90],
            # flags:
            #   b0 : Racing
            #   b1 : Paused 
            #   b2 : Loading
            #   b3 : InGear
            #   b4 : Turbo
            #   b5 : RevLimiter
            #   b6 : Handbrake
            #   b7 : Lights
            #   b8 : LowBeam
            #   b9 : HighBeam
            #   b10: ASM
            #   b11: TCS
    'gear': ['c',0x90,0x91], # lower nibble
    'suggested_gear': ['c',0x90,0x91], #  upper nibble
    'throttle': ['f',0x91,0x92], # /2.55
    'brake': ['f',0x92,0x93], # /2.55
    'tyre_speed_fl': ['f',0xA4,0xA8],
    'tyre_speed_fr': ['f',0xA8,0xAC],
    'tyre_speed_rl': ['f',0xAC,0xB0],
    'tyre_speed_rr': ['f',0xB0,0xB4],
    'tyre_diameter_fl': ['f',0xB4,0xB8],
    'tyre_diameter_fr': ['f',0xB8,0xBC],
    'tyre_diameter_rl': ['f',0xBC,0xC0],
    'tyre_diameter_rr': ['f',0xC0,0xC4],
    'suspension_fl': ['f',0xC4,0xC8],
    'suspension_fr': ['f',0xC8,0xCC],
    'suspension_rl': ['f',0xCC,0xD0],
    'suspension_rr': ['f',0xD0,0xD4],
    'clutch': ['f',0xF4,0xF8],
    'clutch_engaged': ['f',0xF4,0xFC],
    'rpm_after_clutch': ['f',0xFC,0x100],
    'gear_ratio_1': ['f',0x104,0x108],
    'gear_ratio_2': ['f',0x108,0x10C],
    'gear_ratio_3': ['f',0x10C,0x110],
    'gear_ratio_4': ['f',0x110,0x114],
    'gear_ratio_5': ['f',0x114,0x118],
    'gear_ratio_6': ['f',0x118,0x11C],
    'gear_ratio_7': ['f',0x11C,0x120],
    'gear_ratio_8': ['f',0x120,0x124],
    'car_id': ['I',0x124,0x128],

}

tel_data = {
    'rpm':0.0,
    'rpm_redline':0,
    'rpm_limiter':0,
    'speed':0.0,
    'fuel_lvl':0.0,
    'fuel_cap':0.0,
    'gear':0,
    'suggested_gear':0,
}
