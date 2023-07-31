import os
import time
import ruamel.yaml as yaml
from backend.main import Agent

def run_tests():
    test_data_file = os.path.join(os.path.dirname(__file__), 'testText.yaml').replace("\\", "/")
    output_file = "test_output.yaml"
    agent = Agent()

    with open(test_data_file, "r", encoding="utf-8") as test_data:
        test_data = yaml.load(test_data)

    results = {}

    for entry in test_data:
        name = entry['name']
        text = entry['text']

        start_time = time.time()
        output = Agent.run(agent, text, show_token=True)
        end_time = time.time()

        results[name] = {
            'run_time': str(end_time - start_time) + ' second',
            'result': output
        }

    with open(output_file, "w", encoding="utf-8") as output_file:
        yaml.dump(results, output_file, default_style="|", default_flow_style=False, encoding="utf-8")

if __name__ == "__main__":
    run_tests()