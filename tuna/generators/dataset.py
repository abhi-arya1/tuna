import json
import ast
import re
import random
from collections import Counter
from tuna.cli.core.constants import REPO_FILE, TRAIN_DATA, EXCLUDED_EXTENSIONS, EXCLUDED_FILENAMES

def is_excluded(filename):
    return any(filename.lower().endswith(ext) for ext in EXCLUDED_EXTENSIONS) or filename.lower() in EXCLUDED_FILENAMES

def extract_code_elements(content):
    try:
        tree = ast.parse(content)
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        return imports, functions, classes
    except SyntaxError:
        return [], [], []

def analyze_code_structure(content):
    lines = content.split('\n')
    indentation_levels = [len(line) - len(line.lstrip()) for line in lines if line.strip()]
    max_indentation = max(indentation_levels) if indentation_levels else 0
    avg_indentation = sum(indentation_levels) / len(indentation_levels) if indentation_levels else 0
    return {
        'total_lines': len(lines),
        'max_indentation': max_indentation,
        'avg_indentation': avg_indentation,
        'empty_lines': len([line for line in lines if not line.strip()]),
        'comment_lines': len([line for line in lines if line.strip().startswith('#')])
    }

def extract_docstrings(content):
    return re.findall(r'"""[\s\S]*?"""', content)

def generate_dynamic_prompts(file):
    content = file['content']
    filename = file['filename']
    imports, functions, classes = extract_code_elements(content)
    structure = analyze_code_structure(content)
    docstrings = extract_docstrings(content)

    prompts = []

    # Generate prompts based on file characteristics
    if structure['total_lines'] > 200:
        prompts.append({
            'input': f"Analyze the structure of this large Python file ({filename}) and suggest ways to improve its organization:\n\n{content[:500]}...",
            'output': f"File Structure Analysis for {filename}:\n"
                      f"1. Total lines: {structure['total_lines']}\n"
                      f"2. Maximum indentation: {structure['max_indentation']}\n"
                      f"3. Average indentation: {structure['avg_indentation']:.2f}\n"
                      f"4. Empty lines: {structure['empty_lines']}\n"
                      f"5. Comment lines: {structure['comment_lines']}\n\n"
                      "Suggested improvements:\n"
                      "1. [Detailed suggestion for breaking down the file]\n"
                      "2. [Suggestion for improving code organization]\n"
                      "3. [Ideas for enhancing readability]\n"
                      "4. [Recommendations for better documentation]"
        })

    if len(imports) > 10:
        prompts.append({
            'input': f"This file ({filename}) has a large number of imports. Analyze and suggest optimizations:\n\n{content[:500]}...",
            'output': f"Import Analysis for {filename}:\n"
                      f"1. Total imports: {len(imports)}\n"
                      "2. Most common modules imported: [List top 5 most imported modules]\n"
                      "3. Potentially unused imports: [List imports that might be unnecessary]\n"
                      "4. Import organization suggestions:\n"
                      "   a. [Suggestion for grouping related imports]\n"
                      "   b. [Idea for using import aliases to improve readability]\n"
                      "   c. [Recommendation for using 'from x import y' vs 'import x']\n"
                      "5. Performance considerations: [Discuss any heavy imports that might affect load time]"
        })

    # Generate prompts for complex functions
    for func in functions:
        if len(ast.dump(func)) > 1000:  # Arbitrary threshold for "complex" functions
            prompts.append({
                'input': f"Refactor and optimize this complex function from {filename}:\n\n{ast.unparse(func)}",
                'output': f"Refactoring suggestions for function '{func.name}':\n"
                          "1. Complexity analysis:\n"
                          "   a. Cyclomatic complexity: [Estimated value]\n"
                          "   b. Number of parameters: [Count]\n"
                          "   c. Number of local variables: [Count]\n"
                          "2. Structural improvements:\n"
                          "   a. [Suggestion for breaking down the function]\n"
                          "   b. [Ideas for simplifying complex logic]\n"
                          "   c. [Recommendations for improving readability]\n"
                          "3. Performance optimizations:\n"
                          "   a. [Identify potential bottlenecks]\n"
                          "   b. [Suggest algorithmic improvements]\n"
                          "4. Error handling and edge cases:\n"
                          "   a. [Identify potential edge cases]\n"
                          "   b. [Suggest robust error handling strategies]\n"
                          "5. Refactored code snippet:\n"
                          "[Provide a sample of how a part of the function could be refactored]"
            })

    # Generate prompts for classes with many methods
    for cls in classes:
        methods = [node for node in ast.walk(cls) if isinstance(node, ast.FunctionDef)]
        if len(methods) > 10:  # Arbitrary threshold for "many" methods
            prompts.append({
                'input': f"Analyze and improve the design of this class from {filename}:\n\n{ast.unparse(cls)}",
                'output': f"Class design analysis for '{cls.name}':\n"
                          f"1. Total methods: {len(methods)}\n"
                          "2. Potential design patterns: [Identify any patterns the class might be using or could benefit from]\n"
                          "3. Cohesion analysis:\n"
                          "   a. [Discuss how well the methods relate to each other]\n"
                          "   b. [Suggest groupings of related methods]\n"
                          "4. Coupling analysis:\n"
                          "   a. [Identify dependencies on other classes]\n"
                          "   b. [Suggest ways to reduce coupling]\n"
                          "5. Inheritance and composition:\n"
                          "   a. [Discuss current inheritance structure, if any]\n"
                          "   b. [Suggest potential use of composition over inheritance]\n"
                          "6. SOLID principles application:\n"
                          "   [Analyze how well the class adheres to SOLID principles and suggest improvements]\n"
                          "7. Refactoring suggestions:\n"
                          "   a. [Idea for breaking the class into smaller, more focused classes]\n"
                          "   b. [Suggestion for improving method organization]\n"
                          "   c. [Recommendations for enhancing the class's API]"
            })

    # Generate prompts based on docstring quality
    if docstrings:
        prompts.append({
            'input': f"Evaluate and improve the documentation in this file ({filename}):\n\n{docstrings[0]}",
            'output': f"Documentation analysis for {filename}:\n"
                      "1. Docstring coverage: [Percentage of functions/classes with docstrings]\n"
                      "2. Quality assessment:\n"
                      "   a. Completeness: [Evaluate how well the docstrings describe functionality]\n"
                      "   b. Clarity: [Assess the readability and understandability of docstrings]\n"
                      "   c. Consistency: [Evaluate adherence to a consistent documentation style]\n"
                      "3. Improvement suggestions:\n"
                      "   a. [Specific suggestion for enhancing function/method descriptions]\n"
                      "   b. [Ideas for clarifying parameter descriptions]\n"
                      "   c. [Recommendations for improving return value documentation]\n"
                      "   d. [Suggestions for adding usage examples]\n"
                      "4. Example of an improved docstring:\n"
                      "[Provide a rewritten version of one of the existing docstrings]"
        })

    # Generate prompts about potential bugs or code smells
    code_smells = detect_code_smells(content)
    if code_smells:
        prompts.append({
            'input': f"Identify and fix potential bugs or code smells in this file ({filename}):\n\n{content[:500]}...",
            'output': f"Code quality analysis for {filename}:\n"
                      "1. Potential issues detected:\n" +
                      "\n".join(f"   - {smell}" for smell in code_smells) + "\n"
                      "2. Detailed analysis:\n"
                      "[Provide in-depth explanation of each detected issue]\n"
                      "3. Suggested fixes:\n"
                      "[Offer specific code changes to address each issue]\n"
                      "4. Best practices:\n"
                      "[Recommend coding standards or patterns to prevent similar issues]"
        })

    return prompts

