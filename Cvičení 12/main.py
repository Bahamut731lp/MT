from collections import Counter
import numpy as np
from tabulate import tabulate

xor = {
    (0, 0): 0,
    (0, 1): 1,
    (1, 0): 1,
    (1, 1): 0
}

# Vysláno: [11, 11, 9, 22, 23, 8]
# Přijato: [3, 11, 11, 22, 23, 0]
def opravit_inverzni_kod(prijata_data):
    opravena_data = []
    for i in range(0, len(prijata_data), 2):
        
        number_1 = prijata_data[i]
        number_2 = prijata_data[i+1]

        # Nahradit stejným způsobem, jako je cv11 - tam je ten XOR jednoduší
        binary_data = [int(x) for x in list(np.binary_repr(number_1, 8))]
        binary_safety = [int(x) for x in list(np.binary_repr(number_2, 8))]
        zeroes = Counter(list(binary_data))[0]
        binary_safety_inverse = binary_safety
        is_inverted = zeroes % 2 != 0

        # Lichý počet nul v zabezpečovací části, musíme invertovat
        if is_inverted:
            binary_safety_inverse = [int(x) for x in np.logical_not(binary_safety).astype("int")]

        # Pokud se inverze shoduje s druhým číslem, je číslo správné
        if list(binary_data) == list(binary_safety_inverse):
            opravena_data.append(prijata_data[i])

        # Pokud je, je tam chyba a je jí třeba opravit (pokud lze)
        else:
            errors = []

            data_fixed = binary_data.copy()
            safety_fixed = binary_safety.copy()

            for i in range(0, len(binary_data)):
                data_char = binary_data[i]
                safety_char = binary_safety_inverse[i]
                fixed_char = xor[data_char, safety_char]

                errors.append(str(fixed_char))

            test = {v:k for k, v in Counter(errors).items()}
            error_character = test[1]
            error_index = errors.index(str(error_character))

            if error_character == "1":
                safety_fixed[error_index] = abs(1 - safety_fixed[error_index])
            else:
                data_fixed[error_index] = abs(1 - data_fixed[error_index])

            print("\n")
            print(tabulate([
                ["přijato [DEC]", number_1, number_2],
                ["přijato [BCD]", np.binary_repr(number_1, 8), np.binary_repr(number_2, 8)],
                ["překódováno", str.join('', [str(x) for x in binary_data]), str.join('', [str(x) for x in binary_safety_inverse])],
                ["Výsledek XOR", str.join('', errors)],
                ["chyba v části", "zabezpečovací" if error_character == "1" else "informační"],
                ["opraveno",  data_fixed,  safety_fixed]
            ]))
            print("\n")

            opravena_data.append(int(str.join("", [str(x) for x in data_fixed]), 2))

    return opravena_data

prijata_data = np.array([160, 223, 64, 65, 128, 126], dtype=np.uint8)
opravena_data = opravit_inverzni_kod(prijata_data)
print(opravena_data)