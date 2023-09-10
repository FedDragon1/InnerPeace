import keras
from pillow import PIL
import numpy as np


model = keras.models.load_model("cnn")

image = Image.open(r".\emotion_dataset\test\neutral\PrivateTest_687498.jpg")

arr = np.array(image)[None, :].reshape(1, 48, 48, 1)

pred = model.predict(arr)

print(pred)

