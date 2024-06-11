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
        sum &= 0xffffffff  # Ensure sum stays within 32 bits
        count += 2
    if max_count & 1:
        sum += data[max_count - 1]
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    result = ~sum & 0xffff
    result = (result >> 8) | ((result & 0xff) << 8)  # Swap byte order
    return result


def check_errors(data_bytes, received_checksum):
    calculated_checksum = calculate_ip_checksum(data_bytes)
    return calculated_checksum == received_checksum

def induce_isolated_errors(data, ber):
    error_mask = 0
    for i in range(32):
        if random.random() < ber:
            error_mask |= (1 << i)
    return data ^ error_mask

def induce_burst_errors(data, burst_length):
    start_bit = random.randint(0, 32 - burst_length)
    error_mask = 0
    for i in range(start_bit, start_bit + burst_length):
        error_mask |= (1 << i)
    return data ^ error_mask

def induce_errors(data, ber, probability_burst, probability_isolated, burst_length):
    if random.random() < probability_burst:
        return induce_burst_errors(data, burst_length)
    elif random.random() < probability_isolated:
        return induce_isolated_errors(data, ber)
    return data


def visualize_errors(original_data, corrupted_data):
    original_bits = format(original_data, '032b')
    corrupted_bits = format(corrupted_data, '032b')
    error_visualization = []
    consecutive_errors = 0
    burst_error = False
    isolated_error = False

    for o_bit, c_bit in zip(original_bits, corrupted_bits):
        if o_bit != c_bit:
            error_visualization.append('x')
            consecutive_errors += 1
        else:
            if consecutive_errors == 1:
                isolated_error = True
            elif consecutive_errors > 1:
                burst_error = True
            consecutive_errors = 0
            error_visualization.append('0')

    # Final check in case the errors are at the very end
    if consecutive_errors == 1:
        isolated_error = True
    elif consecutive_errors > 1:
        burst_error = True

    error_type = "No error"
    if burst_error and isolated_error:
        error_type = "Burst + Isolated"
    elif burst_error:
        error_type = "Burst"
    elif isolated_error:
        error_type = "Isolated"

    return ''.join(error_visualization), error_type


def generate_next_prime():
    # Generator for prime numbers starting from 2
    def is_prime(num):
        if num <= 1:
            return False
        if num % 2 == 0:
            return num == 2
        for i in range(3, int(num ** 0.5) + 1, 2):
            if num % i == 0:
                return False
        return True

    num = 2
    while True:
        if is_prime(num):
            yield num
        num += 1


# Parameters for error induction
ber = 0.01  # Bit Error Rate
probability_burst = 0.5  # Probability of inducing burst errors
probability_isolated = 0.5  # Probability of inducing isolated errors
burst_length = 3  # The necessary length of contiguous errors to be considered a burst

ser = serial.Serial('COM10', 9600)

prime_generator = generate_next_prime()

if ser.isOpen():
    print("Serial port is open")

    # Start reading data
    while True:
        line = ser.readline().decode('utf-8').strip()
        if "," in line:
            data_part, checksum_part = line.split(',')
            data = int(data_part)
            received_checksum = int(checksum_part)
            data_bytes = struct.pack('>L', data)
            original_data = next(prime_generator)

            # Induce errors in the data after receiving the correct prime number
            data_with_errors = induce_errors(original_data, ber, probability_burst, probability_isolated, burst_length)
            
            if check_errors(data_bytes, received_checksum):
                error_status = "Error not detected"
                error_visualization = "00000000000000000000000000000000"  # No errors
                error_type = "No error"
            else:
                error_status = "Error detected"
                error_visualization, error_type = visualize_errors(original_data, data_with_errors)

            print(f"Data: {data:<10} | Original Data: {original_data:<6}| {error_status:<16} | Error: {error_visualization:<32} | Type: {error_type}")

else:
    print("Serial port is not open")