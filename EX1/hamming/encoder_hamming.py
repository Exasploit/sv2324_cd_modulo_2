def encoder_hamming(data_bits):
    if isinstance(data_bits, str):
        data_bits = list(map(int, data_bits))

    # Generator matrix G for Hamming (7,4) code
    G = [
        [1, 0, 0, 0, 1, 1, 0],  # p1 is a function of d1, d2, d4
        [0, 1, 0, 0, 1, 0, 1],  # p2 is a function of d1, d3, d4
        [0, 0, 1, 0, 0, 1, 1],  # p3 is a function of d2, d3, d4
        [0, 0, 0, 1, 1, 1, 1]   # d4, affects all parity bits
    ]

    encoded_bits = [0] * 7
    # Manually multiplying and summing up according to G
    for i in range(7):  # There are 7 output bits (columns of G)
        for j in range(4):  # There are 4 input bits (rows of G)
            encoded_bits[i] += data_bits[j] * G[j][i]
        encoded_bits[i] %= 2  # Modulus 2 to keep it binary

    encoded_string = ''.join(map(str, encoded_bits))
   # print("Debug - Encoded bits:", encoded_string)  # Print encoded string for debugging
    return encoded_string

def test_encoder():
    # Updating the expected result based on the corrected understanding
    assert encoder_hamming([1, 0, 1, 1]) == '1011010', "Test Failed: [1, 0, 1, 1] should encode to '1011010'"
    assert encoder_hamming([0, 0, 0, 0]) == '0000000', "Test Failed: [0, 0, 0, 0] should encode to '0000000'"
    assert encoder_hamming([1, 1, 1, 1]) == '1111111', "Test Failed: [1, 1, 1, 1] should encode to '1111111'"
    print("All encoder tests passed!")


test_encoder()
