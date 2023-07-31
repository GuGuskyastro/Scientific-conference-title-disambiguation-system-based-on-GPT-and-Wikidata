import unittest
from backend.main import Agent
from backend.agent_utils import AgentUtils
from backend.api_connector import APIConnector

class AgentTest(unittest.TestCase):
    """
     Test if the functions used by the Agent tool and Agent are working correctly.

    """
    
    connector = APIConnector()
    utils = AgentUtils(llm=connector.llm, client=connector.client)
    agent = Agent()

    def test_extraction(self):
        """
            Conference information should be extracted correctly.

        """

        text = "Jonathan Berant, Andrew Chou, Roy Frostig, and Percy Liang. 2013. Semantic parsing on Freebase from question-answer pairs. In Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing, pages 1533–1544, Seattle, Washington, USA."
        result = AgentUtils.extraction(AgentTest.utils, text)
        self.assertIn('Conference short name: EMNLP 2013' , result)


    def test_weaviate(self):
        """
         Should judged that the conference is included in the weaviateVS.

        """

        text = "Conference on Empirical Methods in Natural Language Processing 2013"
        result = AgentUtils.weaviate_query_input(AgentTest.utils, text)
        self.assertIn("is stored in the Database", result)


    def test_run(self):
        """
            Agent should give the correct metadata for the conference mentioned in the text.

        """
        text = "Jonathan Berant, Andrew Chou, Roy Frostig, and Percy Liang. 2013. Semantic parsing on Freebase from question-answer pairs. In Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing, pages 1533–1544, Seattle, Washington, USA."
        result = Agent.run(AgentTest.agent,text)

        self.assertIn("Q109527338", result)
        self.assertIn("https://aclanthology.org/events/emnlp-2013", result)


if __name__ == '__main__':
    unittest.main()

