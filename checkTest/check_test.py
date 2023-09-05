import os
import ruamel.yaml as yaml
from backend.main import Agent
from backend.check import check_metadata,check_match

def run_tests(model_name,use_integrate_agent,outputfile,outputfile_after_check):

    test_data_file = os.path.join(os.path.dirname(__file__), 'testText.yaml').replace("\\", "/")
    agent = Agent(model_name=model_name)

    with open(outputfile, 'w', encoding="utf-8") as result_all_file:
        result_all_file.write("")

    with open(outputfile_after_check, 'w', encoding="utf-8") as result_all_after_check_file:
        result_all_after_check_file.write("")


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
        match_result = check_match('result.yaml')

        check_list = []

        for i in range(0, len(result)):
            if result[i]['Conference Info']['Conference Qid'] is not None:
                check_list.append(result[i]['Conference Info']['Conference Qid'])

        for i in range(0,len(check_list)):
            if match_result[i]['text'] == 'Wrong':
                for n in range(0,len(result)):
                    if result[n]['Conference Info']['Conference Qid'] == check_list[i]:
                        result[n]['Conference Info']['Conference Qid'] = None
                        result[n]['Conference Info']['Conference startDate'] = None
                        result[n]['Conference Info']['Conference endDate'] = None
                        result[n]['Conference Info']['Conference location'] = None
                        result[n]['Conference Info']['Conference officialWebsite'] = None

        with open(outputfile_after_check, 'a', encoding="utf-8") as result_all_after_check_file:
            yaml.dump(result, result_all_after_check_file)

if __name__ == '__main__':
    output = 'result_all.yaml'
    output_check = 'result_all_after.yaml'
    output_gpt3 = 'result_all_gpt3.5.yaml'
    output_check_gpt3 = 'result_all_after_check_gpt3.5.yaml'

    run_tests('gpt-3.5-turbo', use_integrate_agent=True, outputfile=output, outputfile_after_check=output_check)
    run_tests('gpt-3.5-turbo',use_integrate_agent=True, outputfile = output_gpt3 ,outputfile_after_check=output_check_gpt3)