import ast
import inspect
import logging
import textwrap

from pocketflow_v2 import BatchNode, Flow, Node, StartNode, TerminateNode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_exec_function_calls(node):
    """Extract function names called inside the exec method."""
    if not hasattr(node, "exec"):
        logger.debug(f"Node {type(node).__name__} has no exec method")
        return []

    try:
        exec_source = inspect.getsource(node.exec)
        # Dedent the source code to remove leading whitespace
        exec_source = textwrap.dedent(exec_source)
        logger.debug(f"Found exec source for {type(node).__name__}: {exec_source}")

        tree = ast.parse(exec_source)
        function_calls = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    function_calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    function_calls.append(node.func.attr)

        logger.debug(f"Found function calls: {function_calls}")
        return function_calls
    except Exception as e:
        logger.error(f"Error extracting function calls: {str(e)}")
        return []


def build_mermaid(start):
    ids, visited, lines = {}, set(), ["graph TD"]
    ctr = 1

    def get_id(n):
        nonlocal ctr
        return (
            ids[n] if n in ids else (ids.setdefault(n, f"N{ctr}"), (ctr := ctr + 1))[0]
        )

    def link(a, b, condition=None):
        if condition:
            lines.append(f"    {a} -->|{condition}| {b}")
        else:
            lines.append(f"    {a} --> {b}")

    def get_node_label(node):
        if isinstance(node, TerminateNode):
            return " "
        elif isinstance(node, StartNode):
            return " "
        elif isinstance(node, BatchNode):
            node_type = "BatchNode"
        elif isinstance(node, Node):
            node_type = "Node"
        else:
            node_type = "Unknown"

        node_name = type(node).__name__
        function_calls = get_exec_function_calls(node)
        logger.debug(f"Node {node_name} has function calls: {function_calls}")

        label_parts = [f"{node_type}<br>{node_name}"]
        if function_calls:
            label_parts.append(f"Tools: {', '.join(function_calls)}")
        else:
            label_parts.append("No tool calls")

        return "<br>".join(label_parts)

    def walk(node, parent=None, condition=None):
        if node in visited:
            return parent and link(parent, get_id(node), condition)
        visited.add(node)
        if isinstance(node, Flow):
            node.start_node and parent and link(
                parent, get_id(node.start_node), condition
            )
            lines.append(
                f"\n    subgraph sub_flow_{get_id(node)}[{type(node).__name__}]"
            )
            node.start_node and walk(node.start_node)
            for cond, successors in node.successors.items():
                for succ in successors:
                    node.start_node and walk(succ, get_id(node.start_node), cond) or (
                        parent and link(parent, get_id(succ), cond)
                    ) or walk(succ, None, cond)
            lines.append("    end\n")
        else:
            node_id = get_id(node)
            label = get_node_label(node)
            logger.debug(f"Creating node with label: {label}")

            # Choose node shape based on node type
            if isinstance(node, BatchNode):
                lines.append(f'    {node_id}@{{shape: procs, label: "{label}"}}')
            elif isinstance(node, StartNode):
                lines.append(f'    {node_id}@{{shape: circle, label: "{label}"}}')
            elif isinstance(node, TerminateNode):
                lines.append(f'    {node_id}@{{shape: doublecircle, label: "{label}"}}')
            else:
                # For regular nodes, use standard rectangle
                lines.append(f"    {node_id}[{label}]")

            parent and link(parent, node_id, condition)
            if hasattr(node, "successors"):
                for cond, successors in node.successors.items():
                    for succ in successors:
                        walk(succ, node_id, cond)

    walk(start)
    print("\n".join(lines))
    return "\n".join(lines)
