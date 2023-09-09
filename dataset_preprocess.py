import numpy as np
from PIL import Image
import tqdm

from constants import *


def image_to_csv(image_path):
    image = Image.open(image_path)
    # image.mode == 'L", size = (48, 48)
    arr = np.array(image)
    # plt.imshow(arr, cmap='gray')
    # plt.show()
    return ",".join(str(x) for x in arr.flatten())


def get_heading():
    return "emotion," + ",".join(str(i) for i in range(48 ** 2)) + '\n'


def images_to_csv(folder):
    with open(DATASET_PATH / f"{folder}.csv", "w") as file:
        file.write(get_heading())
        for emotion in tqdm.tqdm(list((DATASET_PATH / folder).iterdir()), desc=f"{folder}"):
            code = EMOTION_TO_INDEX[emotion.name]
            for image_path in tqdm.tqdm(list(emotion.iterdir()), desc=f"image"):
                csv_line = image_to_csv(image_path)
                csv_line = f"{code},{csv_line}\n"
                file.write(csv_line)


def dataset_size():
    # test
    test = sum(len(list(emotion.iterdir())) for emotion in (DATASET_PATH / "test").iterdir())
    # train
    train = sum(len(list(emotion.iterdir())) for emotion in (DATASET_PATH / "train").iterdir())

    print(f"{test=}")
    print(f"{train=}")


def main():
    images_to_csv("test")
    images_to_csv("train")


if __name__ == "__main__":
    main()
    # dataset_size()
