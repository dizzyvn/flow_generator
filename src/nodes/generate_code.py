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

        PocketFlow Documentation:
        {pocketflow_doc}

        Available Tools:
        {tools_doc}

        Design a complete flow that satisfies the requirement following these rules:
        1. Follow PocketFlow's patterns and best practices
        2. Have clear node responsibilities and transitions
        3. Use only the provided tools in node.exec() methods
        4. Each node must follow the three-step pattern: prep(), exec(), post()

        For each node:
        - Pre-processing logic goes in prep()
        - Post-processing logic goes in post()
        - The exec() method of a node MUST USE ONLY ONE of the provided tools. If a step require multiple tools, split it into multiple nodes.
        Which means only the following structure is allowed
        def exec(self, prep_res):
            return selected_tool(prep_res)
        - Name of the node file must end with "_node.py". They will be placed in `nodes` and imported as `from nodes.node_name import NodeName`
        - If the node take a single input, use Node. If the node takes a batch of input, process each item, and return a batch of output, use BatchNode.

        Output Format:
        Your response must contain exactly these files, each wrapped in a code block with the filename:

        ```thinking.txt
        Your thinking process goes here.
        First explain the flow, then explain the nodes, including its description, the node type (Node, BatchNode, etc.), the tool it uses, the inputs and where they come from (from node_name, or from initial shared store), and the outputs.
        ```

        ```node_name.py
        from pocketflow import Node
        from utils.tools import tool_name

        class NodeName(Node):
            def prep(self, shared):
                # Prepare the data for the tool
                return {{"param1": value1, "param2": value2, ...}}

            def exec(self, prep_res):
                return tool_name(**prep_res)

            def post(self, shared, prep_res, exec_res):
                # Describe the data to be returned by post()
                # Always show an example of the data will be written to the shared store
                pass
                
                # Write to shared store and routing if needed
        ```

        ```flow.py
        from pocketflow import Flow
        from nodes.node_name import NodeName

        def create_flow():
            # Create and connect nodes, use the node_name.py file as a reference
            pass
        ```

        ```main.py
        from flow import create_flow
        from utils.logging_config import setup_logging
        setup_logging()        

        def main():        
            # Initialize shared store and run flow
            shared = {{...}}
            flow = create_flow()
            flow.run(shared)

            # Print the result of shared store
            for key, value in shared.items():
                print(f"{{key}}: {{value}}")

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
