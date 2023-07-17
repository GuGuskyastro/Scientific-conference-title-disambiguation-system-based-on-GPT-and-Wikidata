import re
import json
import requests
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# This file contains methods that the LLM model will use when invoking the Agent tools


class AgentUtils:
    def __init__(self, llm, client):
        self.llm = llm
        self.client = client

    def extraction(self, input):
        """
         Use Langchain chain to let LLM parse the scientific conference information from the input text.

         Args:
             input (str): The extracted object, in this project usually the reference part a the paper

         Returns:
             str: The extraction results include the original citations, possible conference titles and short name.
         """

        fact_extraction_prompt = PromptTemplate(
            input_variables=["text_input"],
            template='''The following text entry is the citations section of a paper, which may contain one or more citations. 
            Some of these citations may contain information for scientific conference, you need extract conference title and short name. give the answer in the following format for each citation:

            properties: {{
            Citation text: {{"type": "string"}},
            Conference title: {{"type": "string"}},
            Conference short name: {{"type": "string"}}}}

            When extracting, do not appear "Proceedings of" in the Conference title. A simple example:Saleem, M., Mehmood, Q., Ngonga Ngomo, A.C.: FEASIBLE: A Feature-Based SPARQL Benchmark Generation Framework. In: Proceedings of 14th International Semantic Web Conference. pp. 52–69. Springer (2015),
            the Conference title for this citation then should be like International Semantic Web Conference 2015. The short name then is ISWC 2015. The year must be added to the title.
            References that do not mention scientific conferences can just use empty characters in the title and short name.
            Only use the information in the text to extract. If all citations do not have scientific meetings, tell the user that your input does not have any scientific meetings.

            text:\n\n {text_input}'''
        )
        fact_extraction_chain = LLMChain(llm=self.llm, prompt=fact_extraction_prompt)
        facts = fact_extraction_chain.run(input)
        return facts


    def qid_query(self, qid):
        """
         Query the detailed Wikidata metadata of the conference according to the extracted QID.

         Args:
             qid (str): Extracted QID

         Returns:
             str: Corresponding metadata in Wikidata, including title, short name, start/end date, location and conference website.
        """

        query = """
        SELECT ?QID ?conferenceLabel ?startDate ?endDate ?locationLabel ?officialWebsite
        WHERE {
          VALUES ?conference {wd:""" + qid + """}
          OPTIONAL { ?conference wdt:P580 ?startDate. }
          OPTIONAL { ?conference wdt:P582 ?endDate. }
          OPTIONAL { ?conference wdt:P276 ?location. }
          OPTIONAL { ?conference wdt:P856 ?officialWebsite. }
          BIND(REPLACE(STR(?conference), ".*/(Q[0-9]+)$", "$1") AS ?QID)

          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        """

        url = "https://query.wikidata.org/sparql"
        params = {
            "query": query,
            "format": "json"
        }
        response = requests.get(url, params=params)
        data = response.json()
        results = data.get("results", {}).get("bindings", [])

        conference_metadata = []
        for result in results:
            qid = result["QID"]["value"]
            title = result["conferenceLabel"]["value"]
            startDate = re.findall(r'\d{4}-\d{2}-\d{2}', result["startDate"]["value"])[0]
            endDate = re.findall(r'\d{4}-\d{2}-\d{2}', result["endDate"]["value"])[0]
            location = result["locationLabel"]["value"]
            officialWebsite = result["officialWebsite"]["value"]

            conference = {
                "Qid": qid,
                "Title": title,
                "StartDate": startDate,
                "EndDate": endDate,
                "Location": location,
                "OfficialWebsite": officialWebsite
            }
            conference_metadata.append(conference)
        return conference_metadata


    def weaviate_query_input(self, title):
        """
         Use Langchain chain to let LLM query whether the input conference is stored in the Weaviate VS, and if so, obtain detailed information based on QID.

         Args:
             title (str): Conference title for query in Weaviate VS.

         Returns:
             str: The query result (whether there is a matching conference in the database), and if so, the detailed metadata in Wikidata.
        """

        response = (
            self.client.query
            .get("Conference", ["qid", "title", 'shortName'])
            .with_limit(5)
            .with_near_text({
                "concepts": title
            })
            .do()
        )
        result = json.dumps(response)
        merged = "extrationTitle:" + title + '/queryResult:' + result
        query_Input_prompt = PromptTemplate(
            input_variables=["text_input"],
            template=''' I will give you two texts, one is the conference information I extracted, and the other is the query result of my database. Analyze whether the conference I extracted is also in the query result according to the queried short name and title, and answer me in template below:
            The {{conferen title}} is/is not stored in the Database.(If stored then add)Its QID is {{QID}}.

            Two text:{text_input}'''
        )
        weaviateQuery_chain = LLMChain(llm=self.llm, prompt=query_Input_prompt)
        analysis_result = weaviateQuery_chain.run(merged)
        qidQuery_result_str = "[]"
        qid_match = re.search(r'Q[0-9]+', analysis_result)  # Assuming QID follows the format Q followed by numbers
        qid = qid_match.group() if qid_match else None

        if qid:
            qidQuery_result = self.qid_query(qid)  # Call qid_query method with the extracted QID
            qidQuery_result_str = json.dumps(qidQuery_result)

        return analysis_result + "Detailed metadata " + qidQuery_result_str
