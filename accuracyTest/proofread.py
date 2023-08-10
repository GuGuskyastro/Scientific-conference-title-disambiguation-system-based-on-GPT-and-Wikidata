from backend.result_to_yaml import processResult
import yaml
import os

def process_LLM_Result(result_file,output_file):
    """
    Process the previous natural language test results into computer-readable yaml form

    Args:
        result_file (str): The yaml file need to be processed.
        output_file (str): output yaml filename

    """
    structured_result = []
    with open(result_file,'r',encoding="utf-8") as r:
        test_output = yaml.safe_load(r)
        for i in test_output:
            processResult(test_output[i]['result'])
            with open('result.yaml', 'r', encoding="utf-8") as r2:
                result = yaml.safe_load(r2)
                structured_result.append(result)

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(structured_result,f)

    os.remove('result.yaml')

def organize_data(file):
    """
        The output of GPT may use different natural language words for " ", replace these as null values in yaml.
        Eliminate some results which hvae extra quotes

        Args:
            file (str): The yaml file need to be processed.

    """

    not_exist = ['Not available','Not found in the database','Not applicable','Not stored in the database']

    with open(file, 'r', encoding="utf-8") as r:
        result = yaml.safe_load(r)
        for i in range(len(result)):
            for n in range(len(result[i])):
                for m in result[i][n]['Conference Info']:
                    if result[i][n]['Conference Info'][m] in not_exist:
                        result[i][n]['Conference Info'][m] = None
                    if result[i][n]['Conference Info'][m] is not None and '"' in result[i][n]['Conference Info'][m]:
                        result[i][n]['Conference Info'][m] = result[i][n]['Conference Info'][m].strip('"')

    with open(file, 'w', encoding="utf-8") as w:
        yaml.dump(result, w)

def proofread_result(outputfile, profreadfile):
    """
        Check the output against the proofread text to see if there are any errors.

        Args:
            outputfile (str): The yaml file need to be proofread.
            profreadfile (str):The yaml file with proofread text.

        Returns:
            List: Number of errors per test group.

    """

    with open(outputfile, 'r', encoding="utf-8") as r:
        output = yaml.safe_load(r)
    with open(profreadfile, 'r', encoding="utf-8") as r:
        profread = yaml.safe_load(r)

    results = []

    for i in range(0, len(profread)):
        errors = 0

        for n in range(0, len(profread[i])):
            profreadCitation = profread[i][n]['Citation text']
            found_citation = False
            for m in range(0, len(output[i])):
                if profreadCitation in output[i][m]['Citation text']:
                    found_citation = True
                    if output[i][m]['Conference Info']['Conference Qid'] != profread[i][n]['Conference Info']['Conference Qid']:
                        errors += 1
                    break
            if not found_citation:
                errors += 1
        results.append(errors)
    return results

if __name__ == '__main__':
    process_LLM_Result('test_output_individually.yaml', 'structured_test_output_individually.yaml')
    process_LLM_Result('test_output_integrate.yaml', 'structured_test_output_integrate.yaml')
    process_LLM_Result('test_output_intergrate_gpt4.yaml', 'structured_test_output_integrate_gpt4.yaml')
    organize_data('structured_test_output_individually.yaml')
    organize_data('structured_test_output_integrate.yaml')
    organize_data('structured_test_output_integrate_gpt4.yaml')
