def manual_encode_hamming(data_bits):
    # Generator matrix G for Hamming (7,4) code
    G = [
        [1, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 1, 0, 1],
        [0, 0, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 1, 1]
    ]

    # Initialize the encoded bits array with zeros
    encoded_bits = [0] * 7

    # Perform matrix multiplication manually
    for i in range(7):  # There are 7 output bits
        # Calculate each output bit as the dot product of data_bits and the ith column of G
        for j in range(4):  # There are 4 input bits
            encoded_bits[i] += data_bits[j] * G[j][i]
        # Apply modulus 2 to each bit to keep it in binary form
        encoded_bits[i] = encoded_bits[i] % 2

    return encoded_bits


# Example usage of the manual encoding function
data_bits = [1, 0, 1, 1]
manual_encoded = manual_encode_hamming(data_bits)
test = manual_encoded
print(test)  # Output: [1, 0, 1, 0, 0, 1, 1]
# convert to string of bits
convertedToString = ''.join(map(str, test))
