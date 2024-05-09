
# Defining the decoding function for repetition code
def decoder_repetition(data, n):
    decoded_data = ''
    for i in range(0, len(data), n):
        chunk = data[i: i +n]
        if chunk.count('1') > chunk.count('0'):
            decoded_data += '1'  # More 1s than 0s
        else:
            decoded_data += '0'  # More 0s or equal number of 1s and 0s
    return decoded_data

def decoder_efficient_repetition(in_sequence, n):
    # if n is even, the majority of bits is n/2
    # if n is odd, the majority of bits is n//2 + 1
    # skip ahead n bits at a time and count the number of 1s
    out_sequence = ''
    for i in range(0, len(in_sequence), n):
        out_sequence += '1' if in_sequence[i:i + n].count('1') > n // 2 else '0'
    return out_sequence