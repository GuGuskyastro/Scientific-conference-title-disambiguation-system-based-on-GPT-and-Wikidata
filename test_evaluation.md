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

Intergrate Agent achieves advantages in running time and cost but performs worse than Individually Agent in accuracy. The latter had no errors in the first five sets of tests, while the former had errors in both tests. By observing the operation log, there are also some differences between the two errors.
+ #### Error in test 4
```
Citation 2:
    - Citation text: Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, and Jeffrey Dean. 2013. Distributed Representations of Words and Phrases and Their Compositionality. In Proceedings of the 27th International Conference on Neural Information Processing Systems - Volume 2 (NIPS’13). Curran Associates Inc.,Lake Tahoe, Nevada, 3111–3119.
    - Conference title: 
    - Conference short name: 
```
The second Agent in Test 4 had trouble parsing this citation, which actually contained a conference and could be found in the database, but only return empty as result.

```
Action: Extraction
Action Input: 
- KSaleem, M., Mehmood, Q., Ngonga Ngomo, A.C.: FEASIBLE: A Feature-Based SPARQL Benchmark Generation Framework. In: International Semantic Web Conference. pp. 52–69. Springer (2015)
- Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, and Jeffrey Dean. 2013. Distributed Representations of Words and Phrases and Their Compositionality. In Proceedings of the 27th International Conference on Neural Information Processing Systems - Volume 2 (NIPS’13). Curran Associates Inc.,Lake Tahoe, Nevada, 3111–3119.
- K.-F. Kollias, C. K. Syriopoulou-Delli, P. Sarigiannidis, G. F. Fragulis, The contribution of machine learning and eye-tracking technology in autism spectrum disorder research: A review study, in: 2021 10th International Conference on Modern Circuits and Systems Technologies (MOCAST), IEEE, 2021, pp. 1–4.
- S. A. Mithbavkar, M. S. Shah, Recognition of emotion through facial expressions using emg signal, in: 2019 international conference on nascent technologies in engineering (ICNTE), IEEE, 2019, pp. 1–6.
- T. D. Nguyen, P. Rieger, H. Yalame, et al., “FLGUARD: Secure and Private Federated Learning,” en,arXiv:2101.02281 [cs], 2021. (visited on 05/18/2021)

Observation:properties:
  Citation text:
    type: string
  Conference title:
    type: string
  Conference short name:
    type: string

Citation 1:
  Citation text: Saleem, M., Mehmood, Q., Ngonga Ngomo, A.C.: FEASIBLE: A Feature-Based SPARQL Benchmark Generation Framework. In: International Semantic Web Conference. pp. 52–69. Springer (2015)
  Conference title: International Semantic Web Conference 2015
  Conference short name: ISWC 2015

Citation 2:
  Citation text: Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, and Jeffrey Dean. 2013. Distributed Representations of Words and Phrases and Their Compositionality. In Proceedings of the 27th International Conference on Neural Information Processing Systems - Volume 2 (NIPS’13). Curran Associates Inc.,Lake Tahoe, Nevada, 3111–3119.
  Conference title: 
  Conference short name: 
...
```
The above is a part of the log of that operation(until corresponding citation), can find that during the Intergrate Agent, GPT did not resolve that the citation contained a conference at beginning, which resulted in no relevant information in the final output.

```
Thought: I need to repeat the above steps for the remaining citations in the input text.

Action: Extraction
Action Input: "Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, and Jeffrey Dean. 2013. Distributed Representations of Words and Phrases and Their Compositionality. In Proceedings of the 27th International Conference on Neural Information Processing Systems - Volume 2 (NIPS’13). Curran Associates Inc.,Lake Tahoe, Nevada, 3111–3119."

Observation:properties:
  Citation text: Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, and Jeffrey Dean. 2013. Distributed Representations of Words and Phrases and Their Compositionality. In Proceedings of the 27th International Conference on Neural Information Processing Systems - Volume 2 (NIPS’13). Curran Associates Inc.,Lake Tahoe, Nevada, 3111–3119.
  Conference title: International Conference on Neural Information Processing Systems 2013
  Conference short name: NIPS 2013
```
This problem was not encountered when using Individually Agent. When multiple citations are input at one time, GPT-3.5 may make a misjudgment when parsing, which will affect the final output.

+ #### Error in test 5

