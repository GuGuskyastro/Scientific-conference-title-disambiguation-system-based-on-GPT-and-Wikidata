from backend.api_connector import APIConnector
from backend.agent_utils import AgentUtils
from backend.agent_build import AgentBuilder
from langchain.agents import Tool


class Agent:
    """
     Guide LLM to complete tasks step by step through agent templates and defined tools.

    """

    connector = APIConnector()
    llm = connector.llm
    client = connector.client
    utils = AgentUtils(llm=llm, client=client)

    tools = [
        Tool(
            name="Extraction",
            func=utils.extraction,
            description="used for extracting conference information from references"
        ),
        Tool(
            name="Query",
            func=utils.weaviate_query_input,
            description="Supports one conference title input at a time. Used for querying conference information from the database, and give information about metadata as a result"
        )
    ]

    def run(self,text):
        """
         Agent process

         Args:
             input (str): User input, which in the case of this agent should be the citations text of the paper.

         Returns:
             str: complete analysis results including citation text and its corresponding conference information.
        """

        template = """
        You are now a text parsing assistant, and you receive a text of citations from a paper. Strictly follow the following workflow to complete the task:
        For each citation in the input text,
        1. Use the Extraction tool to parse the user input, that is, the user input text is used as the input of the tool. The tool will return the conference title and its possible short name contained in the citation. If the results of this step show that there is no information on any conference, skip the second step.
        2. Use the Query tool to query conference title, that is, the title returned by Extraction tool is used as the input of query tool. 
        
        After operating all citations, summarize the results and give the final answer like:
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
        Thought: Think about what you need to do.
        Action: the action to take, should be one of [{tool_names}]!
        Action Input: the input to the tool. 
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        
        Thought: I now know the final answer
        Final Answer: the final answer according to the previous tips
        
        Question: {input}
        {agent_scratchpad}
        """

        agent_executor = AgentBuilder.build_agent(tools=Agent.tools, template=template, llm=Agent.llm, verbose=True)
        return agent_executor.run(text)