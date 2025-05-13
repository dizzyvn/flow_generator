import os
import subprocess
from typing import Any, Dict

from pocketflow import Node


class ExecuteCode(Node):
    def prep(self, shared: Dict[str, Any]) -> tuple:
        """Get the sandbox directory and generated code files."""
        sandbox_dir = shared["execution_sandbox_dir"]
        generated_code_files = shared["generated_code_files"]
        return sandbox_dir, generated_code_files

    def exec(self, inputs: tuple) -> Dict[str, Any]:
        """Execute the generated code files."""
        sandbox_dir, generated_code_files = inputs
        print(f"\n4. Executing code in sandbox directory: {sandbox_dir}")

        # Change to the sandbox directory
        original_dir = os.getcwd()
        os.chdir(sandbox_dir)

        try:
            # Execute main.py if it exists
            if "main.py" in generated_code_files:
                result = subprocess.run(
                    ["python", "main.py"], capture_output=True, text=True
                )
                print(f"Return code: {result.returncode}")
                if result.returncode != 0:
                    print(f"Error:\n{result.stderr}")
                print(f"Output:\n{result.stdout}")
                return {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode,
                }
            else:
                print("No main.py found in generated files")
                return {
                    "stdout": "",
                    "stderr": "No main.py found in generated files",
                    "returncode": 1,
                }
        finally:
            # Change back to original directory
            os.chdir(original_dir)

    def post(
        self,
        shared: Dict[str, Any],
        prep_res: tuple,
        exec_res: Dict[str, Any],
    ) -> str:
        """Store the execution results in shared store."""
        shared["execution_results"] = exec_res
        return "default"
