
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