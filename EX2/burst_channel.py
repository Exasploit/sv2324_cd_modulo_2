import random


def burst_channel(binary_sequence, burst_length):
    # Check if the burst length is greater than the binary sequence
    if burst_length > len(binary_sequence):
        raise ValueError("Burst length is greater than the binary sequence")

    result = ""
    # Generate a random start index for the burst

    result = list(binary_sequence)  # Convert string to list for efficient modification

    # Select burst_length random indices
    burst_indices = random.sample(range(len(binary_sequence)), burst_length)

    # Invert the bits at the selected indices
    for i in burst_indices:
        result[i] = '0' if result[i] == '1' else '1'

    return ''.join(result)  # Convert list back to string


