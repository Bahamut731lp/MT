"""
    Program řešící cvičení 4 z předmětu MT
"""
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm


def main():
    """
        Hlavní funkce programu
    """
    images_etalons_mapping = {
        "./data/Cv04_porucha1.bmp": "./data/Cv04_porucha1_etalon.bmp",
        "./data/Cv04_porucha2.bmp": "./data/Cv04_porucha2_etalon.bmp"
    }

    # Jasová korekce obrázků
    for (source, error) in images_etalons_mapping.items():
        result = brightness_correction(Path(source), Path(error))

        plt.figure(f"Korekce obrázku {source}")

        plt.subplot(1, 3, 1)
        plt.imshow(result["original"])

        plt.subplot(1, 3, 2)
        plt.imshow(result["etalon"])

        plt.subplot(1, 3, 3)
        plt.imshow(result["corrected"])

        plt.show(block=False)

    # Ekvalizace histogramu
    her = histogram_equalization(Path("./data/Cv04_rentgen.bmp"))

    plt.figure("Ekvalizace histogramu obrázku")

    plt.subplot(2, 2, 1)
    plt.imshow(her["original"]["image"])

    plt.subplot(2, 2, 2)
    plt.xlim([0, 255])
    plt.xticks(ticks=range(0, 257, 16), labels=range(0, 257, 16))
    plt.yscale('log')
    plt.plot(her["original"]["histogram"])

    plt.subplot(2, 2, 3)
    plt.imshow(her["equalized"]["image"])

    plt.subplot(2, 2, 4)
    plt.xlim([0, 255])
    plt.xticks(ticks=range(0, 257, 16), labels=range(0, 257, 16))
    plt.yscale('log')
    plt.plot(her["equalized"]["histogram"])

    plt.show(block=False)

    input("Pro ukončení stiskni libovolnou klávesu")

def brightness_correction(source: Path, error: Path, c = 255):
    """Funkce pro jasovou korekci obrázku

    Args:
        source (Path): Cesta ke zkreslenému obrázku
        error (Path): Cesta k etalonu poruchy
        c (int, optional): Konstanta jasu. Defaults to 255.

    Raises:
        FileNotFoundError: _description_
    """

    if not source.exists() or not error.exists():
        raise FileNotFoundError()

    image = cv2.imread(source.as_posix())
    etalon = cv2.imread(error.as_posix())

    width = image.shape[0]
    height = image.shape[1]
    depth = image.shape[2]

    result = image.copy()

    for y in range(0, width):
        for x in range(0, height):
            for d in range(0, depth):
                result[y, x, d] = (c * image[y, x, d]) / (etalon[y, x, d])

    return {
        "original": image,
        "etalon": etalon,
        "corrected": result
    }

def histogram_equalization(source: Path):
    """Funkce pro ekvalizaci histogramu obrázků

    Args:
        source (Path): Cesta k obrázku

    Raises:
        FileNotFoundError: Cesta k obrázku neexistuje nebo není souborem

    Returns:
        dict: Slovník s novým obrázkem, jeho histogramem a ekvalizovanými ekvivalenty
    """
    if not source.exists() or not source.is_file():
        raise FileNotFoundError()

    image = cv2.imread(source.as_posix())
    equalized = image.copy()
    # Funkce calcHist vrací pole o délce 256 se zastoupením jednotlivých hodnot jasů (0 - 255)
    histogram = cv2.calcHist([image], [0], None, [256], [0, 256])

    min_intensity = 0
    lowest_intensity = 0
    max_intensity = 255
    width = image.shape[0]
    height = image.shape[1]

    for y in tqdm(range(0, width), desc="Ekvalizace Histogramu"):
        for x in range(0, height):
            intensity = image[y, x, 0]
            cumulative_intensity = [int(x) for x in histogram[lowest_intensity:intensity]]
            equalized[y, x] = (max_intensity / (width * height)) * sum(cumulative_intensity)

    equalized_histogram = cv2.calcHist([equalized], [0], None, [256], [0, 256])

    return {
        "original": {
            "image": image,
            "histogram": histogram
        },
        "equalized": {
            "image": equalized,
            "histogram": equalized_histogram
        }
    }


if __name__ == "__main__":
    main()
