import argparse
import ast
import os
from typing import Dict, List


def extract_function_info(source_code: str) -> List[Dict]:
    """
    Extract function information from source code using AST.
    """
    tree = ast.parse(source_code)
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Get function signature
            func_name = node.name
            args = []

            # Process arguments
            for arg in node.args.args:
                arg_name = arg.arg
                if arg_name != "self":  # Skip self parameter
                    args.append(arg_name)

            # Get docstring
            docstring = ast.get_docstring(node)

            # Get return type annotation
            return_type = None
            if node.returns:
                return_type = ast.unparse(node.returns)

            functions.append(
                {
                    "name": func_name,
                    "args": args,
                    "docstring": docstring,
                    "return_type": return_type,
                }
            )

    return functions


def format_function_code(func_info: Dict) -> str:
    """
    Format function information into code string.
    """
    # Format function signature
    args_str = []
    for arg in func_info["args"]:
        args_str.append(f"{arg}: str")

    # Format signature without using backslash in f-string
    args_formatted = ",\n    ".join(args_str)
    signature = f"def {func_info['name']}(\n    {args_formatted}\n) -> {func_info['return_type']}:"

    # Format docstring
    docstring = func_info["docstring"]
    if docstring:
        # Indent docstring
        docstring_lines = docstring.split("\n")
        indented_docstring = "\n".join("    " + line for line in docstring_lines)
        docstring = f'    """\n{indented_docstring}\n    """'

    # Combine everything
    return f"{signature}\n{docstring}"


def generate_tools_code(input_path: str) -> str:
    """
    Generate documentation from Python source code.

    Args:
        input_path (str): Path to the input Python file

    Returns:
        str: Generated documentation string
    """
    # Read input file
    with open(input_path, "r") as f:
        source_code = f.read()

    # Extract function information
    functions = extract_function_info(source_code)

    # Generate output content
    output = []
    for func in functions:
        output.append(format_function_code(func))
        output.append("")  # Add blank line between functions

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Generate function documentation from Python source code"
    )
    parser.add_argument(
        "--input",
        "-i",
        default=os.path.join(os.path.dirname(__file__), "tools.py"),
        help="Path to input Python file (default: tools.py in same directory)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "prompts",
            "tools_code.txt",
        ),
        help="Path to output documentation file (default: prompts/tools_code.txt)",
    )

    args = parser.parse_args()
    doc_str = generate_tools_code(args.input)

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # Write to output file
    with open(args.output, "w") as f:
        f.write(doc_str)
    print(f"Tools doc from {args.input} is generated and saved to {args.output}.")


if __name__ == "__main__":
    main()
