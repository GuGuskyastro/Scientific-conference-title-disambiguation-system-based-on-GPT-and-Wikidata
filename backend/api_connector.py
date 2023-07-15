import os
import weaviate
from langchain.chat_models import ChatOpenAI


# Initialize the connection with LLM and Weaviate VS

class APIConnector:
    def __init__(self):
        # OpenAI API key
        os.environ['OPENAI_API_KEY'] = '${{ secrets.OPENAI_API_KEY }}'
        weaviate_url = os.environ.get('WEAVIATE_URL')
        weaviate_api_key = os.environ.get('WEAVIATE_API_KEY')
        huggingface_api_key = os.environ.get('HUGGINGFACE_API_KEY')

        # Weaviate client
        self.client = weaviate.Client(
            url=weaviate_url,
            auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_api_key),
            additional_headers={
                "X-HuggingFace-Api-Key": huggingface_api_key
            }
        )

        # OpenAI LLM
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
