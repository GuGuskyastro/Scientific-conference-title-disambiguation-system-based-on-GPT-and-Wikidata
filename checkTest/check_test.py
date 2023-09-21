import os
import ruamel.yaml as yaml
from backend.main import Agent
from backend.check import check_metadata,correction_replace_empty,correction_call_GPT4

def run_tests(model_name,use_integrate_agent,outputfile,outputfile_after_check_c1,outputfile_after_check_c2):

    test_data_file = os.path.join(os.path.dirname(__file__), 'testText.yaml').replace("\\", "/")
    agent = Agent(model_name=model_name)

    with open(outputfile, 'w', encoding="utf-8") as result_all_file:
        result_all_file.write("")

    with open(test_data_file, "r", encoding="utf-8") as test_data:
        test_data = yaml.safe_load(test_data)

    for entry in test_data:
        text = entry['text']

        Agent.generate_result(agent, text, show_token=True,use_integrate_agent = use_integrate_agent)

        with open('result.yaml', "r", encoding="utf-8") as data:
            result = yaml.safe_load(data)

        with open(outputfile, 'a', encoding="utf-8") as result_all_file:
            yaml.dump(result,result_all_file)

        check_metadata('result.yaml')
        correction_replace_empty('result.yaml',outputfile_after_check_c1)
        correction_call_GPT4('result.yaml',outputfile_after_check_c2)

if __name__ == '__main__':
    output = 'result_all.yaml'
    output_c1 = 'result_all_after_correction1.yaml'
    output_c2 = 'result_all_after_correction2.yaml'

    output_gpt3 = 'result_all_gpt3.5.yaml'
    output_c1_gpt3 = 'result_all_after_correction1_gpt3.5.yaml'
    output_c2_gpt3 = 'result_all_after_correction2_gpt3.5.yaml'

    run_tests('gpt-4', use_integrate_agent=True, outputfile=output, outputfile_after_check_c1=output_c1,outputfile_after_check_c2=output_c2)
    run_tests('gpt-3.5-turbo',use_integrate_agent=True, outputfile =output_gpt3, outputfile_after_check_c1=output_c1_gpt3,outputfile_after_check_c2=output_c2_gpt3)