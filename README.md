# RWTH Scientific conference title disambiguation system-based on GPT and Wikidata
The project uses a large-scale knowledge graph (wikidata) and vector database (weaviate) to provide a factual basis for LLM (GPT), and guides LLM through Langchain to analyze the scientific conference information that may exist in the reference text entered by the user step by step, and find detailed metadata.


+ [Project Introduction](#project-introduction)



## Project Introduction
Different scientific conference information is likely to be covered in the cited text of each paper, but differences in format and writing make conference identification difficult. With the rapid development of large language models (LLMs), it becomes possible to use, for example, GPT as a recognition tool. But at present, LLM still has the problem of fabricating answers, so it is necessary to use large knowledge graphs as the basis of facts, and vector databases can provide similar matching functions that traditional search engines do not have.

+ ### Current operating environment of the project：

### python : 

```
 python 3.10
```

### Framework for building Agent process :

```
langchain 0.0.233
```
Langchain is currently a popular application framework for extending LLM, allowing LLM to interact with external libraries or resources to get better answers. For the specific use of Langchain, please refer to the official document https://python.langchain.com/docs/get_started/introduction.html

### Vector Database：
```
weaviate_client 3.21.0
```
***Precautions：To clone the project and run it, make sure to keep the extension package as consistent as possible***

+ ### The main file directory of the project
The main file directory of the project is shown in the figure.
```

─accuracyTest
│  │  acc_test.py                       # Testing the Processing Accuracy of Agent
│  │  proofread.py                      # Verify output
│  │  proofreadText.yml
│  │  result_chart.py                   # Plot the results of the test
│  │  test_output.yaml                      
│  │  structured_test_output.yaml                
│  │  testText.yaml                     # Previous test text, integrated into the yaml file
│  │
│  ├─testOutput                         # output result for old template
│  │      citation1_output.txt
│  │      ...
│  │      citation10_output.txt
│  │
│  └─testText                           # citation text for testing old template
│          citation1.txt
│          ...
│          citation10.txt
│
├─backend
│     agent_build.py                    # Build custom Agent, consistent with lancghain documentation
│     agent_utils.py                    # Functions used by Agent tools
│     api_connector.py                  # Connect GPT and Weaviate via API keys
│     main.py
│     result_to_yaml.py                 # Convert GPT natural language results into computer-readable structured data                          
│     weaviateQ.py
│     templates.yaml                    # Store the prompt templates that need to be used in each tool and agent
│
├─frontend
│     dict_edit.py    
│     main.py
│
├─test
│     agentTest.py                     # Test when update code
│
│─WeaviateVS
│      conference_data.json
│      weaviateVS.py                   # Create a vector database based on wikidata metadata
│      wikidataConferenceJson.py       
```
The project puts most of the text, such as templates and test text, in yaml files. The yaml files such as structured_output are the processing results of the previous GPT natural language results. Its general structure is like:

![image](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/chart/UML.png)

Each citation containing a conference is stored in the yaml file as a combination of the citation text and specific conference information, which contains different metadata.

## Agent process

## Current Agent Test Results
see [test eavluation](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/evaluation/test_evaluation.md)
