# MASIVNÍ TODO:
# KDYŽ JE ČETNOST VÍC JAK JEDNOCIFERNÁ, JE TO V PÍČI
# NĚJAK TOHLE MUSÍME OŠÉFOVAT

class RLE:
    """
        Třída pro provedení RLE komprese a dekomprese nad daty
    """
    def compress(self, data: str):
        last_character = data[0]
        counter = 0
        result = []

        for character in list(data):
            if character == last_character:
                counter += 1
            else:
                result.append(str(counter) + last_character)
                counter = 1
                last_character = character

        # Přidání posledního znaku
        result.append(str(counter) + last_character)

        return ("".join(result), result)

    def decompress(self, _, data: list[str]):
        result = []

        for symbol in data:
            count = int(symbol[:-1])
            character = symbol[-1]
            result.append(character * count)

        return "".join(result)
