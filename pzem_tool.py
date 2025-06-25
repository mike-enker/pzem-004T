import serial
import struct
import time


def calc_crc(data):
    """Calculate CRC16 (Modbus-RTU)."""
    crc = 0xFFFF
    for a in data:
        crc ^= a
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return struct.pack('<H', crc)


class PZEM004T:
    def __init__(self, port, baudrate=9600, slave_addr=0x01):
        self.slave_addr = slave_addr
        self.serial = serial.Serial(port, baudrate=baudrate, timeout=1)
        time.sleep(1)

    def _send_request(self, function_code, register_addr=0x0000, num_regs=0x0001, payload=None):
        if function_code in [0x03, 0x04]:
            packet = struct.pack('>B B H H', self.slave_addr, function_code, register_addr, num_regs)
        elif function_code == 0x06:
            if payload is None:
                raise ValueError("Missing payload for write operation")
            packet = struct.pack('>B B H H', self.slave_addr, function_code, register_addr, payload)
        elif function_code == 0x42:
            packet = struct.pack('>B B', self.slave_addr, function_code)
        else:
            raise ValueError(f"Unsupported function code: {function_code}")

        packet += calc_crc(packet)
        self.serial.write(packet)
        time.sleep(0.001)
        return self.serial.read(256)

    def read_input_registers(self, start_reg=0x0000, count=10):
        response = self._send_request(0x04, start_reg, count)
        if not response or response[1] & 0x80:
            raise RuntimeError(f"Read failed with error: {response.hex()}")
        return response

    def write_single_register(self, reg_addr, value):
        response = self._send_request(0x06, reg_addr, payload=value)
        if not response or response[1] & 0x80:
            raise RuntimeError(f"Write failed with error: {response.hex()}")
        return response

    def reset_energy(self):
        response = self._send_request(0x42)
        if not response or response[1] & 0x80:
            raise RuntimeError(f"Reset failed with error: {response.hex()}")
        return response

    def close(self):
        self.serial.close()

    def get_measurements(self):
        raw = self.read_input_registers(0x0000, 10)
        if raw[1] != 0x04:
            raise ValueError("Invalid function code in response")
        
        data = raw[3:-2]

        def get16(i):
            return data[i] << 8 | data[i + 1]

        def get32(lo_index, hi_index):
            low = get16(lo_index)
            high = get16(hi_index)
            return (high << 16) | low

        voltage = get16(0) * 0.1
        current = get32(2, 4) * 0.001
        power = get32(6, 8) * 0.1
        energy = get32(10, 12)
        frequency = get16(14) * 0.1
        power_factor = get16(16) * 0.01
        alarm = get16(18)

        return {
            "voltage": round(voltage, 1),
            "current": round(current, 3),
            "power": round(power, 1),
            "energy": energy,
            "frequency": round(frequency, 1),
            "power_factor": round(power_factor, 2),
            "alarm": bool(alarm),
        }

