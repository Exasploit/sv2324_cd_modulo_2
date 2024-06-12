import serial
import struct
import random


def calculate_ip_checksum(data):
    sum = 0
    max_count = len(data)
    count = 0
    while count + 1 < max_count:
        val = (data[count + 1] << 8) + data[count]
        sum += val
        sum &= 0xffffffff  # Ensures the sum remains within 32 bits
        count += 2
    if max_count & 1:
        sum += data[max_count - 1]
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    result = ~sum & 0xffff
    result = (result >> 8) | ((result & 0xff) << 8)  # Swaps the byte order
    return result


def induce_burst_errors(data, burst_length):
    start_bit = random.randint(0, 32 - burst_length)
    error_mask = 0
    for i in range(start_bit, start_bit + burst_length):
        if random.random() < 0.8:  # Allows some bits to remain correct within the burst
            error_mask |= (1 << i)
    return data ^ error_mask


def induce_errors(data, ber, probability_burst, burst_length):
    if random.random() < probability_burst:
        return induce_burst_errors(data, burst_length)
    else:
        error_mask = 0
        for i in range(32):
            if random.random() < ber:
                error_mask |= (1 << i)
        return data ^ error_mask


def visualize_errors(original_data, corrupted_data):
    original_bits = format(original_data, '032b')
    corrupted_bits = format(corrupted_data, '032b')
    error_visualization = []
    first_error = None
    last_error = None
    error_count = 0

    for index, (o_bit, c_bit) in enumerate(zip(original_bits, corrupted_bits)):
        if o_bit != c_bit:
            if first_error is None:
                first_error = index
            last_error = index
            error_visualization.append('x')
            error_count += 1
        else:
            error_visualization.append('0')

    burst_length_detected = (last_error - first_error + 1) if first_error is not None and last_error is not None else 0
    error_detected = burst_length_detected > 0
    error_type = "No error"

    # Checks if the majority of bits within the range are errors to consider as burst
    if error_detected:
        if error_count == 1:
            error_type = "Isolated error"
        elif error_count > 1:
            if error_count / burst_length_detected > 0.5:  # If more than 50% of the bits are errors
                error_type = "Burst error"
            else:
                error_type = "Isolated errors"

    details = {
        'first_error': first_error,
        'last_error': last_error,
        'burst_length': burst_length_detected,
        'error_count': error_count
    }

    return ''.join(error_visualization), error_type, details


# Induces burst errors after reception
ber = 0.02  # Bit error rate
probability_burst = 0.5  # Probability of inducing burst errors
burst_length = random.randint(2, 15)  # Burst error length can vary from 2 to 10 bits
printDetails = False


def main():
    ser = serial.Serial('COM10', 9600)

    if ser.isOpen():
        print("Serial port is open")

        # Prints the table header
        if printDetails:
            print(f"{'Data':<12} | {'Original Data':<12} | {'Status':<18} | {'Error Visualization':<35} | {'Details'}")
            print("=" * 105)
        else:
            print(f"{'Data':<12} | {'Original Data':<12} | {'Status':<18} | {'Error Visualization':<35}")
            print("=" * 77)

        while True:
            line = ser.readline().decode('utf-8').strip()
            if "," in line:
                data_part, checksum_part = line.split(',')
                data = int(data_part)
                received_checksum = int(checksum_part)
                data_bytes = struct.pack('>L', data)

                corrupted_data = induce_errors(data, ber, probability_burst, burst_length)
                corrupted_data_bytes = struct.pack('>L', corrupted_data)

                # Checks the checksum
                if calculate_ip_checksum(corrupted_data_bytes) == received_checksum:
                    error_status = "No error detected"
                    error_visualization = "00000000000000000000000000000000"  # No errors
                    details = "No Error"
                else:
                    error_visualization, error_status, error_details = visualize_errors(data, corrupted_data)
                    if error_status == "Isolated error":
                        details = f"First Error: {error_details['first_error']} | Last Error: {error_details['last_error']}"
                    elif error_status == "Burst error":
                        details = f"First Error: {error_details['first_error']} | Last Error: {error_details['last_error']} | Burst Length: {error_details['burst_length']}"
                    else:
                        details = f"First Error: {error_details['first_error']} | Last Error: {error_details['last_error']} | Error Count: {error_details['error_count']} | Burst Length: {error_details['burst_length']}"

                if printDetails:
                    print(
                        f"{corrupted_data:<12} | {data:<12} | {error_status:<18} | {error_visualization:<35} | {details}")
                else:
                    print(f"{corrupted_data:<12} | {data:<12} | {error_status:<18} | {error_visualization:<35}")


if __name__ == "__main__":
    main()
