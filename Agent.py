from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import StringPromptTemplate

from langchain.schema import AgentAction, AgentFinish
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from typing import List, Union
import weaviate
import os
import re
import json
import requests

# This file is used to define the Langchain Agent process and required tools

#Your openai api key
os.environ['OPENAI_API_KEY'] = ''

client = weaviate.Client(
        url="https://wikidata-f138wobj.weaviate.network",  # Your weaviate sandbox URL
        auth_client_secret=weaviate.AuthApiKey(api_key=""), # Your weaviate API key
        additional_headers={
            "X-HuggingFace-Api-Key": ""  # Your inference API key
        }
    )

# load openai llm
llm = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0)


# Create extraction prompt template for parsing possible scientific conferences in the input text
def extration(input):
    fact_extraction_prompt = PromptTemplate(
        input_variables=["text_input"],
        template='''The following text entry is the citations section of a paper, which may contain one or more citations. 
        Some of these citations may contain information for scientific conference, you need extract conference title and short name. give the answer in the following format for each citation:

        properties: {{
        Citation text: {{"type": "string"}},
        Conference title: {{"type": "string"}},
        Conference short name: {{"type": "string"}}}}

        When extracting, do not appear "Proceedings of" in the Conference title. A simple example:Saleem, M., Mehmood, Q., Ngonga Ngomo, A.C.: FEASIBLE: A Feature-Based SPARQL Benchmark Generation Framework. In: Proceedings of International Semantic Web Conference. pp. 52–69. Springer (2015),
        the Conference title for this citation then should be like International Semantic Web Conference 2015. The short name then is ISWC 2015.
        References that do not mention scientific conferences can just use empty characters in the title and short name
        Only use the information in the text to extract. If all citations do not have scientific meetings, tell the user that your input does not have any scientific meetings

        text:\n\n {text_input}'''
    )
    # 定义chain
    fact_extraction_chain = LLMChain(llm=llm, prompt=fact_extraction_prompt)
    facts = fact_extraction_chain.run(input)
    return facts


def qidQuery(qid):
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


def weaviateQueryInput(title):
    response = (
        client.query
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
        template=''' I will give you two texts, one is the meeting information I extracted, and the other is the result of my query. Analyze whether the input conference is included in the result according to the title and shortName in query result, and answer me in template below:
        The {{conferen title}} is/is not stored in the Database.(If stored then add)Its QID is {{QID}}.

        Two text:{text_input}'''
    )
    weaviateQuery_chain = LLMChain(llm=llm, prompt=query_Input_prompt)
    analysis_result = weaviateQuery_chain.run(merged)
    qidQuery_result_str = "[]"
    qid_match = re.search(r'Q[0-9]+', analysis_result)  # Assuming QID follows the format Q followed by numbers
    qid = qid_match.group() if qid_match else None

    if qid:
        qidQuery_result = qidQuery(qid)  # Call qidQuery method with the extracted QID
        qidQuery_result_str = json.dumps(qidQuery_result)

    return analysis_result + "Detailed metadata " + qidQuery_result_str


tools = [
    Tool(
        name="Extraction",
        func=extration,
        description="used for extracting conference information from references"
    ),
    Tool(
        name="Query",
        func=weaviateQueryInput,
        description="Supports one conference title input at a time. Used for querying conference information from the database,and give infomation about metadata as result"
    )
]

# Set up the base template for Agent
template = """
You are now a text parsing assistant, and you receive a text of citations from a paper. Strictly follow the following workflow to complete the task:
1. Use the Extraction tool to parse the user input, that is, the user input text is used as the input of the tool. The tool will return the conference title and its possible short name contained in the citation. If the results of this step show that there is no information on any conference, skip the second step.
2. Use the Query tool to query conference title one by one, that is, one of the conference title returned by Extraction tool is used as the input of query tool. No matter what the returned result is, it will not affect you to continue to query the remaining conference titles. Never give short names as input to this tool! Only query titles parsed from user input, never invent new ones yourself! Repeat this step until all conference in step 1 result are judged. 

After operating all steps, summarize the results and give the final answer like:
There are a total of x citations in the input text (which is the user input), of which y contain scientific conference information. Following is extracted meeting information:
properties: {{
        Citation text: {{"type": "string"}},
        (Add following if there is one)
        Conference title: {{"type": "string"}},
        Conference short name: {{"type": "string"}},
        Conference Qid: {{"type": "string"}},
        Conference startDate: {{"type": "string"}},
        Conference endDate: {{"type": "string"}},
        Conference location: {{"type": "string"}}
        Conference officialWebsite: {{"type": "string"}}
        }}

You have access to the following tools:

{tools}

Use the following format:

Question: the input text from user
Thought: Think about what you need to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the tool. 
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)

Thought: I now know the final answer
Final Answer: the final answer according to the previous tips

Text from user: {input}
{agent_scratchpad}"""


# Set up a prompt template
class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in self.tools]
        )
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)


prompt = CustomPromptTemplate(
    template=template,
    tools=tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "intermediate_steps"],
)

class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action: (.*?)[\n]*Action Input:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(
            tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output
        )

output_parser = CustomOutputParser()

tool_names = [tool.name for tool in tools]

llm_chain = LLMChain(llm=llm, prompt=prompt)

agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=output_parser,
    stop=["\nObservation:"],
    allowed_tools=tool_names,
)

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)


# Execute Agent operations
def run2(text):
    return agent_executor.run(text)

