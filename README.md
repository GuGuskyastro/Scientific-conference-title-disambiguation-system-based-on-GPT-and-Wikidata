# RWTH Scientific conference title disambiguation system-based on GPT and Wikidata
The project uses a large-scale knowledge graph (wikidata) and vector database (weaviate) to provide a factual basis for LLM (GPT), and guides LLM through Langchain to analyze the scientific conference information that may exist in the reference text entered by the user step by step, and find detailed metadata.


+ [Project Introduction](#project-introduction)

+ [Test Results](#Test Results)


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
weaviate_client==3.21.0
```
***Precautions：To clone the project and run it, make sure to keep the extension package as consistent as possible***

+ ### The main file directory of the project
The main file directory of the project is shown in the figure.

─accuracyTest
│  │  acc_test.py                       # Testing the Processing Accuracy of Agent
│  │
│  ├─testOutput                         # output result
│  │      citation1_output.txt
│  │      ...
│  │      citation10_output.txt
│  │
│  └─testText                           # citation text for testing
│          citation1.txt
│          ...
│          citation10.txt
│
├─backend
│  │  agent_build.py                    # Build custom Agent, consistent with lancghain documentation
│  │  agent_utils.py                    # Functions used by Agent tools
│  │  api_connector.py                  # Connect GPT and Weaviate via API keys
│  │  main.py                           
│  │  weaviateQ.py
│  │  __init__.py
│
├─fronted
│      front.html
│      web.py
│
├─test
│      agentTest.py                    # Test when update code
│      __init__.py
│

## Test Results

