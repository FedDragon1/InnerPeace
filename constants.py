import pathlib


DATASET_PATH = pathlib.Path("./emotion_dataset")

INDEX_TO_EMOTION = ["angry", "happy", "sad", "surprise", "neutral"]
EMOTION_TO_INDEX = {"angry": 0, "happy":1 , "sad": 2, "surprise": 3, "neutral": 4}

with open("./frontend/index.html") as f:
    INDEX_HTML = f.read()


def get_representation(guess):
    return {
        emotion: possibility for emotion, possibility in zip(INDEX_TO_EMOTION, guess)
    }
