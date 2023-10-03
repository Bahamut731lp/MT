import struct
from pathlib import Path
import cv2
import numpy as np
import math
from tabulate import tabulate
import matplotlib.pyplot as plt

def imread(path: Path):
    if not path.exists():
        return None

    with open(path, "rb") as f:
        bm = f.read(2)
        if bm != b'BM':
            raise Exception("BM")

        # Velikost souboru v bajtech
        size = struct.unpack('i', f.read(4))[0]
        # Rezerovavné bajty
        reserved = struct.unpack('i', f.read(4))[0]
        # Počet bajtů v hlavičce
        bytes_in_header = struct.unpack('i', f.read(4))[0]
        # Nějaký random bajty - nemaj žádnou funkci afaik
        _ = struct.unpack('i', f.read(4))[0]
        # Šířka obrázku v px
        width = struct.unpack('i', f.read(4))[0]
        # Výška obrázku v px
        height = struct.unpack('i', f.read(4))[0]
        # Počet ploch v obraze
        surfaces = struct.unpack("H", f.read(2))[0]
        # Počet bitů na pixel
        bits_per_pixel = struct.unpack("H", f.read(2))[0]
        # Typ komprese
        compression = struct.unpack('i', f.read(4))[0]
        # Velikost dat v bajtech
        data_size = struct.unpack('i', f.read(4))[0]
        # Horizontální počet pixelů na metr
        horizontal_pixels_per_meter = struct.unpack('i', f.read(4))[0]
        # Vertikální počet pixelů na metr
        vertical_pixels_per_meter = struct.unpack('i', f.read(4))[0]
        # Počet barev (pokud jsou definované)
        no_of_colors = struct.unpack('i', f.read(4))[0]
        # Počet důležitých barev (pokud jsou definované)
        no_of_important_colors = struct.unpack('i', f.read(4))[0]
        # Velikost jednoho řádku tak, aby byl dělitelný 4
        row_size = math.ceil(bits_per_pixel * width / 32) * 4
        # Převod z bitů na bajty (na pixel)
        bytes_per_pixel = int(bits_per_pixel / 8)
        # Inicializace obrazových dat
        image_data = np.ndarray((width, height, bytes_per_pixel), dtype="uint8")

        for row in image_data:
            col_index = 0
            for column in row:
                for channel in range(bytes_per_pixel):
                    column[channel] = struct.unpack('B', f.read(1))[0]
                    col_index += 1

            # Každý řádek dat musí být dělitelný 4
            # Tudíž občas tam jsou vyplňující nuly
            # Tyhle potřebujeme přeskočit
            f.seek(abs(row_size - col_index), 1)

        return {
            "size": size,
            "header": {
                "name": path.name,
                "size": bytes_in_header,
                "width": width,
                "height": height,
                "surfaces": surfaces,
                "compression": compression,
                "bits per pixel": bits_per_pixel,
                "resolution": {
                    "horizontal": horizontal_pixels_per_meter,
                    "vertical": vertical_pixels_per_meter
                }
            },
            "data": {
                "size": data_size,
                "content": image_data
            }
        }

if __name__ == "__main__":
    color_spaces = {
        "RGB2GRAY": cv2.COLOR_RGB2GRAY,
        "RGB2HSV": cv2.COLOR_RGB2HSV,
        "BGR2YCR_CB": cv2.COLOR_BGR2YCR_CB
    }

    img = imread(Path("./cv03_objekty1.bmp"))

    # Vytištění informací o souboru do konzole
    print(
        tabulate(
            img.get("header").items(),
            tablefmt="rounded_outline"
        )
    )

    data = cv2.cvtColor(img["data"]["content"], cv2.COLOR_BGR2RGB)
    data = cv2.flip(data, 0)

    # Okno s RGB a Šedým obrázkem
    plt.figure("RGB a Šedotón")
    plt.subplot(1, 2, 1)
    plt.title("RGB")
    plt.imshow(data)

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(data, cv2.COLOR_RGB2GRAY), cmap="gray")
    plt.title("Gray")

    # RGB a HSV
    plt.figure("RGB a HSV")
    h, s, v = cv2.split(cv2.cvtColor(data, cv2.COLOR_RGB2HSV))

    plt.subplot(2, 2, 1)
    plt.imshow(data)
    plt.colorbar()
    plt.subplot(2, 2, 2)
    plt.imshow(h, cmap="jet")
    plt.title("H")
    plt.colorbar()
    plt.subplot(2, 2, 3)
    plt.imshow(s, cmap="jet")
    plt.title("S")
    plt.colorbar()
    plt.subplot(2, 2, 4)
    plt.imshow(v, cmap="jet")
    plt.title("V")
    plt.colorbar()

    #BGR na YCR_CB
    plt.figure("COLOR_BGR2YCR_CB")
    ycr = cv2.cvtColor(cv2.flip(img["data"]["content"], 0).copy(), cv2.COLOR_BGR2YCR_CB)
    plt.subplot(2, 2, 1)
    plt.imshow(data, cmap="jet")
    plt.colorbar()
    plt.subplot(2, 2, 2)
    plt.imshow(ycr[:,:,0], cmap="gray")
    plt.title("Y")
    plt.colorbar()
    plt.subplot(2, 2, 3)
    plt.imshow(ycr[:,:,2], cmap="jet")
    plt.title("Cb")
    plt.colorbar()
    plt.subplot(2, 2, 4)
    plt.title("Cr")
    plt.imshow(ycr[:,:,1], cmap="jet")
    plt.colorbar()

    plt.figure("cv03_red_object.jpg")
    ball = cv2.cvtColor(cv2.imread("./cv03_red_object.jpg"), cv2.COLOR_BGR2RGB)
    ball2 = ball.copy()
    plt.subplot(1, 2, 1)
    plt.imshow(ball)

    rows,cols,_ = ball.shape

    # Thresholding podle zadání
    for i in range(rows):
        for j in range(cols):
            r, g, b = ball[i,j].tolist()

            try:
                thresh = r / (r + g + b)
                if thresh < 0.5:
                    ball2[i, j] = [255, 255, 255]
            except:
                continue

    plt.subplot(1, 2, 1)
    plt.imshow(ball)

    plt.subplot(1, 2, 2)
    plt.imshow(ball2)

    plt.show()
    #plt.show(block=False)
    #input()
    #for (label, space) in color_spaces.items():
    #     converted = cv2.cvtColor(img["data"]["content"], space)
    #     cv2.imshow(label, converted)
    cv2.waitKey(0)