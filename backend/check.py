import yaml, os
from langchain import PromptTemplate,LLMChain
from backend.agent_utils import AgentUtils
from backend.api_connector import APIConnector

model = 'gpt-4'
connector = APIConnector(model_name=model)
llm = connector.llm
client = connector.client
utils = AgentUtils(llm=llm, client=client)


def check_metadata(filename):
    """
    Check the metadata according to the Qid in the output result to prevent GPT from making mistakes when summarizing the answer

    Args:
        filename (str): output file.

    """

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as test_data:
            test_data = yaml.safe_load(test_data)
    else:
        test_data = []

    for i in range(0, len(test_data)):
        if test_data[i]['Conference Info']['Conference Qid'] is not None:
            if '"' in test_data[i]['Conference Info']['Conference Qid']:
                test_data[i]['Conference Info']['Conference Qid'] = test_data[i]['Conference Info']['Conference Qid'].strip('"')

            query_result = utils.qid_query(test_data[i]['Conference Info']['Conference Qid'])

            test_data[i]['Conference Info']['Conference startDate'] = query_result[0]['StartDate']
            test_data[i]['Conference Info']['Conference endDate'] = query_result[0]['EndDate']
            test_data[i]['Conference Info']['Conference location'] = query_result[0]['Location']
            test_data[i]['Conference Info']['Conference officialWebsite'] = query_result[0]['OfficialWebsite']

    with open(filename, 'w', encoding="utf-8") as file:
        yaml.dump(test_data, file, default_flow_style=False)

def check_match(filename):
    """
        Send the output metadata and the original citation to GPT to determine whether it really matches.

        Args:
            filename (str): output file.

        Returns:
            The re-judgment result of GPT.

    """

    template = os.path.join(os.path.dirname(__file__), 'templates.yaml').replace("\\", "/")
    with open(template, 'r', encoding='utf-8') as file:
        templates = yaml.safe_load(file)

    check_template = templates['check_template']

    llm_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(check_template)
    )

    input_list = []

    with open(filename, "r", encoding="utf-8") as test_data:
        test_data = yaml.safe_load(test_data)

    for i in range(0, len(test_data)):
        if test_data[i]['Conference Info']['Conference Qid'] is not None:
            citation_text = test_data[i]['Citation text']
            conferneceTitle_in_citation = test_data[i]['Conference Info']['Conference title']
            text1 = "Text1.The original citation text:" + citation_text + " The conference in this citation:" + conferneceTitle_in_citation

            query_result = utils.qid_query(test_data[i]['Conference Info']['Conference Qid'])
            title = query_result[0]['Title']
            startDate = query_result[0]['StartDate']
            endDate = query_result[0]['EndDate']
            text2 = " | Text2.Matched possible conference metadata:" + ' Title:' + title + ';StartDate:' + startDate + ';EndDate:' + endDate

            megerd = text1 + text2

            input_list.append({"infomation": megerd})

    return llm_chain.apply(input_list)

