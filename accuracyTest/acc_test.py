import os
import time
import ruamel.yaml as yaml
from backend.main import Agent

def run_tests(output_file,model_name,use_integrate_agent):
    """
     Test the selected Agent model and method.

     Args:
         output_file (str): output filename
         model_name (str): the model name of OpenAI,  can choose gpt-4 and gpt-3.5-turbo.
         use_integrate_agent (bool): deciding which Agent method to use

    """

    test_data_file = os.path.join(os.path.dirname(__file__), 'testText.yaml').replace("\\", "/")
    agent = Agent(model_name=model_name)

    with open(test_data_file, "r", encoding="utf-8") as test_data:
        test_data = yaml.load(test_data)

    results = {}

    for entry in test_data:
        name = entry['name']
        text = entry['text']

        start_time = time.time()
        output = Agent.run(agent, text, show_token=True,use_integrate_agent = use_integrate_agent)
        end_time = time.time()

        results[name] = {
            'run_time': str(end_time - start_time) + ' second',
            'result': output
        }

    with open(output_file, "w", encoding="utf-8") as output_file:
        yaml.dump(results, output_file, default_style="|", default_flow_style=False, encoding="utf-8")

if __name__ == '__main__':
    run_tests('test_output_individually.yaml', 'gpt-3.5-turbo', False)
    run_tests('test_output_integrate.yaml','gpt-3.5-turbo',True)
    run_tests('test_output_integrate_gpt4.yaml', 'gpt-4', True)






