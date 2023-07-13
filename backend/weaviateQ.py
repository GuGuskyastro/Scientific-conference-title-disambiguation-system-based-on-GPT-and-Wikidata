import weaviate
import json


# Example of a query method in weaviate

client = weaviate.Client(
    url = "",  #
    auth_client_secret=weaviate.AuthApiKey(api_key=""),
    additional_headers = {
        "X-HuggingFace-Api-Key": ""
    }
)

title = ""


response = (
        client.query
            .get("Conference", ["qid", "title", 'shortName'])
            .with_limit(5)
            .with_near_text({
            "concepts": title
        })
            .do()
    )
print(json.dumps(response, indent=4))