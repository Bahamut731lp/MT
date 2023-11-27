import numpy as np
from tabulate import tabulate
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--binary", action="store_true", default=True)
parser.add_argument("-d", "--decimal", action='store_true', default=False)
parser.add_argument("-t", "--test", action='store_true', default=False)
args = parser.parse_args()

headers = []
if args.decimal:
    headers.append("INPUT (DEC)")

if args.binary:
    headers.append("INPUT (BIN)")

if args.decimal:
    headers.append("OUTPUT (DEC)")

if args.binary:
    headers.append("OUTPUT (BIN)")

if args.test:
    headers.append("TEST")


rows = []

values = range(256)
converted = []

test_cases = {
    "0": "0",
    "1": "1",
    "2": "3",
    "3": "2",
    "4": "6",
    "5": "7",
    "6": "5",
    "7": "4",
    "8": "12",
    "9": "13",
    "10": "15",
    "11": "14",
    "12": "10",
    "13": "11",
    "14": "9",
    "15": "8"
}

for number in values:
    binary = int(bin(number), 2)
    # ^ je XOR operátor
    # >> je znaménkový posun vpravo
    # Jinak řečeno, dělá se tady XOR mezi bitem a tím předchozím
    encoded = binary ^ (binary >> 1)
    row = []

    if args.decimal:
        row.append(binary)

    if args.binary:
        row.append(np.binary_repr(binary, 8))

    if args.decimal:
        row.append(encoded)

    if args.binary:
        row.append(np.binary_repr(encoded, 8))

    if args.test:
        test = test_cases[str(number)] if str(number) in test_cases else ""
        test_output = "✔️" if test == str(encoded) else "❌"
        test_output = test_output if test != "" else ""
        row.append(test_output)

    rows.append(row)

print(tabulate(rows, headers=headers, tablefmt="github"))
