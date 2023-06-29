import requests
import json



# This file is used to obtain information of all scientific conferences in wikidata as the input dataset for weaviateVS


# Get QID, label and shortname
query = """
SELECT ?QID ?conferenceLabel ?shortname
WHERE {
  ?conference wdt:P31 wd:Q2020153.
  ?conference wdt:P1813 ?shortname
  BIND(REPLACE(STR(?conference), ".*/(Q[0-9]+)$", "$1") AS ?QID)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
"""


# API
url = "https://query.wikidata.org/sparql"
params = {
    "query": query,
    "format": "json"
}


# send and parse
response = requests.get(url, params=params)
data = response.json()
results = data.get("results", {}).get("bindings", [])


# process result
conference_data = []
for result in results:
    qid = result["QID"]["value"]
    title = result["conferenceLabel"]["value"]
    shortname = result["shortname"]["value"]

    conference = {
        "Qid": qid,
        "Title": title,
        "ShortName": shortname
    }
    conference_data.append(conference)


# Write to JSON
with open("conference_data.json", "w", encoding="utf-8") as file:
    json.dump(conference_data, file, ensure_ascii=False, indent=4)
