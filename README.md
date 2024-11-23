## Overview
Ohad PR Helper CLI is a powerful tool designed to automatically generate code based on feature requests. It simplifies the process of coding by reading existing files in your repository, understanding the context, and writing new code as per your specifications.

## Main Benefits
- **Automated Coding**: Automatically generate code snippets or entire files based on your feature request without manually writing code from scratch.
- **Time-Saving**: Save valuable time by reducing manual coding tasks, allowing you to focus on more complex aspects of development.
- **Consistency**: Ensure consistent code quality and style across different parts of your project by leveraging learned patterns in the existing repository.

## How It Works
1. **Read Repository Files**: The tool reads files from your local repository, optionally restricting it to specific files if requested.
2. **Understand Context**: It uses a coding service to analyze the read files and understand their context, structure, and coding style.
3. **Generate Code**: Based on your feature request, it generates new code or modifies existing code as needed.
4. **Write Output**: The generated code is written back to the repository in the appropriate location.
5. **Explain Changes**: An explanation file is created to detail the changes made, including the reasoning behind each modification.

## Usage
Run the CLI using Python:

```bash
python cli.py
```
Follow the prompts to specify which files to include (if any) and what feature you want implemented.

## Pre-commit Setup
To ensure code quality before committing, install pre-commit hooks. Follow these steps:
1. Install the dev requirements file using pip:
   ```bash
   pip install -r requirements-dev.txt
   ```
2. Run pre-commit to set up the repository hooks:
   ```bash
   pre-commit install
   ```