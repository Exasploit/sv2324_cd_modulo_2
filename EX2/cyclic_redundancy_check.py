

# data: binary string
# generator: binary string
# return: remainder as binary string
def cyclic_redundancy_check(data, generator):
    # Convert generator string to a list of integers
    generator = [int(bit) for bit in generator]

    # Convert data string to a list of integers
    data = [int(bit) for bit in data]

    # Append zeros to the data to match the length of the generator
    data += [0] * (len(generator) - 1)

    # Perform the CRC
    for i in range(len(data) - len(generator) + 1):
        if data[i] == 1:
            for j in range(len(generator)):
                data[i + j] = data[i + j] ^ generator[j]

    # Return the remainder
    return ''.join(str(bit) for bit in data[-len(generator) + 1:])





