import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def calc_closest_factors(c: int):
    """Calculate the closest two factors of c.

    Returns:
      [int, int]: The two factors of c that are closest; in other words, the
        closest two integers for which a*b=c. If c is a perfect square, the
        result will be [sqrt(c), sqrt(c)]; if c is a prime number, the result
        will be [1, c]. The first number will always be the smallest, if they
        are not equal.
    """
    if c//1 != c:
        raise TypeError("c must be an integer.")

    a, b, i = 1, c, 0
    while a < b:
        i += 1
        if c % i == 0:
            a = i
            b = c//a

    return [b, a]

def count_circles(path: Path):
    img = cv2.imread(path.as_posix(), cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(img, (7, 7), 0)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    # Použil jsem cv2.HOUGH_GRADIENT_ALT
    # Protože pak je param2 míra "perfektnosti" kruhu, basically jak moc kruh musí být kruh
    # Ono to takhle funguje i při tom normálním, ale prostě mi tohle fungovalo, narozdíl od toho prvního
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT_ALT, 1, 20, param1=50, param2=0.8, minRadius=0, maxRadius=0)
    circles = np.uint16(np.around(circles))

    font = cv2.FONT_HERSHEY_DUPLEX
    text = str(len(circles[0,:]))
    font_thickness = 4
    font_size = 4
    font_color = (255, 0, 0)
    size, _ = cv2.getTextSize(text, font, font_size, font_thickness)

    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

    center_x = round(img.shape[0] / 2) - round(size[0] / 2)
    center_y = round(img.shape[1] / 2) + round(size[1] / 2)

    cv2.putText(cimg, text, (center_x, center_y), font, font_size, font_color, font_thickness)

    return cimg, len(circles[0,:])

def analyze_circles(files):
    no_of_files = len(files)
    subplot_factors = calc_closest_factors(no_of_files)
    index = 0

    plt.figure("Detekované kruhy v obrázcích")
    for path in files:
        image, circles = count_circles(path)
        print(f"Found {circles} circle(s) in {path.name}")
        index += 1

        plt.subplot(subplot_factors[0], subplot_factors[1], index)
        plt.imshow(image)

    plt.show()

def encode_with_erosion(path):
    image = cv2.imread(path.as_posix(), cv2.IMREAD_GRAYSCALE) / 255
    kernel = np.ones((3, 3), np.uint8)
    half_height = image.shape[0] // 2

    # Analyzované prvky v obrázku - horní a dolní polovina obrázku
    features = [image[:half_height, :], image[half_height:, :]]

    # Slovník grafů, které budou na konci procedury vykresleny.
    plots = {
        "Image": image,
    }

    # Analýza prvků
    for index, feature in enumerate(features):
        # Počet souřadnic prvků - počítáme s tím, že na konci bude jenom jedna
        coordinates_count = len(feature)
        # Počet iterací eroze
        iterations = 0
        # Kopie obrázku pro postupnou erozi
        encoded_image = feature.copy()

        # Nalezení počtu iterací nutných k zakódování
        while True:
            # Zakódování pomocí eroze
            temporary_image = cv2.erode(encoded_image, kernel)
            # Updatování počtu souřadnic
            coordinates_count = len(np.column_stack(np.where(temporary_image != 0)))

            # Pokud jsme ztratili informaci o značkách (a.k.a eroze odstranila už všechno)
            # Tak to přerušíme a necháme staré výsledky
            if coordinates_count == 0:
                break

            # Pokud ještě souřadnice zbyly, přičteme iteraci a nastavíme mezivýsledek
            iterations += 1
            encoded_image = temporary_image

        # Přidání zakódovaného obrázku do grafů
        plots[f"Feature {index} - Enkódovaný"] = encoded_image

        # Získání souřadnic značek
        coordinates = np.column_stack(np.where(encoded_image != 0))

        print("")
        print(f"Souřadnice značek (feature {index}): {coordinates[0]}")
        print(f"Počet iterací: {iterations}")
        print("")

        # Dekódování pomocí dilatace
        decoded_image = cv2.dilate(encoded_image, kernel, iterations=iterations)
        plots[f"Feature {index} - Dekódovaný"] = decoded_image

    # Vykreslení grafů
    plt.figure("Eroze a dilatace")
    subplot_factors = calc_closest_factors(len(plots.keys()))
    index = 1

    for label, image_data in plots.items():
        plt.subplot(subplot_factors[0], subplot_factors[1], index)
        plt.title(label)
        plt.imshow(image_data, cmap="gray")

        index += 1

    # Ukázání okna s grafy
    plt.show()

if __name__ == "__main__":
    analyze_circles(list(Path("./data").glob("Cv11_c*.bmp")))
    encode_with_erosion(Path("./data/Cv11_merkers.bmp"))
