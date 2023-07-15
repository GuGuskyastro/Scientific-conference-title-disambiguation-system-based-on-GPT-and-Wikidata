import unittest
from backend.main import run


class AgentTest(unittest.TestCase):
    def test_run(self):
        text = "Jonathan Berant, Andrew Chou, Roy Frostig, and Percy Liang. 2013. Semantic parsing on Freebase from question-answer pairs. In Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing, pages 1533–1544, Seattle, Washington, USA."
        result = run(text)

        self.assertIn("Q109527338", result)
        self.assertIn("https://aclanthology.org/events/emnlp-2013", result)

if __name__ == '__main__':
    unittest.main()

