# Code First Flow Generator

A powerful tool for generating code flows based on natural language requirements using PocketFlow framework. This project helps you create, visualize, and manage code flows for various applications.

## Overview

This repository provides a framework for generating code flows from natural language requirements. It uses PocketFlow, a lightweight framework for building LLM-powered applications, to create and manage flows of code generation tasks.

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd code_first_flow_generator
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install Mermaid CLI for visualization (required for flow diagrams):

```bash
npm install -g @mermaid-js/mermaid-cli
```

## Usage

### Running the Main Flow

The main flow generator can be run using `main.py`. It takes a natural language requirement and generates code based on it.

```bash
python main.py --requirement "Your requirement here" --sandbox-dir "execution_sandbox"
```

Parameters:

- `--requirement`: The natural language requirement for code generation (default: "Send an email to a friend about a place to go in a city.")
- `--sandbox-dir`: Directory where generated code will be stored (default: "execution_sandbox")

### Visualizing Flows

You can visualize the generated flows using the visualization tool:

```bash
python execution_sandbox/visualize.py --output flow.png
```

Parameters:

- `--output`: Output file path (default: flow.png)

### Generating Tools

The repository includes a helper script to generate tool implementations based on descriptions:

```bash
python src/helper/generate_tool.py --description "Your tool description here"
```

This will generate a Python function implementation with:

- Proper type hints
- Comprehensive docstring
- Mock data
- Error handling
- Implementation Details

## Implementation Details

The project is built using PocketFlow, a minimalist framework for building LLM-powered applications. The system follows a four-step workflow to generate and execute code from natural language requirements:

### 1. Flow Generation Process

The system uses a sequence of specialized nodes to transform natural language requirements into executable code:

1. **CreateToolsDoc Node**

   - Generates comprehensive documentation for available tools
   - Uses `generate_tools_code` utility to create tool descriptions
   - Stores tool documentation in the shared store for use in code generation
2. **GenerateCode Node**

   - Core node responsible for code generation
   - Uses a sophisticated prompt engineering approach:
     ```python
     system_prompt = """
     You are a code generation expert that creates PocketFlow applications...

     PocketFlow Documentation:
     {pocketflow_doc}

     Available Tools:
     {tools_doc}

     Design a complete flow that satisfies the requirement following these rules:
     1. Follow PocketFlow's patterns and best practices
     2. Have clear node responsibilities and transitions
     3. Use only the provided tools in node.exec() methods
     4. Each node must follow the three-step pattern: prep(), exec(), post()
     """
     ```
   - Generates multiple files:
     - `thinking.txt`: Explains the design decisions and flow logic
     - Node files: Individual node implementations
     - `flow.py`: Flow creation and node connections
     - `main.py`: Entry point for the generated application
3. **SetupExecutionSandbox Node**

   - Creates a clean execution environment
   - Organizes generated files into appropriate directories
   - Ensures proper file structure for execution
4. **ExecuteCode Node**

   - Runs the generated code in the sandbox environment
   - Captures and reports execution results
   - Handles errors and provides feedback

### 2. Prompt Engineering

The system uses carefully crafted prompts to ensure high-quality code generation:

### 2. Code Organization

The generated code follows a consistent structure:

1. **Node Implementation**

   ```python
   class NodeName(Node):
       def prep(self, shared):
           # Prepare data for tool execution
           return prepared_data

       def exec(self, prep_res):
           # Execute single tool with prepared data
           return tool_name(**prep_res)

       def post(self, shared, prep_res, exec_res):
           # Store results and handle routing
           pass
   ```
2. **Flow Structure**

   ```python
   def create_flow():
       # Create nodes
       node1 = Node1()
       node2 = Node2()

       # Connect nodes
       node1 >> node2

       return Flow(start=node1)
   ```
3. **Main Entry Point**

   ```python
   def main():
       shared = {
           "input_data": initial_data,
           "results": {}
       }

       flow = create_flow()
       flow.run(shared)
   ```

## Project Structure

```
├── main.py                 # Main entry point for flow generation
├── requirements.txt        # Project dependencies
├── src/
│   ├── flow.py            # Flow creation and management
│   ├── helper/
│   │   └── generate_tool.py  # Tool generation helper
│   └── prompt/
│       └── pocketflow_doc.txt  # PocketFlow documentation
└── execution_sandbox/
    ├── visualize.py       # Flow visualization tool
    └── utils/            # Generated utilities
```

## Todo

* [ ] Test with batch node
* [ ] Test with conditional branch
* [ ] Figure out how to implement the user `<->` planner interaction

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
