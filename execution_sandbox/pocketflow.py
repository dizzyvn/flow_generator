import copy
import time
import warnings


def print_node_io(node_name, input_data, output_data):
    """Print node input and output in a clean format."""
    print(f"\n{'=' * 20} Node: {node_name} {'=' * 20}")
    print("\nInput:")
    if isinstance(input_data, list):
        for i, item in enumerate(input_data):
            print(f"  {i + 1}. {item}")
    else:
        print(f"  {input_data}")

    print("\nOutput:")
    if isinstance(output_data, list):
        for i, item in enumerate(output_data):
            print(f"  {i + 1}. {item}")
    else:
        print(f"  {output_data}")


class BaseNode:
    def __init__(self):
        self.params = {}
        self.successors = {}  # Keep as dict but store lists of nodes

    def set_params(self, params):
        self.params = params

    def next(self, node, action="default"):
        if action not in self.successors:
            self.successors[action] = []
        self.successors[action].append(node)
        return node

    def prep(self, shared):
        pass

    def exec(self, prep_res):
        pass

    def post(self, shared, prep_res, exec_res):
        pass

    def _exec(self, prep_res):
        return self.exec(prep_res)

    def _run(self, shared):
        try:
            # Run prep phase
            p = self.prep(shared)

            # Run exec phase
            e = self._exec(p)
            print_node_io(self.__class__.__name__, p, e)

            # Run post phase
            r = self.post(shared, p, e)

            return r

        except Exception as e:
            raise e

    def run(self, shared):
        if self.successors:
            warnings.warn("Node won't run successors. Use Flow.")
        return self._run(shared)

    def __rshift__(self, other):
        return self.next(other)

    def __sub__(self, action):
        if isinstance(action, str):
            return _ConditionalTransition(self, action)
        raise TypeError("Action must be a string")


class _ConditionalTransition:
    def __init__(self, src, action):
        self.src, self.action = src, action

    def __rshift__(self, tgt):
        return self.src.next(tgt, self.action)


class Node(BaseNode):
    def __init__(self, max_retries=1, wait=0):
        super().__init__()
        self.max_retries, self.wait = max_retries, wait

    def exec_fallback(self, prep_res, exc):
        raise exc

    def _exec(self, prep_res):
        for self.cur_retry in range(self.max_retries):
            try:
                return self.exec(prep_res)
            except Exception as e:
                if self.cur_retry == self.max_retries - 1:
                    return self.exec_fallback(prep_res, e)
                if self.wait > 0:
                    time.sleep(self.wait)

    def _run(self, shared):
        try:
            p = self.prep(shared)
            e = self._exec(p)
            print_node_io(self.__class__.__name__, p, e)
            r = self.post(shared, p, e)
            return r
        except Exception as e:
            raise e


class TerminateNode(Node):
    pass


class BatchNode(Node):
    def _exec(self, items):
        return [super(BatchNode, self)._exec(i) for i in (items or [])]


class Flow(BaseNode):
    def __init__(self, start=None):
        super().__init__()
        self.start_node = start

    def start(self, start):
        self.start_node = start
        return start

    def get_next_nodes(self, curr, action):
        # Get all next nodes for the action
        action = action or "default"  # Ensure we use "default" instead of None
        next_nodes = curr.successors.get(action, [])

        if not next_nodes and curr.successors:
            warnings.warn(f"Flow ends: '{action}' not found in {list(curr.successors)}")

        return next_nodes

    def _build_dependency_graph(self, action_map):
        # Build a graph of node dependencies based on the actual actions taken
        dependencies = {}  # node -> set of nodes that must complete before this node
        reverse_deps = {}  # node -> set of nodes that depend on this node

        def add_dependency(node, action=None):
            if node not in dependencies:
                dependencies[node] = set()
            if node not in reverse_deps:
                reverse_deps[node] = set()

            # If we have an action from the action_map, use it
            # Otherwise, add dependencies for all possible actions
            actions = [action] if action else node.successors.keys()

            for curr_action in actions:
                for succ in node.successors.get(curr_action, []):
                    if succ not in dependencies:
                        dependencies[succ] = set()
                    if succ not in reverse_deps:
                        reverse_deps[succ] = set()
                    dependencies[succ].add(node)
                    reverse_deps[node].add(succ)
                    # Recursively add dependencies for this successor
                    add_dependency(succ)

        # Start with the start node's action if we have it
        start_action = action_map.get(self.start_node)
        add_dependency(self.start_node, start_action)
        return dependencies, reverse_deps

    def _orch(self, shared, params=None):
        # First pass: execute nodes and collect actions
        action_map = {}  # node -> action returned by post
        p = params or {**self.params}

        def execute_node(node):
            if node in action_map:  # Skip if already executed
                return

            node_copy = copy.copy(node)
            node_copy.set_params(p)
            prep_res = node_copy.prep(shared)
            exec_res = node_copy._exec(prep_res)
            print_node_io(node_copy.__class__.__name__, prep_res, exec_res)
            action = node_copy.post(shared, prep_res, exec_res)
            action = action or "default"  # Ensure we use "default" instead of None
            action_map[node] = action
            return action

        # Execute start node first
        execute_node(self.start_node)

        # Build dependency graph based on actual actions taken
        dependencies, reverse_deps = self._build_dependency_graph(action_map)

        # Initialize execution state
        completed_nodes = {self.start_node}
        ready_nodes = []

        # Find initial ready nodes (nodes that only depend on start node)
        for node in dependencies:
            if dependencies[node].issubset(completed_nodes):
                ready_nodes.append(node)

        # Process nodes in dependency order
        while ready_nodes:
            # Process all ready nodes
            for node in ready_nodes:
                if node not in completed_nodes:
                    execute_node(node)
                    completed_nodes.add(node)

            # Find new ready nodes
            ready_nodes = []
            for node in completed_nodes:
                for dependent in reverse_deps.get(node, set()):
                    if all(dep in completed_nodes for dep in dependencies[dependent]):
                        ready_nodes.append(dependent)

            # Remove duplicates and already completed nodes
            ready_nodes = list(set(ready_nodes) - completed_nodes)

        return action_map.get(self.start_node)

    def _run(self, shared):
        p = self.prep(shared)
        o = self._orch(shared)
        r = self.post(shared, p, o)
        return r

    def post(self, shared, prep_res, exec_res):
        return exec_res


class BatchFlow(Flow):
    def _run(self, shared):
        pr = self.prep(shared) or []
        for bp in pr:
            self._orch(shared, {**self.params, **bp})
        return self.post(shared, pr, None)
