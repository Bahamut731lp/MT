"""Funkce řešící cvičení 5 z MT

Raises:
    LookupError: Pokud není fráze nalezena ve slovníku
"""
import numpy as np
from tabulate import tabulate

class LZW:
    """
        Třída pro provedení LZW komprese a dekomprese nad daty
    """
    def __init__(self, data: list[str]) -> None:
        self.data = data
        self.ratio = 0
        self.alphabet = {v:str(k + 1) for k,v in enumerate(sorted(list(set(data))))}
        self.max_iters = 1000

    def compress(self):
        """Metoda pro kompresi dat

        Raises:
            LookupError: Pokud abeceda není úplná a nelze v ní najít novou frázi

        Returns:
            list[str]: Výsledný řetězec
        """
        phrases = self.alphabet.copy()
        remainder = self.data.copy()
        iteration = 0
        result = []

        while len(remainder) > 0 and iteration < self.max_iters:
            iteration += 1
            longest_phrase = remainder
            longest_phrase_str = "".join(longest_phrase)

            # Nalezení nejdelší fráze
            # Pokud není fráze v seznamu frází, odebere poslední znak a zkusíme znovu
            # Když zbyde prázdný string, vyhodí LookupError
            while longest_phrase_str not in phrases:
                # Odstranění posledního znaku
                longest_phrase = longest_phrase[:-1]
                # Převod na string
                longest_phrase_str = "".join(longest_phrase)

                # Pokud bude fráze prázdný string, tak se něco pokazilo a bude to chtít debugnout.
                if not longest_phrase:
                    raise LookupError(f"Z řetězce {remainder} nemohla být vygenerována nová fráze")


            # Zaznamenání indexu nalezení fráze
            result.append(phrases[longest_phrase_str])
            # Nová fráze
            new_phrase = "".join(remainder[0:len(longest_phrase) + 1])
            # Index nové fráze ve slovníku
            new_phrase_index = len(phrases.items())
            # Přičítáme + 1, protože abecedu taky začínáme jedničkou
            phrases[new_phrase] = str(new_phrase_index + 1)
            # Odstranění již nalezené fráze ze zbytku
            remainder = remainder[len(longest_phrase):]

        self.data = result
        return True

    def decompress(self):
        """Metoda pro dekompresi dat

        Returns:
            list[str]: Pole dekomprimovaných znaků
        """
        phrases = {v: k for k, v in self.alphabet.copy().items()}
        remainder = self.data.copy()
        iteration = 0
        result = []

        while len(remainder) > 0 and iteration < self.max_iters:
            iteration += 1
            # První enkódovaný znak ve zbytku
            encoded_symbol = remainder[0]

            # Pokud je enkódovaný znak v seznamu frází,
            # stačí ho přidat do výsledků
            # Nová fráze je pak předposlední výsledek a první znak tohodle posledního výsledku
            if encoded_symbol in phrases:
                result.append(phrases[encoded_symbol])

                if len(result) > 1:
                    new_phrase_index = str(len(phrases.items()) + 1)
                    phrases[new_phrase_index] = result[-2] + result[-1][0]

            else:
                if len(result) > 0:
                    new_phrase_index = len(phrases.items()) + 1
                    nwe_phrase = result[-1] + result[-1][0]
                    phrases[new_phrase_index] = nwe_phrase
                    result.append(nwe_phrase)

            remainder = remainder[1:]

        self.data = result
        return True

def main():
    """
        Hlavní metoda programu
    """
    with open("./data/Cv05_LZW_data.bin", "r", encoding="utf-8") as file_handle:
        integers = np.fromfile(file_handle, dtype='uint8')

        test_suites = {
            "Příklad z přednášky": ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'b', 'c', 'b', 'a'],
            "Binární data": [str(x) for x in integers]
        }

        headers = ["Label", "Originál", "Komprese", "Dekomprese", "Shodují se"]
        results = []

        for (key, value) in test_suites.items():
            result = [key]

            # Záznam původních dat
            driver = LZW(value)
            result.append("".join(driver.data))

            # Komprese
            driver.compress()
            result.append("".join(driver.data))

            # Dekomprese
            driver.decompress()
            result.append("".join(driver.data))

            # Kontrola, jestli nedošlo ke ztrátě informace
            result.append(result[1] == result[3])

            # Přidání výsledku do tabulky
            results.append(result)

        print(tabulate(results, headers=headers, tablefmt="rounded_outline"))

if __name__ == "__main__":
    main()