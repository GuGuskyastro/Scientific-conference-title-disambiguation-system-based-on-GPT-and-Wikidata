import os
import weaviate
from langchain.chat_models import ChatOpenAI


# Initialize the connection with LLM and Weaviate VS

class APIConnector:
    def __init__(self):
        # OpenAI API key
        os.environ['OPENAI_API_KEY'] = ''

        # Weaviate client
        self.client = weaviate.Client(
            url="",
            auth_client_secret=weaviate.AuthApiKey(api_key=""),
            additional_headers={
                "X-HuggingFace-Api-Key": ""
            }
        )

        # OpenAI LLM
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