```
Citation 4:
      Citation text: Erling, O., Averbuch, A., Larriba-Pey, J., Chafi, H., Gubichev, A., Prat, A., Pham, M.D., Boncz, P.: The LDBC Social Network Benchmark: Interactive Workload. In: Proceedings of the 2015 ACM SIGMOD International Conference on Management of Data. pp. 619–630 (2015)
      Conference title: ACM SIGMOD International Conference on Management of Data 2015
      Conference short name: SIGMOD 2015
      Conference Qid: Q113715793
      Conference startDate: 2015-05-31
      Conference endDate: 2015-06-04
      Conference location: Melbourne
      Conference officialWebsite: https://sigmod2021.org/
```
In Test 5, the Intergrate Agent made an error in the output of the fourth citation. The citation does contain a meeting, but can not be found in the database. The log shows that no errors occurred during the execution process, but when summarizing and outputting the results at the end, GPT-3.5 also wrote the QID (Q113715793) of the conference contained in the first citation to this meeting, and created the remaining metadata by itself. Although the time and location are consistent with the actual situation, but that this is based on the GPT own knowledge base, rather than the metadata actually queried in the knowledge graph. Also the official website is wrong. 

![image](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/chart/individually_with_intergrate/error_6-10.png)

In the last 5 sets of tests, both agents made errors in the sixth test, and the errors were consistent.
```
Citation 3:
      Citation text: M. Bettayeb, S. Ghunaim, N. Mohamed, and Q. Nasir. “Error correction codes in wireless sensor networks: a systematic literature review”. In 2019 International Conference on Communications, Signal Processing, and their Applications (ICCSPA). IEEE. (2019): 1-6 doi: 10.1109/ICCSPA.2019.8713725.
      Conference title: International Conference on Communications, Signal Processing, and their Applications 2019
      Conference short name: ICCSPA 2019
      Conference Qid: Q106337803
      Conference startDate: 2019-07-20
      Conference endDate: 2019-07-22
      Conference location: Ürümqi
      Conference officialWebsite: N/A
```

The conference referred to in the citation is the 2019 International Conference on Communications, Signal Processing, and their Applications. The conference is not stored in the database, and GPT considers it to be the same as the International Conference on Communications, Signal Processing, and Systems 2019 when comparing query result , The two conferences do have some similarities in title, and the "limited" parsing capabilities of GPT-3.5 made a mistake here. The error occurs when using the query tool, the different Agent methods are not the cause of the error, so in the end both agents have the same error.

### GPT3.5 - GPT4 (Both Intergrate Agent)
The Intergrate Agent has less running time and cost in the test, but lower accuracy, so use the same agent method, but change the LLM model to GPT4, then we can see if there is an improvement in accuracy, and how the actual usage cost and running time are.
![image](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/chart/gpt3.5_with_gpt4/runtime_1-5.png)
![image](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/chart/gpt3.5_with_gpt4/runtime_6-10.png)

Judging from the running time chart, there is a very large gap between GPT-4 and GPT-3.5 throughout the test. This should be due to the current rate limit when general users access GPT-4. In the description on the OpenAI official website, the rate of GPT-4 is severely limited to ease the pressure of a large number of users, which also caused the processing time of GPT-4 to reach more than 3 times that of GPT-3.5 in the test.

![image](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/chart/gpt3.5_with_gpt4/cost_1-5.png)
![image](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/chart/gpt3.5_with_gpt4/cost_6-10.png)

The difference in cost between the two models is even greater. The output of GPT is not stable, especially when there is a "thinking" task when executing the agent, so the usage of tokens will not be exactly the same. But in general, the two are similar, but it can be seen that because of the current API price of GPT-4 and the price reduction of GPT-3.5, the final average cost of GPT-4 is more than 20 times that of GPT-3.5.

![image](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/chart/gpt3.5_with_gpt4/error_1-5.png)
![image](https://github.com/GuGuskyastro/Scientific-conference-title-disambiguation-system-based-on-GPT-and-Wikidata/blob/main/chart/gpt3.5_with_gpt4/error_6-10.png)

The high price and long processing time have brought GPT-4 good processing accuracy. At least in the test text, GPT-4 has no errors. On the other hand, because of the limited processing and understanding capabilities of GPT-3.5, very detailed Instructions and examples are often required in the template to help it understand the task, so when using GPT-4, perhaps a more streamlined template can also allow it to understand and complete tasks.