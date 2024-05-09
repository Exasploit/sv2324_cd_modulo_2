import random

from EX1.binary_symetric_channel import binary_symmetric_channel

sequence_lengths = [1024, 10240, 102400, 1024000, 10240000]  # Sequence lengths
probability = 0.1  # BER probability


# EX 6, b
# Function to simulate a binary symmetric channel that receives the length of the sequence and a probability p of BER
def simulate_bsc_sequence(L, p):
    # Generate a random binary sequence of length L as string
    in_sequence = ''.join(random.choice('01') for _ in range(L))
    # Transmit the sequence through the binary symmetric channel
    out_sequence = binary_symmetric_channel(in_sequence, p)
    # Calculate the number of errors
    num_errors = sum(a != b for a, b in zip(in_sequence, out_sequence))
    # Calculate the real BER
    real_ber = num_errors / L
    return real_ber


def main():
    for L in sequence_lengths:
        # Calculate the BER for each sequence length
        ber = simulate_bsc_sequence(L, probability)
        print(f"BER for L = {L} is {ber} with p = {probability}")


main()