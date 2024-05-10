import serial
import struct

def calculate_ip_checksum(data):
    sum = 0
    max_count = len(data)
    count = 0
    while count + 1 < max_count:
        val = (data[count + 1] << 8) + data[count]
        sum += val
        sum &= 0xffffffff  # Ensure sum stays within 32 bits
        count += 2
    if max_count & 1:
        sum += data[max_count - 1]
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    result = ~sum & 0xffff
    result = (result >> 8) | ((result & 0xff) << 8)  # Swap byte order
    return result

ser = serial.Serial('COM8', 9600)

while True:
    line = ser.readline().decode('utf-8').strip()
    if "," in line:
        data_part, checksum_part = line.split(',')
        data = int(data_part)
        received_checksum = int(checksum_part)
        data_bytes = struct.pack('>L', data)  # Confirm little-endian is correct
        calculated_checksum = calculate_ip_checksum(data_bytes)
        print(f"Data: {data}, Packed Bytes: {data_bytes.hex()}, Received Checksum: {received_checksum}, Calculated Checksum: {calculated_checksum}")
        if calculated_checksum == received_checksum:
            print(f"Data received correctly ==> {data}")
        else:
            print(f"Error detected in data ==> {data}")
