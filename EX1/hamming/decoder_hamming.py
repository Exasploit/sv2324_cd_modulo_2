def decoder_hamming(encoded_sequence):
    H = [
        [1, 1, 0, 1, 1, 0, 0],
        [1, 0, 1, 1, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 1]
    ]

    error_patterns = {
        (0, 0, 0): None, (0, 0, 1): 6, (0, 1, 0): 5,
        (0, 1, 1): 4, (1, 0, 0): 3, (1, 0, 1): 2,
        (1, 1, 0): 1, (1, 1, 1): 0
    }

    decoded_sequence = ''
    for i in range(0, len(encoded_sequence), 7):
        codeword = list(map(int, encoded_sequence[i:i+7]))
        syndrome = [0] * 3
        for j in range(3):
            for k in range(7):
                syndrome[j] ^= H[j][k] * codeword[k]
        syndrome_tuple = tuple(syndrome)
        error_position = error_patterns.get(syndrome_tuple)
        if error_position is not None and error_position < 4:
            codeword[error_position] ^= 1
        decoded_sequence += ''.join(str(bit) for bit in codeword[:4])

    return decoded_sequence

def test_decoder():
    encoded = '1011001'  # corresponds to data bits '1011'
    assert decoder_hamming(encoded) == '1011', "Test Failed: No error decoding failed"
    # Introduce a single error in the second bit
    encoded_error = '1111001'
    assert decoder_hamming(encoded_error) == '1011', "Test Failed: Single bit error decoding failed"
    print("All decoder tests passed!")


test_decoder()