import json
import os

import weaviate

from dotenv import load_dotenv

load_dotenv()

client = weaviate.Client(
    url="https://inner-peace-sandbox-x3xxx6sb.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key=os.environ.get("WEAVIATE_API")),
    additional_headers={
        "X-OpenAI-Api-Key": os.environ.get("OPENAI_API")
    }
)


def create_obj():
    client.schema.delete_class("InnerPeace")
    class_obj = {
        "class": "InnerPeace",
        "description": "Mental Health Investigator",
        "properties": [
            {
                "dataType": ["text"],
                "description": "What user says",
                "name": "user",
            },
            {
                "dataType": ["text"],
                "description": "The response",
                "name": "response",
            },
            {
                "dataType": ["text"],
                "description": "User's emotion",
                "name": "emotion",
            },
        ],
        "vectorizer": "text2vec-openai",
        "moduleConfig": {
            "text2vec-openai": {
                "vectorizeClassName": True
            }
        }
    }

    client.schema.create_class(class_obj)


def popularize_database():
    with open("sample_data.json", "r") as f:
        prompts = json.load(f)

    client.batch.configure(batch_size=100)
    with client.batch as batch:
        for i, d in enumerate(prompts):
            properties = {
                "user": d["user"],
                "response": d["response"],
                "emotion": d["emotion"],
            }
            batch.add_data_object(properties, "InnerPeace")


def test_database():
    response = (
        client.query
        .get("InnerPeace", ["user", "response", "emotion"])
        .with_near_text({"concepts": ["angry: 0, disgust: 0, fear: 0, happy: 0.7, neutral: 0, sad: 0, surprise: 0.9"]})
        .with_limit(2)
        .do()
    )

    print(json.dumps(response, indent=4))


if __name__ == '__main__':
    create_obj()
    # popularize_database()
    # test_database()
