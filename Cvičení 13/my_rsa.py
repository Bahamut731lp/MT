"""
    Modul implementující algoritmus RSA
"""
import math
import random

from tabulate import tabulate

from sieve import generate_primes_in_range

def rsa(string):
    start = 1000
    end = 10000
    user_input_converted = [ord(x) for x in list(string)]

    primes = generate_primes_in_range(start, end)

    print(primes)

    # 2 velká prvočísla "p" a "q"
    p, q = random.sample(primes, 2)

    # Modul
    n = p * q

    phi = (p - 1) * (q - 1)

    # Veřejný klíč
    e = random.randint(2, phi - 1)

    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    # Privátní klíč
    d = pow(e, -1, phi)

    #cyphered = [(np.array(user_input_converted.copy(), dtype=np.object_) ** e) % n]
    cyphered = [pow(x, e, n) for x in user_input_converted]

    # TODO: Tady zase možný bude něco s typama, chce to prověřit
    #decyphered = (np.copy(cyphered) ** d) % n
    decyphered = [pow(x, d, n) for x in cyphered]

    return {
        "original": {
            "text": string,
            "numerical": user_input_converted
        },
        "cyphered": {
            "text": "",
            "numerical": list(cyphered)
        },
        "decyphered": {
            "text": str.join("", [chr(x) for x in list(decyphered)]),
            "numerical": list(decyphered)
        }
    }

if __name__ == "__main__":
    user_input = input("Zadej zpravu pro zasifrovani:")
    result = rsa(user_input)
    print(tabulate([
        ["Původní zpráva", result["original"]["text"], result["original"]["numerical"]],
        ["Zašifrovaná zpráva", result["cyphered"]["text"], result["cyphered"]["numerical"]],
        ["Dešifrovaná zpráva", result["decyphered"]["text"], result["decyphered"]["numerical"]]
    ]))
