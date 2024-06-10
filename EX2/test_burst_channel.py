import random
from EX2.burst_channel import burst_channel


def test_burst_channel():
    length = 40
    binary_sequence = ''.join(random.choice('01') for _ in range(length))
    print("Start sequence : " + binary_sequence)

    for burst_length in [3, 5, 20]:
        result = burst_channel(binary_sequence, burst_length)

        start_index = -1
        end_index = -1
        for i in range(0, len(binary_sequence)):
            if binary_sequence[i] != result[i]:
                start_index = i
                break

        for i in range(-1, -len(binary_sequence) - 1, -1):
            if binary_sequence[i] != result[i]:
                end_index = len(binary_sequence) + i
                break

        burst_real_length = end_index - start_index + 1
        print(f"Entry busrt is {burst_length} and real burst was {burst_real_length}: " + result)


test_burst_channel()
