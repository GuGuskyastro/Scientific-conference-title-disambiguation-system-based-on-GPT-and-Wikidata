import os
import time
from backend.main import run

def run_tests():
    test_dir = "testText"
    output_dir = "testOutput"
    os.makedirs(output_dir, exist_ok=True)

    test_files = os.listdir(test_dir)
    for filename in test_files:
        if filename.endswith(".txt"):
            input_file_path = os.path.join(test_dir, filename)
            output_file_path = os.path.join(output_dir, f"{filename.split('.')[0]}_output.txt")

            with open(input_file_path, "r", encoding="utf-8") as file:
                text = file.read()

            start_time = time.time()
            output = run(text)
            end_time = time.time()

            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(f"Test File: {filename}\n")
                output_file.write(f"Run Time: {end_time - start_time:.4f} seconds\n")
                output_file.write("Log:\n")
                output_file.write(output)

if __name__ == "__main__":
    run_tests()
