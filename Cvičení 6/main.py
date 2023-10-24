import numpy as np
from tabulate import tabulate

from rle import RLE
from huffman import Huffman

def main():
    integers = None

    with open("./data/Cv06_RLE_data.bin", "r", encoding="utf-8") as file_handle:
        integers = np.fromfile(file_handle, dtype='uint8')

    test_suites = {
        "Příklad z přednášky RLE": "AAAAAFFFFCHHH",
        "Příklad z přednášky Huffman": "ABRAKADABRA",
        "Binární data": "".join([str(x) for x in integers])
    }

    headers = ["Label", "Value"]
    methods = [RLE, Huffman]
    
    for method in methods:
        for (case, data) in test_suites.items():
            results = []
            driver = method()

            (compressed, additional) = driver.compress(data)
            decompressed = driver.decompress(compressed, additional)

            matching = data == decompressed

            results.append(["Label", case])
            results.append(["Algoritmus", driver.__class__.__name__])
            results.append(["Vstup", data])
            results.append(["Komprese", compressed])
            results.append(["Dodatečné", additional])
            results.append(["Dekomprese", decompressed])
            results.append(["Shodují se", matching])

            print(tabulate(results, headers=headers, tablefmt="rounded_outline"))

if __name__ == "__main__":
    main()
