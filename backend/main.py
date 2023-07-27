from backend.api_connector import APIConnector
from backend.agent_utils import AgentUtils
from backend.agent_build import AgentBuilder
from langchain.agents import Tool
import yaml
from langchain.callbacks import get_openai_callback

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

    def run(self,text,show_token=True):
        """
         Agent process

         Args:
             text (str): User input, which in the case of this agent should be the citations text of the paper.

         Returns:
             str: complete analysis results including citation text and its corresponding conference information.
        """

        with open('backend/templates.yaml', 'r', encoding='utf-8') as file:
            templates = yaml.safe_load(file)

        base_templates = templates['base_template']


        agent_executor = AgentBuilder.build_agent(tools=Agent.tools, template=base_templates, llm=Agent.llm, verbose=True)

        with get_openai_callback() as cb:
            response = agent_executor.run(text)
            total_tokens = f"Total Tokens: {cb.total_tokens}"
            total_cost = f"Total Cost (USD): ${cb.total_cost}"

        if show_token:
            response += f"\n{total_tokens}\n{total_cost}"

        return response