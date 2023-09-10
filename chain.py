import json
import os

import keras
import weaviate
import numpy as np

from constants import *
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.vectorstores.weaviate import Weaviate
from langchain.chains import ChatVectorDBChain


model = keras.models.load_model("cnn")

load_dotenv()

client = weaviate.Client(
    url="https://inner-peace-sandbox-x3xxx6sb.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key=os.environ.get("WEAVIATE_API")),
    additional_headers={
        "X-OpenAI-Api-Key": os.environ.get("OPENAI_API")
    }
)

vectorstore = Weaviate(client, "InnerPeace", "user")

openai = OpenAI(temperature=0.2, openai_api_key=os.environ.get("OPENAI_API"))


qa = ChatVectorDBChain.from_llm(openai, vectorstore)


def emotion_detection(image_array):
    pred = model.predict(image_array)
    return ", ".join(f"{emotion}: {value:2f}" for emotion, value in zip(INDEX_TO_EMOTION, pred))


if __name__ == '__main__':
    response = client.query.get(
        "InnerPeace", ["user", "response", "emotion"]
    ).with_near_text(
        {"concepts": ["sad"]}
    ).with_limit(2).do()

    print(json.dumps(response, indent=4))
