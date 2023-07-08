# Useful for processing python libraries into dataet for text to code
import os
import re
import json

def extract_functions_and_classes(source_code):
    class_pattern = re.compile(r"(class\s+.*?:.*?)(?=class\s+|$)", re.DOTALL | re.MULTILINE)
    function_pattern = re.compile(r"(def\s+.*?:.*?)(?=def\s+|$)", re.DOTALL | re.MULTILINE)
    comment_pattern = re.compile(r"#[^\n]*")

    classes = class_pattern.findall(source_code)
    functions = function_pattern.findall(source_code)
    comments = comment_pattern.findall(source_code)

    data = []

    for i, class_code in enumerate(classes):
        if i < len(comments) and not any(keyword in comments[i].lower() for keyword in ["licence", "license"]):
            data.append({
                'prompt': 'What does the following class do?',
                'response': comments[i] + '\n' + class_code
            })

    for i, function_code in enumerate(functions):
        if i < len(comments) and not any(keyword in comments[i].lower() for keyword in ["licence", "license"]):
            data.append({
                'prompt': 'What does the following function do?',
                'response': comments[i] + '\n' + function_code
            })

    return data

directory = ".local/lib/python3.10/site-packages"

data = []

for package in os.listdir(directory):
    if os.path.isdir(os.path.join(directory, package)) and not package.startswith('__') and not package.endswith('.egg-info'):
        for root, dirs, files in os.walk(os.path.join(directory, package)):
            for file in files:
                if file.endswith('.py'):
                    with open(os.path.join(root, file), 'r') as f:
                        try:
                            source_code = f.read()
                            data.extend(extract_functions_and_classes(source_code))
                        except Exception as e:
                            print(f"Failed to process {file} in {root}: {str(e)}")

with open('dataset.json', 'w') as f:
    json.dump(data, f)
