import os
from typing import Any, Dict

from pocketflow import Node


class SetupExecutionSandbox(Node):
    def prep(self, shared: Dict[str, Any]) -> tuple:
        """Get the execution sandbox directory path and generated code files."""
        sandbox_dir = shared["execution_sandbox_dir"]
        generated_code_files = shared["generated_code_files"]
        return sandbox_dir, generated_code_files

    def exec(self, inputs: tuple) -> Dict[str, bool]:
        """Set up the execution sandbox directory structure and write generated code files."""
        sandbox_dir, generated_code_files = inputs
        print(f"\n3. Setting up execution sandbox in directory: {sandbox_dir}")

        # Create nodes directory if not exists, and clean up nodes
        os.makedirs(os.path.join(sandbox_dir, "nodes"), exist_ok=True)
        for file in os.listdir(os.path.join(sandbox_dir, "nodes")):
            if file.endswith(".py"):
                os.remove(os.path.join(sandbox_dir, "nodes", file))

        # Write generated code files to appropriate directories
        files_written = {}
        for filename, content in generated_code_files.items():
            # Determine the target directory based on the file type
            if "node" in filename:
                target_dir = os.path.join(sandbox_dir, "nodes")
            else:
                target_dir = sandbox_dir

            # Write the file
            filepath = os.path.join(target_dir, filename)
            with open(filepath, "w") as f:
                f.write(content)
            files_written[filename] = True

        print(f"Setup complete. Files written: {len(files_written)}")
        return {
            "files_written": files_written,
        }

    def post(
        self,
        shared: Dict[str, Any],
        prep_res: tuple,
        exec_res: Dict[str, bool],
    ) -> str:
        """Store the setup results in shared store."""
        shared["sandbox_setup_results"] = exec_res
        return "default"
