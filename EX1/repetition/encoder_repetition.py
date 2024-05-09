

# in_sequence: string of bits to encode
# n: number of repetitions for each bit
def encoder_repetition(in_sequence, n):
    out_sequence = ''
    for bit in in_sequence:
        out_sequence += bit * n
    return out_sequence


def decoder_efficient_repetition(in_sequence, n):
    # if n is even, the majority of bits is n/2
    # if n is odd, the majority of bits is n//2 + 1
    # skip ahead n bits at a time and count the number of 1s
    out_sequence = ''
    for i in range(0, len(in_sequence), n):
        out_sequence += '1' if in_sequence[i:i + n].count('1') > n // 2 else '0'
    return out_sequence