def detect_code_smells(content):
    smells = []
    if 'global ' in content:
        smells.append("Use of global variables detected")
    if 'except:' in content:
        smells.append("Bare except clause detected")
    if 'import *' in content:
        smells.append("Wildcard import detected")
    return smells

def traverse_files(files, parent_path=''):
    return [
        file for file in files
        if not file['directory'] and not is_excluded(file['filename'])
    ] + [
        subfile
        for file in files if file['directory']
        for subfile in traverse_files(file['children'], parent_path + file['filename'] + '/')
    ]

def build_dataset(min_entries=100000):
    with open(REPO_FILE, 'r') as f:
        repository_data = json.load(f)
    
    all_files = traverse_files(repository_data['files'])
    dataset_entries = []
    
    while len(dataset_entries) < min_entries:
        for file in all_files:
            dataset_entries.extend(generate_dynamic_prompts(file))
            if len(dataset_entries) >= min_entries:
                break
        
        # generate prompts about file relationships for more entries
        if len(dataset_entries) < min_entries:
            for i in range(0, len(all_files), 2):
                if i + 1 < len(all_files):
                    file1, file2 = all_files[i], all_files[i+1]
                    dataset_entries.extend(analyze_file_relationships(file1, file2))
                    if len(dataset_entries) >= min_entries:
                        break
    
    save_to_jsonl(dataset_entries[:min_entries], TRAIN_DATA)
    print(f"Generated dataset with {min_entries} entries.")

def analyze_file_relationships(file1, file2):
    return [{
        'input': f"Analyze the relationship and potential integration between these two Python files:\n\nFile 1: {file1['filename']}\nFile 2: {file2['filename']}",
        'output': f"File relationship analysis between {file1['filename']} and {file2['filename']}:\n"
                  "1. Common functionalities:\n"
                  "   [Identify and describe any shared purposes or functionalities]\n"
                  "2. Dependencies:\n"
                  "   [Analyze any import relationships or shared data structures]\n"
                  "3. Integration opportunities:\n"
                  "   a. [Suggest potential for creating a shared module]\n"
                  "   b. [Identify opportunities for code reuse]\n"
                  "   c. [Propose ideas for improving overall project structure]\n"
                  "4. Consistency analysis:\n"
                  "   [Evaluate and suggest improvements for maintaining consistent coding style and patterns]\n"
                  "5. Refactoring suggestions:\n"
                  "   [Provide specific ideas for refactoring these files to improve their interaction]"
    }]

def save_to_jsonl(dataset_entries, output_file):
    with open(output_file, 'w') as f:
        for entry in dataset_entries:
            json.dump(entry, f)
            f.write('\n')

if __name__ == "__main__":
    build_dataset()