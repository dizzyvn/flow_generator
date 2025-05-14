from pocketflow import BatchNode, Flow, Node


def build_mermaid(start):
    ids, visited, lines = {}, set(), ["graph TD"]
    ctr = 1

    def get_id(n):
        nonlocal ctr
        return (
            ids[n] if n in ids else (ids.setdefault(n, f"N{ctr}"), (ctr := ctr + 1))[0]
        )

    def link(a, b):
        lines.append(f"    {a} --> {b}")

    def get_node_style(node):
        if isinstance(node, BatchNode):
            return (
                "fill:#ffd700,stroke:#333,stroke-width:2px"  # Gold color for BatchNode
            )
        elif isinstance(node, Node):
            return "fill:#90EE90,stroke:#333,stroke-width:2px"  # Light green for regular Node
        return "fill:#f9f9f9,stroke:#333,stroke-width:2px"  # Default style

    def walk(node, parent=None):
        if node in visited:
            return parent and link(parent, get_id(node))
        visited.add(node)
        if isinstance(node, Flow):
            node.start_node and parent and link(parent, get_id(node.start_node))
            lines.append(
                f"\n    subgraph sub_flow_{get_id(node)}[{type(node).__name__}]"
            )
            node.start_node and walk(node.start_node)
            for nxt in node.successors.values():
                node.start_node and walk(nxt, get_id(node.start_node)) or (
                    parent and link(parent, get_id(nxt))
                ) or walk(nxt)
            lines.append("    end\n")
        else:
            node_id = get_id(node)
            style = get_node_style(node)
            lines.append(f"    {node_id}['{type(node).__name__}']:::node_{node_id}")
            lines.append(f"    classDef node_{node_id} {style}")
            parent and link(parent, node_id)
            [walk(nxt, node_id) for nxt in node.successors.values()]

    walk(start)
    return "\n".join(lines)
