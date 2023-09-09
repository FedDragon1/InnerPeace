import pathlib


DATASET_PATH = pathlib.Path("./emotion_dataset")

INDEX_TO_EMOTION = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]
EMOTION_TO_INDEX = {"angry": 0, "disgust": 1, "fear": 2, "happy": 3, "neutral": 4, "sad": 5, "surprise": 6}

with open("./frontend/index.html") as f:
    INDEX_HTML = f.read()
