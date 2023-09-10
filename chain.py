import json
import os

import keras
import weaviate
import numpy as np
from langchain import PromptTemplate

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

openai = OpenAI(temperature=0.2, openai_api_key=os.environ.get("OPENAI_API"))

prompt = PromptTemplate.from_template("""You are now a data analysis model for a senior psychologist called inner-peace. You have undergone extensive training in psychology, human behavior, and emotional analysis. In addition to text input, you can also receive and interpret facial expression data from both users and psychologists. Furthermore, you have access to our previous conversation history and your past responses to provide context (up to 5 message). We will provide you with the following information:

Text content (e.g., what the user or psychologist said).
Facial expression descriptions related to the text 
Previous conversation history and your past responses.
Note, I will give you the percentage for each of these seven expressions: ["angry", "happy", "neutral", "sad", "surprise"]

Based on this information and our past interactions, you will provide me with a deep emotional and psychological analysis, helping me understand why someone might have a specific expression when saying something, and the possible psychological reasons behind it.

For example:
Input:
Text content: I've been feeling tired lately.
Facial expression: sad
Previous conversation: {{"user": "I've been stressed at work.", "inner-peace": "It's important to take breaks and manage stress."}}

Output:
This person might be experiencing fatigue or emotional suppression. Their facial expression shows a sense of despondency and powerlessness, which might be due to long working hours, emotional stress, or other pressures in life. Considering the previous conversation, work-related stress could be a contributing factor.

Important: Only reply the output analysis, don't say anything extra throughout this session. Reply in the json format only. Do not include text of Output

Question:
Text content: {text_content}
Facial expression: {facial_expression}
Previous conversation: {history}
""")


global_query_count = 0      # for every 3 queries, ask weaviate once to avoid heavy openai api usage


def emotion_detection(image_array):
    pred = model.predict(image_array)[0]
    # model has a tendency to classify angry. tweak the data a bit to get more accurate result
    if np.argmax(pred) == 0 and np.all(pred[1:] == 0):
        pred[0] = 0.3
        pred[EMOTION_TO_INDEX["neutral"]] += 0.5 + np.random.random()
        pred[EMOTION_TO_INDEX["happy"]] += 0.5 + np.random.random()

    return ", ".join(f"{emotion}: {value:2f}" for emotion, value in zip(INDEX_TO_EMOTION, pred)), INDEX_TO_EMOTION[np.argmax(pred)]


def process_history(history):
    return repr({roll: chat for roll, chat in history})


def get_chat_analysis(chat, emotion, history):
    global global_query_count
    global_query_count += 1
    if global_query_count % 3 == 0:
        ret = weaviate_query(emotion, chat)
        print(ret)
        return ret

    p = prompt.format(
        text_content=chat,
        facial_expression=emotion,
        history=process_history(history)
    )
    p = openai.predict(p).split('\n')[-1]
    try:
        p = json.loads(p)["analyze"]
    except Exception:
        ...
    p = str(p)
    store_in_weaviate(chat, p, emotion)
    return p


def store_in_weaviate(user, response, emotion):
    client.batch.configure(batch_size=1)
    with client.batch as batch:
        batch.add_data_object({
            "user": user,
            "response": response,
            "emotion": emotion
        }, "InnerPeace")


def weaviate_query(emotion, user):
    resp = client.query.get(
        "InnerPeace", ["response"]
    ).with_near_text(
        {"concepts": [emotion, user]}
    ).with_limit(1).do()

    return resp["data"]["Get"]["InnerPeace"][0]["response"]



if __name__ == '__main__':
    response = client.query.get(
        "InnerPeace", ["response"]
    ).with_near_text(
        {"concepts": ["sad", "i'm so broke"]}
    ).with_limit(1).do()

    print(json.dumps(response, indent=4))

    # prompt = prompt.format(
    #         text_content="I'm so broke, i want to suicide",
    #         facial_expression="angry: 0, disgust: 0, fear: 0, happy: 0, neutral: 0, sad: 0.8, surprise: 0",
    #         history='{"user": "I\'ve been stressed at work.", "therapist": "It\'s important to take breaks and manage stress."}'
    #     )
    # print(prompt)
    # openai = OpenAI(openai_api_key=os.environ.get("OPENAI_API"))
    # a = openai(
    #     prompt
    # )
    # print(a)
