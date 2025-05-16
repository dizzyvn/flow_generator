import re

from pocketflow import Node

from src.utils.call_llm import call_llm


class GenerateCode(Node):
    def prep(self, shared):
        return (
            shared["requirement"],
            shared["pocketflow_doc_str"],
            shared["tools_doc_str"],
        )

    def exec(self, inputs):
        requirement, pocketflow_doc, tools_doc = inputs
        print(f"\n2. Generating code for requirement: {requirement[:100]}...")

        system_prompt = f"""
        You are a code generation expert that creates PocketFlow applications. You will be given requirement and must generate a complete flow implementation.

        PocketFlow v2 Documentation:
        {pocketflow_doc}

        Available Tools:
        {tools_doc}

        Design a complete flow that satisfies the requirement following these rules:
        1. Follow PocketFlow v2's patterns and best practices
        2. Have clear node responsibilities and transitions
        3. Use only the provided tools in node.exec() methods
        4. Each node must follow the three-step pattern: prep(), exec(), post()

        For each node:
        - Name of the node file must end with "_node.py". They will be placed in `nodes` and imported as `from nodes.node_name import NodeName`
        - If the node take a single input, use Node. If the node takes a batch of input, process each item, and return a batch of output, use BatchNode.
        - prep() is used to prepare the data for the tool from the shared store and define all parameters of the tool (including constants, prompts...). Some preprocessing can be done here.
        - post() is used to write the data to the shared store and return action to routing.
        - exec() is used to execute the tool. MUST USE ONLY ONE of the provided tools. If a step require multiple tools, split it into multiple nodes.
        - **IMPORTANT** Only the following code is allowed! Only prep_res is used as input! No variable assignment is allowed in exec().
        ```python
        def exec(self, prep_res):
            return selected_tool(prep_res)
        ```
        - All the preprocessing must be done in prep(). Instead of
        ```python
        def prep(self, shared):
            x = shared['x']
            return {{'x': x}}

        def exec(self, prep_res):
            y = prep_res['y']
            return selected_tool(y)
        ```

        Do this:

        ```python
        def prep(self, shared):
            y = shared['x']['y']
            return {{'y': y}}

        def exec(self, prep_res):
            return selected_tool(**prep_res)
        ```

        # Design preference:
        - Activeness: Use conditional branching when the execution of a node depends on the outcome of a previous node.
        - Efficiency: Use parallel branching when nodes can be executed independently to improve performance.
        - Simplicity: Avoid including nodes that do not perform any meaningful action — every node should serve a purpose.

        Output Format:
        Your response must contain exactly these files, each wrapped in a code block with the filename:

        ```thinking.txt
        Your thinking process goes here.
        First explain the flow, then explain the nodes, including its description, the node type (Node, BatchNode, etc.), the tool it uses, the inputs and where they come from (from node_name, or from initial shared store), and the outputs.
        ```

        ```node_name.py
        from pocketflow_v2 import Node        
        from utils.tools import tool_name # Tools is located in `utils/tools.py` !!

        class NodeName(Node):
            def prep(self, shared):
                # Prepare the data for the tool from the shared store. Some preprocessing can be done here
                # Example:
                value1 = ... # from shared store
                value2 = ... # from shared store
                return {{"param1": value1, "param2": value2, ...}}

            # The exec() method of a node MUST USE ONLY ONE of the provided tools, or directly return the prep_res.
            def exec(self, prep_res):
                return tool_name(**prep_res)

            def post(self, shared, pnoderep_res, exec_res):
                # Describe the data to be returned by post(), write it to shared store. Always show an example of the data will be written to the shared store
                # Example:
                # shared["key_1"] = ...
                # shared["key_2"] = ...

                # Also, return action to routing if needed
                # Example:
                if ...:
                    return "action_1"
                else:
                    return "action_2"
        ```

        ```flow.py
        from pocketflow_v2 import Flow, StartNode, TerminateNode
        from nodes.node_name import NodeName

        def create_flow():
            # Create and connect nodes, use the node_name.py file as a reference
            # Explicitly use start_node to start the flow
            # Explicitly use terminate_node to terminate the flow
            terminate_node = TerminateNode()
            start_node = StartNode()

            # Connect nodes
            start_node >> ...
            ...
            ... >> terminate_node

            return Flow(start=start_node) # MUST START WITH START NODE
        ```

        ```main.py
        from flow import create_flow
        from utils.logging_config import setup_logging
        setup_logging()

        def main():
            # Initialize shared store and run flow
            # Simulate all required user's input for the flow here
            shared = {{...}}
            flow = create_flow()
            flow.run(shared)

        if __name__ == "__main__":
            main()
        ```
        """

        user_prompt = f"Requirement: {requirement}"
        response = call_llm(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )

        # Extract code blocks from the response
        try:
            # Find all code blocks with filenames
            code_blocks = re.finditer(
                r"```(\w+\.(?:py|txt))\n(.*?)```", response, re.DOTALL
            )

            generated_code_files = {}
            thinking_text = None

            for match in code_blocks:
                filename = match.group(1)
                content = match.group(2).strip()

                if filename == "thinking.txt":
                    thinking_text = content
                    continue

                generated_code_files[filename] = content

            if not generated_code_files:
                raise ValueError("No Python files found in the response")

            if not thinking_text:
                raise ValueError("No thinking process found in the response")

            print(
                f"Thinking: {thinking_text}\nGenerated {len(generated_code_files)} files: {', '.join(generated_code_files.keys())}"
            )
            return {"files": generated_code_files, "thinking": thinking_text}

        except Exception as e:
            raise ValueError(f"Error parsing code blocks: {str(e)}")

    def post(self, shared, prep_res, exec_res):
        shared["generated_code_files"] = exec_res["files"]
        shared["thinking"] = exec_res["thinking"]
        return "default"
