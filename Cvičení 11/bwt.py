from collections import deque
from tabulate import tabulate

alphabet = list("abcdefghijklmnopqrstuvwxyz")
user_input = input("Zadej vstup pro BWT: ")

# Encoding
encoding_stack = alphabet.copy()
encoded_output = []

block_size = len(user_input)
encoding_matrix = [user_input] * block_size

for i, x in enumerate(encoding_matrix):
    queue = deque(x)
    queue.rotate(i)
    encoding_matrix[i] = str.join("", queue)

encoding_matrix = sorted(encoding_matrix)
encoded_output = str.join("", [x[-1] for x in encoding_matrix])
input_index = encoding_matrix.index(user_input)

# Decoding
decoding_matrix = list(encoded_output)
for i in range(len(encoded_output) - 1):
    letters_to_add = [x[-1] for x in sorted(decoding_matrix)]
    decoding_matrix = [x + y for x, y in zip(decoding_matrix, letters_to_add)]

decoding_matrix = sorted(decoding_matrix)
decoded_output = decoding_matrix[input_index]

print(tabulate([
    [user_input, encoded_output, tabulate(encoding_matrix, tablefmt="fancy_grid")],
    [encoded_output, decoded_output, tabulate(decoding_matrix, tablefmt="fancy_grid")]
]))
