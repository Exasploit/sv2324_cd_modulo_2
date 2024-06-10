import random
from EX2.cyclic_redundancy_check import cyclic_redundancy_check
from EX2.burst_channel import burst_channel


def test_src():
    k_bits = 1024  # Number of bits in block
    burst_length = 11  # Length of burst (Change values to test different scenarios)
    generator = '1011'  # CRC
    data = ''.join(random.choice('01') for _ in range(k_bits))  # Generate random data
    print("Data: " + data)
    print("Generator: " + generator)

    new_data = ""
    for i in range(0, len(data), 1024):
        src = cyclic_redundancy_check(data[i:i + 1024], generator)
        new_data += data[i:i + 1024] + src

    burst = burst_channel(new_data, burst_length)

    src_check = cyclic_redundancy_check(burst, generator)
    print("CRC: " + src_check)
    if src_check == '0' * (len(generator) - 1):
        print("No errors")
    else:
        print("Errors")



test_src()
