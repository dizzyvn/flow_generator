from pocketflow import Flow

from src.nodes.create_tools_doc import CreateToolsDoc
from src.nodes.generate_code import GenerateCode
from src.nodes.setup_execution_sandbox import SetupExecutionSandbox


def create_flow():
    """Create and return a flow for implementing a runnable workflow using PocketFlow."""
    # Create nodes
    create_tools_doc_node = CreateToolsDoc()
    generate_code_node = GenerateCode(max_retries=3)
    setup_sandbox_node = SetupExecutionSandbox()

    # Connect nodes in sequence
    (create_tools_doc_node >> generate_code_node >> setup_sandbox_node)

    return Flow(start=create_tools_doc_node)
