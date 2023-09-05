import matplotlib.pyplot as plt


categories = ['GPT-4 result', 'GPT-4 result(after check)', 'GPT-3.5 result', 'GPT-3.5 result(after check)']
correct_results = [40, 40, 34, 36]

plt.figure(figsize=(14, 9))


bars = plt.bar(categories, correct_results,width=0.3)

for bar in bars:
    height = bar.get_height()
    plt.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3),
                 textcoords="offset points",
                 ha='center', va='bottom', fontsize=12)

plt.title('Test Results')
plt.xlabel('Test Categories')
plt.ylabel('Number of Correct Results')

plt.tight_layout()
plt.show()
