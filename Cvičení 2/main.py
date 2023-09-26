import numpy as np
import matplotlib.pyplot as plt
import struct
import os
from glob import iglob
from pathlib import Path
from tabulate import tabulate

ERRORS = {
    "not_a_file": "Cesta není souborem nebo neexistuje",
    "not_a_riff": "Soubor není ve formátu RIFF",
    "bad_length": "Špatná délka souboru",
    "not_a_wave": "Soubor není ve formátu WAVE",
    "not_format_start": "Soubor nemá počátek shluku fmt",
    "bad_format_length": "Soubor má špatně zakódovanou délku shluku fmt",
    "bad_data_length": "Špatná délka shluku dat"
}

COMPRESSION = {
    0: "Neznámá",
    1: "PCM",
    2: "Microsoft ADPCM",
    6: "ITU G.711 a-law",
    7: "ITU G.711 Âμ-law",
    17: "IMA ADPCM",
    20: "ITU G.723 ADPCM (Yamaha)",
    49: "GSM 6.10",
    64: "ITU G.721 ADPCM",
    80: "MPEG"
}

FORMAT = {
    1: "B",
    2: "h"
}

def make_plot(A2, VF, SIG):
    t = np.arange(A2).astype(float)/VF
    plt.plot(t, SIG)
    plt.xlabel('t[s]')
    plt.ylabel('A[-]')
    plt.show()

def analyze(path: str):
    size = os.path.getsize(path)

    result = {
        "name": Path(path).name,
        "x": [],
        "y": [],
        "compression": "",
        "channels": 0,
        "sampling_frequency": 0,
        "is_valid": True,
        "error": None
    }

    with open(path, 'rb') as f:
        # RIFF
        riff_string = f.read(4)
        if riff_string != b'RIFF':
            result["error"] = ERRORS["not_a_riff"]
            result["is_valid"] = False
            return result

        file_size = struct.unpack('i', f.read(4))[0]
        # Proč -8 ? Protože se do délky A1 v hlavičce nepočítá RIFF 
        # a ta samotná informace o délce (8 byte-ů)
        if file_size != size - 8:
            result["error"] = ERRORS["bad_length"]
            result["is_valid"] = False
            return result

        wave_string = f.read(4)
        if wave_string != b'WAVE':
            result["error"] = ERRORS["not_a_wave"]
            result["is_valid"] = False
            return result

        # Formát
        format_position = f.tell()
        format_string = f.read(4)
        if format_string != b'fmt ':
            result["error"] = ERRORS["not_format_start"]
            result["is_valid"] = False
            return result

        format_length = struct.unpack('i', f.read(4))[0]
        f.seek(format_length, 1)

        data_position = f.tell()
        data_string = f.read(4)
        if data_string != b'data':
            result["error"] = ERRORS["bad_format_length"]
            result["is_valid"] = False
            return result

        format_length = struct.unpack('i', f.read(4))[0]
        f.seek(format_position + 8)

        compression_index = struct.unpack("H", f.read(2))[0]
        channels = struct.unpack("H", f.read(2))[0]
        VF = struct.unpack('i', f.read(4))[0]
        PB = struct.unpack('i', f.read(4))[0]
        VB = struct.unpack("H", f.read(2))[0]
        VV = struct.unpack("H", f.read(2))[0]
        channel_block_size = int(VB / channels)

        result["compression"] = COMPRESSION[compression_index if compression_index in COMPRESSION else 0]  
        result["channels"] = channels
        result["sampling_frequency"] = VF

        # Přeskončení dodatečných bytů v fmt chunku.
        f.seek(data_position - f.tell(), 1)
        # Přeskočení data stringu, víme z dřívějška, že tam je
        f.seek(4, 1)

        remaining_size = struct.unpack('i', f.read(4))[0]

        # Ověření pravdivosti A2 - Délky zbývajících dat s celkovou délkou souboru
        # Přičítáme osmičku, protože do zbývající délky se nepočítá b'data' a zbývající délka
        # Musíme tyhle části tedy přeskočit, a ty mají vždy 8 byte-ů
        if data_position + 8 + remaining_size != size:
            result["error"] = ERRORS["bad_data_length"]
            result["is_valid"] = False
            return result

        # data
        blocks = int(remaining_size / VB)
        signal = [[0 for _ in range(blocks)] for j in range(channels)]

        for i in range(0, blocks):
            for j in range(0, channels):
                signal[j][i] = struct.unpack(FORMAT[channel_block_size], f.read(channel_block_size))[0]

        COLUMNS = 2 if channels > 2 else 1
        ROWS = round(channels / COLUMNS)
        t = np.arange(blocks).astype(float)/VF

        plt.figure(result["name"])

        for m in range(0, channels):
            plt.subplot(ROWS, COLUMNS, m+1)
            plt.plot(t, signal[m][::])
            plt.title("Channel no.:"+str(m+1))
            plt.xlabel('t[s]')
            plt.ylabel('A[-]')
        plt.show(block=False)

        return result

if __name__ == "__main__":
    CURRENT_DIR = Path(__file__).parent
    DATA_PATH = Path(CURRENT_DIR, "data", "*.wav").resolve().as_posix()
    WAVES = list(iglob(DATA_PATH))
    index = 1

    for wave in WAVES:
        result = analyze(wave)
        print(tabulate(result.items(), tablefmt="rounded_outline"))
        index += 1

    input("Enter")


# t = np.arange(A2).astype(float)/VF
# plt.plot(t, SIG)
# plt.xlabel('t[s]')
# plt.ylabel('A[-]')
# plt.show()
