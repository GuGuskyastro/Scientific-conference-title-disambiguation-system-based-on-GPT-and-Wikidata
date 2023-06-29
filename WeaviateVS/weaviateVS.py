import weaviate
import json

client = weaviate.Client(
    url = "",  # Fill in the weaviate sandbox URL you created
    auth_client_secret=weaviate.AuthApiKey(api_key=""), # API for sandbox
    additional_headers = {
        "X-HuggingFace-Api-Key": ""  # Inference API key, depends on the embedding model you use
    }
)

# ===== add schema =====
class_obj = {
    "class": "Conference",
    "vectorizer": "text2vec-huggingface",  # Can choose different vectorizers according to your needs
    "moduleConfig": {
        "text2vec-huggingface": {
            "model": "sentence-transformers/all-MiniLM-L6-v2",
            "options": {
                "waitForModel": True
            }
        }
    }
}

client.schema.create_class(class_obj)

# ===== import data =====
# Load data

with open(r"conference_data.json","r",encoding="utf-8") as file: # Load the Json file you got
    data = json.load(file)

# Configure a batch process, time to embed the dataset into the vector depend on different vectorizer
with client.batch(
    batch_size=100
) as batch:
    # Batch import
    for i, d in enumerate(data):
        print(f"importing conference: {i+1}")

        # Set properties in VS according to requirements
        properties = {
            "qid": d["Qid"],
            "title": d["Title"],
            "shortName": d["ShortName"],
        }

        client.batch.add_data_object(
            properties,
            "Conference",
        )