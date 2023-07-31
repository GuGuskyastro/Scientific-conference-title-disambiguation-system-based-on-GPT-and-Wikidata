import ruamel.yaml as yaml

def proofread_results(output_file, proofread_file):
    with open(output_file, "r", encoding="utf-8") as output_data:
        output_data = yaml.safe_load(output_data)

    with open(proofread_file, "r", encoding="utf-8") as proofread_data:
        proofread_data = yaml.safe_load(proofread_data)

    results = {}

    for citation_key, proofread_citation in proofread_data.items():
        if citation_key not in output_data:
            results[citation_key] = "Missing citation in output."
            continue

        output_citation = output_data[citation_key]['result']
        proofread_in_db = proofread_citation.get('conference(in database)', {})
        proofread_not_in_db = proofread_citation.get('conference(not in database)', {})
        proofread_total = proofread_citation.get('text with conference', {})
        errors = []

        # Check if conferences in the database are present in the output
        for conf_key, conf_id in proofread_in_db.items():
            if conf_id not in output_citation:
                errors.append(f"Conference ID {conf_id} not found in the output for {citation_key}.")

        # Check if conferences not in the database are present in the output
        for conf_key, conf_name in proofread_not_in_db.items():
            if conf_name not in output_citation:
                errors.append(f"Conference name '{conf_name}' not found in the output for {citation_key}.")

        # Check the total count of citations with conference information
        if proofread_total not in output_citation:
            errors.append(f"Expected text '{proofread_total}' not found in the output for {citation_key}.")

        if not errors:
            results[citation_key] = "Pass"
        else:
            results[citation_key] = ", ".join(errors)

    with open("proofreading_results.yaml", "w", encoding="utf-8") as result_file:
        yaml.dump(results, result_file, default_style="|", default_flow_style=False, encoding="utf-8")

if __name__ == "__main__":
    output_file = "test_output.yaml"
    proofread_file = "proofreadText.yml"
    proofread_results(output_file, proofread_file)