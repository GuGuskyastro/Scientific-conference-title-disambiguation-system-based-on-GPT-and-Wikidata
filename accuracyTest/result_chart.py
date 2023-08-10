from proofread import proofread_result
import yaml
import matplotlib.pyplot as plt
import numpy as np
import re

#This file is used to plot the results of the test, including run time, run cost, and number of errors.

def extract_runtimes(file,range):
    with open(file, 'r', encoding="utf-8") as file:
        data = yaml.safe_load(file)
        run_times = []
        for i in range:
            key = f'citation{i}'
            if key in data:
                run_time = float(data[key]['run_time'].split('second')[0].strip())
                run_times.append(run_time)
        return run_times


def runtime_plot(range,xlabel,file1,file2,labels):
    individually_runtimes = extract_runtimes(file1,range)
    integrate_runtimes = extract_runtimes(file2,range)
    average_individually = sum(individually_runtimes) / len(individually_runtimes)
    average_integrate = sum(integrate_runtimes) / len(integrate_runtimes)

    bar_width = 0.25
    index = np.arange(1, 6)

    fig, ax = plt.subplots(figsize=(15, 10))
    rects1 = ax.bar(index, individually_runtimes, bar_width, label=labels[0])
    rects2 = ax.bar(index + bar_width, integrate_runtimes, bar_width, label=labels[1])

    avg_rects1 = ax.bar(6, average_individually, bar_width, color=rects1[0].get_facecolor())
    avg_rects2 = ax.bar(6 + bar_width, average_integrate, bar_width, color=rects2[0].get_facecolor())

    for rect in rects1 + avg_rects1:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')

    for rect in rects2 + avg_rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')

    ax.set_xlabel('Test Cases')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Comparison of Test Runtimes')
    ax.set_xticks(np.append(index, 6 + bar_width / 2))
    ax.set_xticklabels(xlabel)
    ax.legend(loc='upper right')
    plt.show()

def get_cost(file,range):
    pattern = r'Total Tokens: (\d+)\s+Total Cost \(USD\): \$([\d.]+)'

    token_and_cost = []

    with open(file, 'r', encoding="utf-8") as file:
        data = yaml.safe_load(file)
        for i in range:
            key = f'citation{i}'
            if key in data:
                text = data[key]['result']
                matches = re.findall(pattern, text)
                for match in matches:
                    tokens = int(match[0])
                    cost = float(match[1])
                    token_and_cost.append({"Total Tokens": tokens, "Total Cost (USD)": cost})
    return token_and_cost



