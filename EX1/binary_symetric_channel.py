import random


# EX 6, a
# Function to simulate a binary symmetric channel that receives a binary sequence as string and a probability p of BER
def binary_symmetric_channel(binary_sequence, p):
    result = ""
    for bit in binary_sequence:
        # For each bit in the binary sequence, generate a random number between 0 and 1 and compare it with the BER
        if random.random() < p:
            result += '0' if bit == '1' else '1'
        # If the random number is greater than the BER, the bit is transmitted without errors
        else:
            result += bit
    return result
