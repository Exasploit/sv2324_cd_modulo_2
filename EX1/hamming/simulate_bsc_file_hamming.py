from EX1.binary_symetric_channel import binary_symmetric_channel
from EX1.repetition.decoder_repetition import decoder_repetition
from EX1.repetition.encoder_repetition import encoder_repetition

probability = 0.005  # BER
in_file_path = 'test_files/alice29.txt'  # File to be transmitted
out_file_path = 'test_files/alice29_out.txt'  # File to be received


# EX 6, c
# Function to simulate a binary symmetric channel that receives a file as input and a BER and writes the output to a file
def simulate_bsc_file(input_file, output_file, p):
    # Read the input file with bytes
    with open(input_file, 'rb') as input_file:
        data = input_file.read()

    # Convert the bytes to a binary string
    in_sequence = ''.join(format(byte, '08b') for byte in data)

    # Apply the encoding with repetition
    encode_sequence = encoder_hamming(in_sequence, 3)

    # Apply the binary symmetric channel
    out_sequence = binary_symmetric_channel(encode_sequence, p)

    # Apply the decoding with repetition
    decode_sequence = decoder_hamming(out_sequence, 3)

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