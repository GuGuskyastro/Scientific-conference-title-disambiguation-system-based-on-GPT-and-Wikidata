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
│  │  proofreading_results.yaml         # Test Results
│  │  proofreadText.yml                 
│  │  test_output.yaml                  
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
│     weaviateQ.py
│     templates.yaml                    # Store the prompt templates that need to be used in each tool and agent
│
├─fronted
│     front.html
│     web.py
│
├─test
│     agentTest.py                     # Test when update code
│
│─WeaviateVS
│      conference_data.json
│      weaviateVS.py                   # Create a vector database based on wikidata metadata
│      wikidataConferenceJson.py       
```

## Agent process

## Current Agent Test Results
The agent's processing flow is based on the question-and-answer with GPT, including the final output results, so different templates and models may bring different results. To explore the performance of GPT in different situations, I used ten sets of citations for testing. 

Each of the ten sets of [test texts](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/accuracyTest/testText.yaml) contained five citations. In general, there are two types of citations:

1.The citation contains information about the meeting

2.The citation does not have any information about conference (maybe from scientific journals, etc.)

However, the purpose of the project is to provide detailed metadata of the conference with the help of the knowledge graph (Wikidata), so GPT is also required to find the matching Qid by comparing the query results in the Weaviate VS. Then the third situation may occur:

3.The citation does contain conference information, but the conference is not stored in the database (wikidata does not include it)

In the first five groups of test texts, there is one citation in each group that does not contain conference information. Among the remaining four citations, two conferences can be queried with specific metadata, and two are not included in the database. In the last five groups of test texts, two citation in each group do not contain conference information, one of which can be queried for specific metadata, and two of which are not included in the database. Different situations lead to differences in the time and cost of executing agents.

### Individually - Intergrate

First focus on the performance of GPT-3.5 under two different templates.
#### Run time
![image](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/chart/individually_with_intergrate/runtime_1-5.png)

The Intergrate Agent parses all the text entered by the user at one time, which saves time compared to calling the tool by using GPT to parse citation one by one. (Of course, parsing 5 citations at once will take more time than parsing one) From the test results, the time spent by Intergrate Agent is shorter for each set of tests. For The first five tests saved an average of more than 15 seconds, the efficiency increased by about 18%.

![image](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/chart/individually_with_intergrate/runtime_6-10.png)

As the number of citations that need to be further queried is less, the average run time of the two agents in the last five tests is shorter, but it is still in line with the results obtained in the first five tests. On average, Intergrate Agent saved about 10 seconds. The output time of GPT is not stable each time, but it can be seen from this trend that when entering more citation text, using the second method can save time.

#### Token and cost
![image](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/chart/individually_with_intergrate/cost_1-5.png)

There is also a significant difference in cost between the two agent. Both tools in agent need to use GPT (extract conference, compare conference information), so each time a tool is used, a template of the corresponding task will be sent to GPT. In the first five tests, the Intergrate Agent spent about 70% of the Individually Agent on average.

![image](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/chart/individually_with_intergrate/cost_6-10.png)
The test result of the last five groups is also similar.

#### Accuracy
![image](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/chart/individually_with_intergrate/error_1-5.png)
![image](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/chart/individually_with_intergrate/error_6-10.png)

