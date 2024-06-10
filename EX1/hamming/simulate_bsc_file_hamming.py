from EX1.binary_symetric_channel import binary_symmetric_channel
from EX1.hamming.decoder_hamming import decoder_hamming
from EX1.hamming.encoder_hamming import encoder_hamming

probability = 0.0000005  # BER
in_file_path = 'test_files/alice29.txt'  # File to be transmitted
out_file_path = 'test_files/alice29_out.txt'  # File to be received


# EX 6, c
# Function to simulate a binary symmetric channel that receives a file as input and a BER and writes the output to a file
def simulate_bsc_file(input_file, output_file, p):
    with open(input_file, 'rb') as file:
        data = file.read()

    in_sequence = ''.join(format(byte, '08b') for byte in data)
    chunks = [in_sequence[i:i + 4] for i in range(0, len(in_sequence), 4)]
    encode_sequence = ''.join(''.join(map(str, encoder_hamming(list(map(int, chunk)))))
                              for chunk in chunks if len(chunk) == 4)

    out_sequence = binary_symmetric_channel(encode_sequence, p)
    decode_chunks = [out_sequence[i:i + 7] for i in range(0, len(out_sequence), 7)]
    decode_sequence = ''.join(decoder_hamming(chunk) for chunk in decode_chunks)


    # Calculate the number of bit errors for BER' and BER
    bit_errors_1 = sum(a != b for a, b in zip(in_sequence, decode_sequence))
    bit_errors_2 = sum(a != b for a, b in zip(encode_sequence, out_sequence))

    # Calculate the total number of bits
    total_bits_1 = len(in_sequence)
    total_bits_2 = len(encode_sequence)

    # Calculate the BER' nad the BER
    BER_1 = bit_errors_1 / total_bits_1
    BER_2 = bit_errors_2 / total_bits_2
    print(f"BER' for the file {in_file_path} is {BER_1}, with p = {p}")
    print(f"BER for the file {in_file_path} is {BER_2}, with p = {p}")

    # Write the output file with bytes
    with open(output_file, 'wb') as output_file:
        output_file.write(bytes(int(decode_sequence[i:i + 8], 2) for i in range(0, len(decode_sequence), 8)))

    # Group the sequences into bytes
    in_bytes = [in_sequence[i:i + 8] for i in range(0, len(in_sequence), 8)]
    out_bytes = [decode_sequence[i:i + 8] for i in range(0, len(decode_sequence), 8)]

    # Calculate the number of errors
    num_errors = sum(a != b for a, b in zip(in_bytes, out_bytes))

    # Calculate the length of the sequence
    length = len(in_bytes)
    return num_errors, length


# Function to write a binary string to a file
def write_bsc_file(file, data):
    with open(file, 'wb') as file:
        file.write(bytes(int(data[i:i + 8], 2) for i in range(0, len(data), 8)))


def main():
    n_errors, length = simulate_bsc_file(in_file_path, out_file_path, probability)
    print(f"Number of errors for the symbols for the file {in_file_path} is {n_errors}, with p = {probability}")
    print(f"Error rate for file {in_file_path} is {n_errors / length} , with p = {probability}")


main()