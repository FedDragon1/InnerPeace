import numpy as np
import tensorflow as tf
import keras

from PIL import Image

model = keras.models.load_model("cnn")

image = Image.open(r"D:\JetBrains\PycharmProjects\InnerPeace\emotion_dataset\train\angry\Training_3908.jpg")

arr = np.array(image)[None, :].reshape(1, 48, 48, 1)

pred = model.predict(arr)

print(pred)
