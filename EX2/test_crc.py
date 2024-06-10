import random
from EX2.cyclic_redundancy_check import cyclic_redundancy_check
from EX2.burst_channel import burst_channel


def test_src():
    k_bits = 1024  # Number of bits in block
    burst_length = 100  # Length of burst (Change values to test different scenarios)
    generator = '1011'  # CRC
    data = "1001011" * (k_bits // 7)  # Data to be transmitted
    print("Data: " + data)
    print("Generator: " + generator)

    burst_data = burst_channel(data, burst_length)  # Apply burst channel
    src = cyclic_redundancy_check(burst_data, generator)  # Apply CRC
    print("Remainder: " + src)
    print(len(generator))
    if src == '0' * (len(generator) - 1):
        print("No errors detected!")
    else:
        print("Errors detected!")


test_src()
