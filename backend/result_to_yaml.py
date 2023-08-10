import re
import yaml

def processResult(input_text):
    """
    Convert GPT natural language results into computer-readable structured data

    Args:
        input_text (str): GPT natural language results

    Returns:
        yaml file containing structured GPT result.

    """

    citation_pattern = r"Citation text: (.+?)(?=\n\s*-|\n\s{2,}Conference)"
    citations = re.findall(citation_pattern, input_text, re.DOTALL)

    result = []

    for i in range(len(citations)):

        citation_text = citations[i]
        start_index = input_text.find(citation_text)
        end_index = len(input_text) if i == len(citations) - 1 else input_text.find(citations[i + 1])
        citation_data = input_text[start_index:end_index]

        # Extract attributes using regex
        conference_title = re.search(r"Conference title: (.+)", citation_data)
        conference_short_name = re.search(r"Conference short name: (.+)", citation_data)
        conference_qid = re.search(r"Conference Qid: (.+)", citation_data)
        conference_start_date = re.search(r"Conference startDate: (.+)", citation_data)
        conference_end_date = re.search(r"Conference endDate: (.+)", citation_data)
        conference_location = re.search(r"Conference location: (.+)", citation_data)
        conference_website = re.search(r"Conference officialWebsite: (.+)", citation_data)


        citation_info = {
            "Citation text": citation_text.strip(),
            "Conference Info": {
                "Conference title": conference_title.group(1).strip() if conference_title else None,
                "Conference short name": conference_short_name.group(1).strip() if conference_short_name else None,
                "Conference Qid": conference_qid.group(1).strip() if conference_qid else None,
                "Conference startDate": conference_start_date.group(1).strip() if conference_start_date else None,
                "Conference endDate": conference_end_date.group(1).strip() if conference_end_date else None,
                "Conference location": conference_location.group(1).strip() if conference_location else None,
                "Conference officialWebsite": conference_website.group(1).strip() if conference_website else None
            }
        }

        result.append(citation_info)

    output_file = "result.yaml"
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(result,f)



