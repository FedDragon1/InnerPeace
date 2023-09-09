import os
import pathlib
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from constants import *
import tqdm


def image_to_csv(image_path):
    image = Image.open(image_path)
    # image.mode == 'L"
    arr = np.array(image)
    # plt.imshow(arr, cmap='gray')
    # plt.show()
    return ",".join(str(x) for x in arr.flatten())


def images_to_csv(folder):
    with open(DATASET_PATH / f"{folder}.csv", "w") as file:
        for emotion in tqdm.tqdm(list((DATASET_PATH / folder).iterdir()), desc=f"{folder}"):
            code = EMOTION_TO_INDEX[emotion.name]
            for image_path in tqdm.tqdm(list(emotion.iterdir()), desc=f"image"):
                csv_line = image_to_csv(image_path)
                csv_line = f"{code},{csv_line}\n"
                file.write(csv_line)


def main():
    images_to_csv("test")
    images_to_csv("train")


if __name__ == "__main__":
    main()
