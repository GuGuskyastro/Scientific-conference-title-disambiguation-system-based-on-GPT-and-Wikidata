import yaml
import json
from backend.main import Agent

agent = Agent(model_name='gpt-3.5-turbo')

with open('testText.yaml', "r", encoding="utf-8") as test_data:
    test_data = yaml.safe_load(test_data)

answer_List = []
for entry in test_data:
    results = {'result':entry['name']}

    for i in entry['text']:
        text = entry['text'][i]

        Agent.generate_result(agent, text, show_token=False, use_integrate_agent=True)

        with open('result.yaml', "r", encoding="utf-8") as data:
            result = yaml.safe_load(data)

        ablation_class = i
        qid = result[0]['Conference Info']['Conference Qid']
        results.update({i:qid})

    answer_List.append(results)

with open('output.json', 'w') as json_file:
    json.dump(answer_List, json_file, ensure_ascii=False, indent=4)


