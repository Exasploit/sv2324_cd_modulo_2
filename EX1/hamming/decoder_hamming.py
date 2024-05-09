

# in_sequence: string of bits to encode
def decoder_hamming(in_sequence):
    # Calculate the number of parity bits
    m = 0
    while 2 ** m < len(in_sequence) + m + 1:
        m += 1

    # Create the parity check matrix
    parity_check_matrix = [[int(bin(i)[2:].zfill(m)[j]) for j in range(m)] for i in range(1, 2 ** m) if bin(i).count('1') % 2 == 1]

    # Create the generator matrix
    generator_matrix = [[int(bin(i)[2:].zfill(m)[j]) for j in range(m)] for i in range(1, 2 ** m) if bin(i).count('1') % 2 == 0]

    # Create the syndrome table
    syndrome_table = {}
    for i in range(2 ** m):
        syndrome_table[''.join(str(int(a) % 2) for a in np.dot(parity_check_matrix, [int(a) for a in bin(i)[2:].zfill(m)]))] = i

    # Group the sequence into codewords
    codewords = [in_sequence[i:i + m] for i in range(0, len(in_sequence), m)]

    # Decode the sequence
    out_sequence = ''
    for codeword in codewords:
        syndrome = ''.join(str(int(a) % 2) for a in np.dot(parity_check_matrix, [int(a) for a in codeword]))
        if syndrome == '0' * len(syndrome):
            out_sequence += codeword[:-m]
        else:
            error_position = syndrome_table[syndrome]
            out_sequence += ''.join(str(int(a) % 2) for a in np.dot(generator_matrix, [int(a) for a in codeword]))[:-m]

    return out_sequence
