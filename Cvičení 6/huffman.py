from collections import Counter

class Huffman():
    def compress(self, data: str):
        # Četnosti znaků
        length = len(data)
        occurences= dict(Counter(data))
        pairs = list(occurences.items())
        letters = dict([(key, []) for key, _ in pairs])
        occurences = [(key, round(value/length, 2)) for key, value in pairs]
        result = []

        # Posčítání pravděpodobností
        while len(occurences) > 1:
            last_two = occurences[-2:]
            new_pair = tuple(
                map(
                    lambda symbol, probability: symbol + probability,
                    last_two[0],
                    last_two[1]
                )
            )

            

            # Přidání do seznamu sekvencí pro písmena
            for (index, word) in enumerate([x for x,_ in last_two]):
                priority = 1 - index

                for letter in word:
                    if letter not in letters:
                        print("DOPÍČI")

                    letters[letter].append(str(priority))

            # Odseknutí posledních dvou hodnot, ze kterých jsme dělali novou sekvenci
            occurences = occurences[:-2]
            # Přidání nové sekvence
            occurences.append(new_pair)
            # Seřazení podle pravděpodobnosti
            occurences = sorted(occurences, key=lambda x: (x[1]), reverse=True)
            # Připočtení hloubky stromu

        # Otočení sekvencí pro písmena
        for sequence in letters:
            rev = list(reversed(letters[sequence]))
            string = "".join(rev)
            letters[sequence] = string

        # Přeložení písmen ze vstupu na slova v huffmanově kódování
        for letter in data:
            result.append(letters[letter])

        return ("".join(result), letters)

    def decompress(self, data: str, tree: dict):
        remainder = list(data)
        lookup = {value:key for key, value in tree.items()}
        result = []

        while len(remainder) > 0:
            sequence = ""
            index = 0

            while sequence not in lookup:
                sequence += remainder[index]
                index += 1

                if index > len(remainder):
                    print("JE TO GIGA V KUNDĚ")
                    break

            remainder = remainder[len(sequence):]
            result.append(lookup[sequence])

        return "".join(result)
