import unittest
from backend.main import run
from backend.agent_utils import AgentUtils
from backend.api_connector import APIConnector

class AgentTest(unittest.TestCase):
    connector = APIConnector()
    utils = AgentUtils(llm=connector.llm, client=connector.client)

    def test_extraction(self):
        text = "Jonathan Berant, Andrew Chou, Roy Frostig, and Percy Liang. 2013. Semantic parsing on Freebase from question-answer pairs. In Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing, pages 1533–1544, Seattle, Washington, USA."
        result = AgentUtils.extraction(AgentTest.utils, text)
        self.assertIn('Conference short name: "EMNLP 2013"' , result)


    def test_weaviate(self):

        text = "Conference on Empirical Methods in Natural Language Processing 2013"
        result = AgentUtils.weaviate_query_input(AgentTest.utils, text)
        self.assertIn("The Conference on Empirical Methods in Natural Language Processing 2013 is stored in the Database", result)


    def test_run(self):
        text = "Jonathan Berant, Andrew Chou, Roy Frostig, and Percy Liang. 2013. Semantic parsing on Freebase from question-answer pairs. In Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing, pages 1533–1544, Seattle, Washington, USA."
        result = run(text)

        self.assertIn("Q109527338", result)
        self.assertIn("https://aclanthology.org/events/emnlp-2013", result)


if __name__ == '__main__':
    unittest.main()

