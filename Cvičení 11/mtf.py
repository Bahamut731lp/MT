from tabulate import tabulate

alphabet = list("abcdefghijklmnopqrstuvwxyz")
user_input = input("Zadej vstup pro MTF: ")

# Encoding
encoding_stack = alphabet.copy()
encoded_output = []

for character in list(user_input):
    if character not in encoding_stack:
        message = f"Znak '{character}' není v povolené abecedě"
        raise LookupError(message)

    index = encoding_stack.index(character)
    encoded_output.append(str(index))

    encoding_stack.remove(character)
    encoding_stack.insert(0, character)

# Decoding
decoding_stack = alphabet.copy()
decoded_output = []

for index in encoded_output:
    character = decoding_stack[int(index)]
    decoded_output.append(character)

    decoding_stack.remove(character)
    decoding_stack.insert(0, character)

print(tabulate([
    [user_input, str.join(", ", encoded_output), str.join("", encoding_stack)],
    [str.join("", encoded_output), str.join("", decoded_output), str.join("", decoding_stack)]
]))