import yaml


def organize_data(file):
    with open(file, 'r', encoding="utf-8") as r:
        result = yaml.safe_load(r)
        for i in range(len(result)):
            for n in result[i]['Conference Info']:
                if result[i]['Conference Info'][n] is not None and '"' in result[i]['Conference Info'][n]:
                    result[i]['Conference Info'][n] = result[i]['Conference Info'][n].strip('"')

    with open(file, 'w', encoding="utf-8") as w:
        yaml.dump(result, w)

def proofread_result(outputfile, profreadfile):

    with open(outputfile, 'r', encoding="utf-8") as r:
        output = yaml.safe_load(r)
    with open(profreadfile, 'r', encoding="utf-8") as r:
        profread = yaml.safe_load(r)

    errors = 0

    for i in range(0, len(profread)):
        profreadCitation = profread[i]['Citation text']
        found_citation = False
        for n in range(0, len(output)):
            if profreadCitation in output[n]['Citation text']:
                found_citation = True
                if output[n]['Conference Info']['Conference Qid'] != profread[i]['Conference Info']['Conference Qid']:
                    errors += 1

                break
        if not found_citation:
            errors += 1

    print(errors)
    return errors

if __name__ == '__main__':
    organize_data('result_all.yaml')
    organize_data('result_all_after_check.yaml')
    organize_data('result_all_gpt3.5.yaml')
    organize_data('result_all_after_check_gpt3.5.yaml')

    proofread_result('result_all.yaml','proofreadText.yaml')
    proofread_result('result_all_after_check.yaml','proofreadText.yaml')
    proofread_result('result_all_gpt3.5.yaml','proofreadText.yaml')
    proofread_result('result_all_after_check_gpt3.5.yaml','proofreadText.yaml')