from typing import Any, Dict

from pocketflow import Node

from src.utils.generate_tool_doc import generate_tools_code


class CreateToolsDoc(Node):
    def prep(self, shared: Dict[str, Any]) -> str:
        """Get the input path for tool documentation generation."""
        return shared["tools_file_path"]

    def exec(self, input_path: str) -> Dict[str, str]:
        """Generate documentation from tools.py file using the utility."""
        print(f"\n1. Generating documentation from tools file at: {input_path}")
        doc_str = generate_tools_code(input_path)
        print(f"Generated documentation length: {len(doc_str)} characters")
        return doc_str

    def post(
        self, shared: Dict[str, Any], prep_res: str, exec_res: Dict[str, str]
    ) -> str:
        """Store the documentation string in shared store."""
        shared["tools_doc_str"] = exec_res
        return "default"
