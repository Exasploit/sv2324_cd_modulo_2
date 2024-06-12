import random
from EX2.burst_channel import burst_channel


def test_average_real_burst_length():
    averages = {3: 0, 5: 0, 10: 0, 20: 0}
    for burst_length in [3, 5, 10, 20]:
        for i in range(1, 10000):
            length = 40
            binary_sequence = ''.join(random.choice('01') for _ in range(length))
            result = burst_channel(binary_sequence, burst_length)

            start_index = -1
            end_index = -1
            for i in range(0, len(binary_sequence)):
                if binary_sequence[i] != result[i] and start_index == -1:
                    start_index = i
                elif start_index != -1 and binary_sequence[i] != result[i]:
                    end_index = i

            burst_real_length = end_index - start_index + 1
            averages[burst_length] += burst_real_length
        print(f"Entry burst is {burst_length} and average real burst was {averages[burst_length]/10000}")


def test_burst_channel():
    length = 40
    binary_sequence = ''.join(random.choice('01') for _ in range(length))
    print("Start sequence : " + binary_sequence)

    for burst_length in [3, 5, 10, 20]:
        result = burst_channel(binary_sequence, burst_length)

        start_index = -1
        end_index = -1
        for i in range(0, len(binary_sequence)):
            if binary_sequence[i] != result[i] and start_index == -1:
                start_index = i
            elif start_index != -1 and binary_sequence[i] != result[i]:
                end_index = i

        burst_real_length = end_index - start_index + 1
        print(f"Entry burst is {burst_length} and real burst was {burst_real_length}: " + result)


test_burst_channel()
print("Averages")
test_average_real_burst_length()
