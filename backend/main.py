from backend.api_connector import APIConnector
from backend.agent_utils import AgentUtils
from backend.agent_build import AgentBuilder
from backend.result_to_yaml import processResult
from langchain.agents import Tool
from langchain.callbacks import get_openai_callback
import yaml,os


class Agent:
    """
     Guide LLM to complete tasks step by step through agent templates and defined tools.

    """

    def __init__(self, model_name="gpt-3.5-turbo"):
        self.connector = APIConnector(model_name=model_name)
        self.llm = self.connector.llm
        self.client = self.connector.client
        self.utils = AgentUtils(llm=self.llm, client=self.client)

        self.tools = [
            Tool(
                name="Extraction",
                func=self.utils.extraction,
                description="used for extracting conference information from references"
            ),
            Tool(
                name="Query",
                func=self.utils.weaviate_query_input,
                description="Supports one conference title input at a time. Used for querying conference information from the database, and give information about metadata as a result"
            )
        ]

    def run(self, text, show_token=True, use_integrate_agent=False):
        """
        Agent process

        Args:
            text (str): User input, which in the case of this agent should be the citations text of the paper.
            show_token (bool): Whether to show token and cost information.
            use_integrate_agent (bool): Choose Agent way.

        Returns:
            str: complete analysis results including citation text and its corresponding conference information.
        """

        template = os.path.join(os.path.dirname(__file__), 'templates.yaml').replace("\\", "/")

        with open(template, 'r', encoding='utf-8') as file:
            templates = yaml.safe_load(file)

        base_templates_individually = templates['base_template_individually']
        base_templates_intergrate = templates['base_template_intergrate']

        if use_integrate_agent:
            agent_executor = AgentBuilder.build_agent(tools=self.tools, template=base_templates_intergrate,llm=self.llm, verbose=True)
        else:
            agent_executor = AgentBuilder.build_agent(tools=self.tools, template=base_templates_individually,llm=self.llm, verbose=True)

        with get_openai_callback() as cb:
            response = agent_executor.run(text)
            total_tokens = f"Total Tokens: {cb.total_tokens}"
            total_cost = f"Total Cost (USD): ${cb.total_cost}"

        if show_token:
            response += f"\n{total_tokens}\n{total_cost}"

        return response



    def generate_result(self,text,show_token=True,use_integrate_agent=False):
        """
        Prcess the user input and give the structured data as final result.

        Args:
            text (str): User input, which in the case of this agent should be the citations text of the paper.
            show_token (bool): Whether to show token and cost information.
            use_integrate_agent (bool): Choose Agent way.

        Returns:
            yaml file containing structured GPT result.
        """
        result = Agent.run(self,text,show_token,use_integrate_agent)
        processResult(result)







