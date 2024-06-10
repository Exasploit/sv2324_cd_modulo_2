def decoder_hamming(encoded_sequence):
    # Defining the parity check matrix H for Hamming (7,4) code
    H = [
        [0, 1, 1],
        [1, 1, 0],
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

    # Defining the error patterns for the syndrome
    error_patterns = {
        (0, 0, 0): None, (0, 0, 1): 6, (0, 1, 0): 5,
        (1, 0, 0): 4, (1, 1, 1): 3, (1, 0, 1): 2,
        (1, 1, 0): 1, (0, 1, 1): 0
    }

    decoded_sequence = ''
    for i in range(0, len(encoded_sequence), 7):
        # Extracting the codeword
        codeword = list(map(int, encoded_sequence[i:i + 7]))
        syndrome = [0, 0, 0]
        for j in range(3):
            for k in range(7):
                syndrome[j] += codeword[k] * H[k][j]
            syndrome[j] %= 2

        # Detecting and correcting the error if any was introduced
        error = error_patterns[tuple(syndrome)]
        if error is not None:
            codeword[error] = 1 - codeword[error]
        decoded_sequence += ''.join(map(str, codeword[:4]))

    return decoded_sequence


def test_decoder():
    encoded = '1011001'  # corresponds to data bits '1011'
    assert decoder_hamming(encoded) == '1011', "Test Failed: No error decoding failed"
    # Introduce a single error in the second bit
    encoded_error = '1111001'
    assert decoder_hamming(encoded_error) == '1011', "Test Failed: Single bit error decoding failed"
    print("All decoder tests passed!")


test_decoder()