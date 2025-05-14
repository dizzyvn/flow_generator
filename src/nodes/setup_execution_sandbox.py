import os
from typing import Any, Dict

from pocketflow import Node

from src.utils.docker_utils import (
    build_docker_image,
    get_python_run_instructions,
    is_docker_available,
)


class SetupExecutionSandbox(Node):
    def prep(self, shared: Dict[str, Any]) -> tuple:
        """Get the execution sandbox directory path and generated code files."""
        sandbox_dir = shared["execution_sandbox_dir"]
        generated_code_files = shared["generated_code_files"]
        return sandbox_dir, generated_code_files

    def exec(self, inputs: tuple) -> Dict[str, Any]:
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
            target_dir = (
                os.path.join(sandbox_dir, "nodes")
                if "node" in filename
                else sandbox_dir
            )
            filepath = os.path.join(target_dir, filename)
            with open(filepath, "w") as f:
                f.write(content)
            files_written[filename] = True

        # Try Docker if available, otherwise provide Python instructions
        if is_docker_available():
            print("\nBuilding Docker image...")
            success, run_command, error = build_docker_image(sandbox_dir)
            if success:
                print("Docker image built successfully!")
                return {
                    "files_written": files_written,
                    "docker_available": True,
                    "docker_build_success": True,
                    "run_command": run_command,
                }
            print(f"Error building Docker image:\n{error}")

        # Provide Python instructions if Docker is not available or build failed
        python_instructions = get_python_run_instructions(sandbox_dir)
        print(python_instructions)
        return {
            "files_written": files_written,
            "docker_available": is_docker_available(),
            "docker_build_success": False,
            "python_instructions": python_instructions,
        }

    def post(
        self,
        shared: Dict[str, Any],
        prep_res: tuple,
        exec_res: Dict[str, Any],
    ) -> str:
        """Store the setup results in shared store."""
        shared["sandbox_setup_results"] = exec_res
        if exec_res.get("docker_build_success"):
            print("\nTo run the application, use this command:")
            print(exec_res["run_command"])
        else:
            print("\nTo run the application, follow these steps:")
            print(exec_res["python_instructions"])
        return "default"
