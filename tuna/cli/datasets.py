# pylint: disable=all
# FIXME: This file has major issues, updating soon

import json
from tuna.cli.constants import REPO_FILE, TRAIN_DATA, EXCLUDED_EXTENSIONS, EXCLUDED_FILENAMES

def is_excluded(filename):
    if any(filename.lower().endswith(ext) for ext in EXCLUDED_EXTENSIONS):
        return True
    if filename.lower() in EXCLUDED_FILENAMES:
        return True
    return False

def create_prompts(file):
    prompts = []
    content_lines = file['content'].split('\n')
    
    function_starts = [i for i, line in enumerate(content_lines) if line.strip().startswith('def ')]
    for start in function_starts:
        function_end = start + 1
        while function_end < len(content_lines) and not content_lines[function_end].strip() == '':
            function_end += 1
        function_code = '\n'.join(content_lines[start:function_end])
        prompts.append({
            'input': f"Complete the following function:\n\n{function_code}",
            'output': function_code
        })
    
    for i, line in enumerate(content_lines):
        if line.strip().startswith('def '):
            func_name = line.split('(')[0].strip()[4:]
            prompts.append({
                'input': f"Write a docstring for the following function:\n\n{line}",
                'output': f'"""\nFunction {func_name}:\n\n[Add detailed docstring here]\n"""'
            })
    
    for i in range(0, len(content_lines), 5):
        snippet = '\n'.join(content_lines[i:i+5])
        prompts.append({
            'input': f"Refactor the following code snippet to improve readability and efficiency:\n\n{snippet}",
            'output': snippet
        })
    
    return prompts

def traverse_files(files, parent_path=''):
    file_list = []
    for file in files:
        if is_excluded(file['filename']):
            continue
        if file['directory']:
            file_list.extend(traverse_files(file['children'], parent_path + file['filename'] + '/'))
        else:
            file['filepath'] = parent_path + file['filename']
            file_list.append(file)
    return file_list

def build_dataset():
    with open(REPO_FILE, 'r') as f:
        repository_data = json.load(f)
    all_files = traverse_files(repository_data['files'])

    dataset_entries = []
    for file in all_files:
        prompts = create_prompts(file)
        dataset_entries.extend(prompts)

    save_to_jsonl(dataset_entries, TRAIN_DATA)

def save_to_jsonl(dataset_entries, output_file):
    with open(output_file, 'w') as f:
        for entry in dataset_entries:
            json.dump(entry, f)
            f.write('\n')

