from collections import Counter
from types import SimpleNamespace
from functools import reduce

import numpy as np
from tabulate import tabulate

def sort_descending(x):
    """Funkce pro seřazení prvků sestupně

    Parameters
    ----------
    x
        Iterable

    Returns
    -------
        Seřazený iterable
    """
    return sorted(x, key=lambda v: v[0])

def round_probabilities(x):
    """Funkce pro zaokrouhlení hodnot v dict_items

    Parameters
    ----------
    x
        Tuple (klíč, hodnota)

    Returns
    -------
        List, ve kterém jsou tuples se zaokrouhleným druhým prvkem
    """

    return [(key, round(value, 2)) for key, value in x]

def get_occurences(x):
    """Funkce pro získání četností

    Parameters
    ----------
    x
        Iterable

    Returns
    -------
        List itemů slovníku ve tvaru (item, abs. četnost)
    """
    return list(dict(Counter(x)).items())

def normalize_fn_factory(length):
    """Funkce pro vytváření funkce normalizace

    Parameters
    ----------
    length
        Maximální hodnota, vůči které normalizovat
    """

    def inner_normalize(x):
        return [(key, value/length) for key, value in x]

    return inner_normalize

def parameterize(v):
    """Funkce pro strukturování

    Parameters
    ----------
    v
        Pole tuplů ve tvaru (klíč, hodnota)

    Returns
    -------
        Pole strukturovaných dat
    """

    # Zde používáme SimpleNamespace, kterej mi dovolí
    # přistupovat ke klíčům slovníku pomocí tečkové notace
    # je to jenom pro syntax sugar, nic víc.
    return [SimpleNamespace(**{"letter": x[0], "freq": x[1] }) for x in v]

class Interval():
    """
        Hezkej container pro práci s intervaly
    """
    def __init__(self, low: float, high: float) -> None:
        self.low: float = round(low, 2)
        self.high: float = round(high, 2)

    def __repr__(self):
        return f"({self.low}, {self.high})"

class Arithmetic():
    """
        Třída pro práci s aritmetickým kódováním
    """
    def compress(self, data: str):
        """Funkce pro kompresi pomocí aritmetického kódování

        Parameters
        ----------
        data
            Vstupní slovo

        Returns
        -------
            Výsledek a data nutná k dekompresi
        """

        # Četnosti znaků
        length = len(data)
        letters = list(data)

        # Pipeline pro získání pravděpodobností
        pipeline = [
            get_occurences,
            normalize_fn_factory(length),
            round_probabilities,
            sort_descending,
            parameterize
        ]

        # Redukce, která provede celej pipeline
        occurences = reduce(lambda acc, fn: fn(acc), pipeline, data)

        # Tahle redukce vytvoří z pole výskytů distribuční funkci
        # Vždycky to vezme předchozí výsledek a posune to vyšší hranici intervalu
        # Musíme začínat od 2. prvku (hence occurences[1:]), protože musíme taky správně udělat
        # počáteční podmínku - aka ten první
        intervals: list[Interval] = reduce(
            lambda result, current: (
                result + [(
                    current.letter,
                    Interval(result[-1][1].high, result[-1][1].high + current.freq)
                )]
            ),
            occurences[1:],
            [(occurences[0].letter, Interval(0, occurences[0].freq))]
        )

        # Předchozí redukce vytvořila list párů,
        # tak si to převedeme na slovník, ať se s tím líp pracuje
        intervals: dict[str, Interval] = dict(intervals)
        # Interval pro kódování
        interval = Interval(0, 1)

        for letter in letters:
            char_interval = intervals[letter]

            # Přepočítané hranice intervalu si uložíme do proměnné,
            # jinak bychom si je měnili uprostřed výpočtu
            new_low = interval.low + char_interval.low * (interval.high - interval.low)
            new_high = interval.low + char_interval.high * (interval.high - interval.low)

            # Nastavení nových hranic intervalu
            interval.low = new_low
            interval.high = new_high

        # Na konci průměrováním uděláme z intervalu reálné číslo
        result = (interval.low + interval.high) / 2

        # Pro úspěšné dekódování je potřeba vrátit i
        # - délku slova (abychom věděli, kdy skončit)
        # - rozdělení intervalů (abychom dokázali znaky interpretovat)
        return (result, interval, intervals, length)

    def decompress(self, data: float, model: dict[str, Interval], length: int):
        """Funkce pro dekomprimaci dat zakódovaných aritmetickým kódováním

        Parameters
        ----------
        data
            Zakódovaný výsledek
        model
            Slovník intervalů pro dekódování
        length
            Délka výstupního slova

        Returns
        -------
            Dekódovaný výsledek
        """
        # Interval pro dekódování
        interval = Interval(0, 1)
        # Pole pro výsledné znaky
        result = []

        # Omezení dekódování na správný počet znaků
        for _ in range(length):
            # Výpočet hodnoty K - aneb kde se číslo nachází v intervalu
            character_value = (data - interval.low) / (interval.high - interval.low)

            # Znak a interval znaku
            char = None
            char_interval = None

            # Hledání intervalu, ve kterém znak leží
            for key, inter in model.items():
                is_in_interval = all([
                    character_value >= inter.low,
                    character_value < inter.high
                ])

                if is_in_interval:
                    char = key
                    char_interval = inter
                    result.append(char)

            # Přepočítané hranice intervalu si uložíme do proměnné,
            # jinak bychom si je měnili uprostřed výpočtu
            new_low = interval.low + char_interval.low * (interval.high - interval.low)
            new_high = interval.low + char_interval.high * (interval.high - interval.low)

            interval.low = new_low
            interval.high = new_high

        # Výsledek vrátíme jako string
        return "".join(result)

def main():
    integers = None

    with open("./data/Cv07_Aritm_data.bin", "r", encoding="utf-8") as file_handle:
        integers = np.fromfile(file_handle, dtype='uint8')

    test_suites = {
        "Příklad z přednášky AR": "CBAABCADAC",
        "Příklad z přednášky RLE": "AAAAAFFFFCHHH",
        "Příklad z přednášky Huffman": "ABRAKADABRA",
        "Binární data": "".join([str(x) for x in integers])
    }

    for (case, data) in test_suites.items():
        driver = Arithmetic()
        results = []

        (compressed, interval, model, length) = driver.compress(data)
        decompressed = driver.decompress(compressed, model, length)

        matching = data == decompressed

        print("\n\n\n")
        results.append(["Label", case])
        results.append(["Vstup", data])
        results.append(["Výstup komprese", compressed])
        results.append(["Interval", interval])
        results.append(["Model", model])
        results.append(["Délka", length])
        results.append(["Výstup dekomprese", decompressed])
        results.append(["Shodují se", matching])

        print(tabulate(results, tablefmt="simple"))

if __name__ == "__main__":
    main()