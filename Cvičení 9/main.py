from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt

def pca(image):
    depth = image.shape[2]
    vectors = []

    # Převod kanálů na řádkové vektory
    for channel in range(depth):
        vectors.append(image[:,:,channel].flatten())

    # Výpočet středního vektoru
    # np.add.reduce(vectors) sečte vektory v poli vectors po prvcích
    effective_vector = np.add.reduce(vectors) / depth
    # Odchylky vektorů od středního vektoru
    std_deviation = np.array([np.subtract(x, effective_vector) for x in vectors])
    # Kovarianční matice
    covariance = np.cov(std_deviation)
    # Výpočet vlastních čísel a vlastních vektorů
    eigenvalues, eigenvectors = np.linalg.eig(covariance)
    # Seřazení vlastních čísel
    sorted_indexes = np.argsort(eigenvalues)

    eigvecs = eigenvectors[:,sorted_indexes]
    eigenspace = np.matmul(eigvecs, std_deviation)

    # Reálně si myslim, že ty vlastní vektory musí bejt nečim vynásobený, to jinak nedává smysl
    return np.array([np.add(v, effective_vector) for v in eigenspace])

def main():
    image = cv2.imread(Path("data/Cv09_obr.bmp").as_posix())
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    width = image.shape[0]
    height = image.shape[1]

    result = pca(image)

    print(result, result.shape)
    plt.figure("Komponenty PCA")
    plt.subplot(2, 2, 1)
    plt.title("Původní obrázek")
    plt.imshow(image)

    plt.subplot(2, 2, 2)
    plt.title("První hlavní komponenta")
    plt.imshow(np.reshape(result[0], (width, height)), cmap="gray")
    
    plt.subplot(2, 2, 3)
    plt.title("Druhá hlavní komponenta")
    plt.imshow(np.reshape(result[1], (width, height)), cmap="gray")

    plt.subplot(2, 2, 4)
    plt.title("Třetí hlavní komponenta")
    plt.imshow(np.reshape(result[2], (width, height)), cmap="gray")

    plt.show(block=False)

    plt.figure("Porovnání")
    plt.subplot(2, 2, 1)
    plt.title("Výsledek PCA")
    plt.imshow(np.reshape(result[0], (width, height)), cmap="gray")
    
    plt.subplot(2, 2, 2)
    plt.title("Výsledek RGB2GRAY")
    plt.imshow(cv2.cvtColor(image.copy(), cv2.COLOR_RGB2GRAY), cmap="gray")

    plt.subplot(2,2,3)
    plt.title("Histogram PCA")
    plt.hist(result[0], bins=256)

    plt.subplot(2,2,4)
    plt.title("Histogram RGB2GRAY")
    plt.hist(cv2.cvtColor(image.copy(), cv2.COLOR_RGB2GRAY).ravel(), bins=256)

    plt.show()
    


if __name__ == "__main__":
    main()