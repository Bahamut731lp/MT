import cv2
import numpy as np
import matplotlib.pyplot as plt

vidcap = cv2.VideoCapture('./data/cv08_video.mp4')
success, image = vidcap.read()
count = 0
P = 5

def get_dct(frame):
    # Compute the DCT
    dct_image = cv2.dct(np.float32(frame))
    coefficients = np.absolute(dct_image.flatten())
    top_n_indices = np.argsort(coefficients)[-P:]
    top_n_coefficients = np.log(coefficients[top_n_indices])[::-1]

    return top_n_coefficients

distances = []
last_vector = None
last_image = None

method_1_seg_values = []
method_2_seg_values = []
method_3_seg_values = []
method_4_seg_values = []

# While read is successful, ie. no corrupted data
while success:
    # Převod snímku do barevného složky zvoleného barevného prostoru
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    grayscale = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    if last_image is not None:
        last_grayscale = cv2.cvtColor(last_image, cv2.COLOR_RGB2GRAY)

        # Převod z uint8, protože jinak to při operacích přetejká a dělá brikule
        img_1 = last_image.astype("int32")
        img_2 = rgb.astype("int32")

        # Rozdíl sum hodnot obrazových bodů v následujících snímcích
        method_1 = np.absolute(
            np.subtract(
                np.sum(img_1),
                np.sum(img_2)
            )
        )

        # Spočítáme sumu barevných hodnot pixelů v diferenci
        # Je to v podstatě ekvivalentní zápisu cv2.absdiff(last_image, rgb)

        # Suma rozdílů hodnot obrazových bodů v následujících snímcích
        method_2 = np.sum(
            np.absolute(
                np.subtract(
                    img_1,
                    img_2
                )
            )
        )

        # Histogramově založená metoda
        # Použil jsem šedé tóny
        hist1 = cv2.calcHist([last_grayscale], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([grayscale], [0], None, [256], [0, 256])
        method_3 = np.sum(np.absolute(np.subtract(hist1, hist2)))

        # Metoda založena na DCT
        last_image_dct = get_dct(last_grayscale)
        image_dct = get_dct(grayscale)
        method_4 = np.sum(np.absolute(np.subtract(last_image_dct, image_dct)))

        # Přidání výsledků do polí pro snímky
        method_1_seg_values.append(method_1)
        method_2_seg_values.append(method_2)
        method_3_seg_values.append(method_3)
        method_4_seg_values.append(method_4)

    # Čtení dalšího snímku
    last_image = rgb
    success, image = vidcap.read()
    count += 1

vidcap.release()

plt.subplot(2, 2, 1)
enums = list(enumerate(method_1_seg_values))
t = [x[0] for x in enums]
vec = [x[1] for x in enums]
plt.title("Rozdíl sum")
plt.axvline(x=208, linewidth=2, color='r')
plt.axvline(x=268, linewidth=2, color='r')
plt.plot(t, vec, linewidth=2, color='b')
plt.axis([min(t), max(t), min(vec), max(vec)])

plt.subplot(2, 2, 2)
enums = list(enumerate(method_2_seg_values))
t = [x[0] for x in enums]
vec = [x[1] for x in enums]
plt.title("Suma rozdílů")
plt.axvline(x=208, linewidth=2, color='r')
plt.axvline(x=268, linewidth=2, color='r')
plt.plot(t, vec, linewidth=2, color='b')
plt.axis([min(t), max(t), min(vec), max(vec)])

plt.subplot(2, 2, 3)
enums = list(enumerate(method_3_seg_values))
t = [x[0] for x in enums]
vec = [x[1] for x in enums]
plt.title("Histogramová metoda")
plt.axvline(x=208, linewidth=2, color='r')
plt.axvline(x=268, linewidth=2, color='r')
plt.plot(t, vec, linewidth=2, color='b')
plt.axis([min(t), max(t), min(vec), max(vec)])

plt.subplot(2, 2, 4)
enums = list(enumerate(method_4_seg_values))
t = [x[0] for x in enums]
vec = [x[1] for x in enums]
plt.title("DCT Metoda")
plt.axvline(x=208, linewidth=2, color='r')
plt.axvline(x=268, linewidth=2, color='r')
plt.plot(t, vec, linewidth=2, color='b')
plt.axis([min(t), max(t), min(vec), max(vec)])

plt.show()

fig = plt.figure()
fig.add_axes([0, 0, 1, 1], frameon=False, xticks=[], yticks=[])
cap = cv2.VideoCapture('./data/cv08_video.mp4')
NFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

enums = list(enumerate(method_1_seg_values))
t = [x[0] for x in enums]
vec = [x[1] for x in enums]

for i in range(1, NFrames):
    ret, bgr = cap.read()
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    fig.clear()

    plt.axvline(x=208, linewidth=2, color='r')
    plt.axvline(x=268, linewidth=2, color='r')
    plt.plot(t, vec, linewidth=2, color='b')
    l = plt.axvline(x=i, linewidth=2, color='g')
    plt.axis([min(t), max(t), min(vec), max(vec)])

    plt.imshow(rgb, aspect='auto', extent = [min(t), max(t), min(vec), max(vec)])
    plt.show(block=False)
    plt.pause(0.001)

plt.show()