def token_cost_plot(range,xlabel,file1,file2,labels):
    individually_data = get_cost(file1, range)
    integrate_data = get_cost(file2, range)

    individually_tokens = [entry['Total Tokens'] for entry in individually_data]
    integrate_tokens = [entry['Total Tokens'] for entry in integrate_data]

    individually_costs = [entry['Total Cost (USD)'] for entry in individually_data]
    integrate_costs = [entry['Total Cost (USD)'] for entry in integrate_data]

    average_individually_token = sum(individually_tokens) / len(individually_tokens)
    average_integrate_token = sum(integrate_tokens) / len(integrate_tokens)
    average_individually_cost = sum(individually_costs) / len(individually_costs)
    average_integrate_cost = sum(integrate_costs) / len(integrate_costs)

    bar_width = 0.25
    index = np.arange(1, 6)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 20))

    rects1 = ax1.bar(index, individually_tokens, bar_width, label=labels[0])
    rects2 = ax1.bar(index + bar_width, integrate_tokens, bar_width, label=labels[1])
    avg_rects1 = ax1.bar(6, average_individually_token, bar_width, color=rects1[0].get_facecolor())
    avg_rects2 = ax1.bar(6 + bar_width, average_integrate_token, bar_width, color=rects2[0].get_facecolor())

    for rect in rects1 + avg_rects1:
        height = rect.get_height()
        ax1.annotate(f'{height}', xy=(rect.get_x() + rect.get_width() / 2, height),
                     xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')

    for rect in rects2 + avg_rects2:
        height = rect.get_height()
        ax1.annotate(f'{height}', xy=(rect.get_x() + rect.get_width() / 2, height),
                     xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')

    ax1.set_ylabel('Token Usage')
    ax1.set_title('Comparison of Token Usage')
    ax1.set_xticks(np.append(index, 6 + bar_width / 2))
    ax1.set_xticklabels(xlabel)
    ax1.legend(loc='upper right')

    rects1 = ax2.bar(index, individually_costs, bar_width, label=labels[0])
    rects2 = ax2.bar(index + bar_width, integrate_costs, bar_width, label=labels[1])
    avg_rects1 = ax2.bar(6, average_individually_cost, bar_width, color=rects1[0].get_facecolor())
    avg_rects2 = ax2.bar(6 + bar_width, average_integrate_cost, bar_width, color=rects2[0].get_facecolor())

    for rect in rects1 + avg_rects1:
        height = rect.get_height()
        ax2.annotate(f'{height:.5f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                     xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')

    for rect in rects2 + avg_rects2:
        height = rect.get_height()
        ax2.annotate(f'{height:.5f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                     xytext=(0, 5), textcoords='offset points', ha='center', va='bottom')

    ax2.set_ylabel('Total Cost (USD)')
    ax2.set_title('Comparison of Total Costs')
    ax2.set_xticks(np.append(index, 6 + bar_width / 2))
    ax2.set_xticklabels(xlabel)
    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.show()



def acc_plot(x_label,start,end,file1,file2,labels):
    total_tests = 5

    errors_individually = proofread_result(file1, 'proofreadText.yml')[start:end]
    errors_integrate = proofread_result(file2, 'proofreadText.yml')[start:end]

    correct_individually = [total_tests - error for error in errors_individually]
    correct_integrate = [total_tests - error for error in errors_integrate]

    fig, ax = plt.subplots(figsize=(16, 9))

    bar_width = 0.25
    bar_gap = 0.1
    bar_positions_individually = np.arange(len(x_label))
    bar_positions_integrate = [pos + bar_width + bar_gap for pos in bar_positions_individually]

    ax.bar(bar_positions_individually, correct_individually, width=bar_width, label=labels[0])
    ax.bar(bar_positions_integrate, correct_integrate, width=bar_width, label=labels[1])
    ax.bar(bar_positions_individually, errors_individually, width=bar_width, label='Wrong results', color='red', bottom=correct_individually)
    ax.bar(bar_positions_integrate, errors_integrate, width=bar_width, color='red', bottom=correct_integrate)

    ax.set_xticks([pos + bar_width / 2 for pos in bar_positions_individually])
    ax.set_xticklabels(x_label)
    ax.set_ylabel('Number of Tests')
    ax.set_title('Test Results Comparison')
    ax.legend(loc='upper right')

    ax.set_ylim(0, 6)

    plt.tight_layout()
    plt.show()




if __name__ == '__main__':
    individually = 'test_output_individually.yaml'
    intergrate = 'test_output_integrate.yaml'
    intergrate_gpt4 = 'test_output_intergrate_gpt4.yaml'

    struct_indi = 'structured_test_output_individually.yaml'
    struct_inter= 'structured_test_output_integrate.yaml'
    struct_inter_gpt4 = 'structured_test_output_integrate_gpt4.yaml'

    range1 = range(1,6)
    range2 = range(6,11)

    xlabel1 = ['Citation Group 1','Citation Group 2','Citation Group 3','Citation Group 4','Citation Group 5','Average']
    xlabel2 = ['Citation Group 6','Citation Group 7','Citation Group 8','Citation Group 9','Citation Group 10','Average']
    label1 = ['Agent:Individually', 'Agent:Integrate']
    label2 = ['Agent:Intergrate', 'Agent:Integrate GPT4']

    runtime_plot(range1,xlabel1,individually,intergrate,label1)
    runtime_plot(range2,xlabel2,individually,intergrate,label1)

    runtime_plot(range1,xlabel1,intergrate,intergrate_gpt4,label2)
    runtime_plot(range2,xlabel2,intergrate,intergrate_gpt4,label2)

    token_cost_plot(range1,xlabel1,individually,intergrate,label1)
    token_cost_plot(range2,xlabel2,individually,intergrate,label1)

    token_cost_plot(range1,xlabel1,intergrate,intergrate_gpt4,label2)
    token_cost_plot(range2,xlabel2,intergrate,intergrate_gpt4,label2)

    xlabel_acc1 = ['Citation Group 1','Citation Group 2','Citation Group 3','Citation Group 4','Citation Group 5']
    xlabel_acc2 = ['Citation Group 6','Citation Group 7','Citation Group 8','Citation Group 9','Citation Group 10']

    acc_plot(xlabel_acc1,0,5,struct_indi,struct_inter,label1)
    acc_plot(xlabel_acc2,5,10,struct_indi,struct_inter,label1)

    acc_plot(xlabel_acc1,0,5,struct_inter,struct_inter_gpt4,label2)
    acc_plot(xlabel_acc2,5,10,struct_inter,struct_inter_gpt4,label2)