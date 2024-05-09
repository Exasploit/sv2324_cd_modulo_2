

# in_sequence: string of bits to encode
# n: number of repetitions for each bit
def encoder_repetition(in_sequence, n):
    out_sequence = ''
    for bit in in_sequence:
        out_sequence += bit * n
    return out_sequence
