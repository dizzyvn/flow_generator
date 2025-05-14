import subprocess
from typing import Tuple


def is_docker_available() -> bool:
    """Check if Docker is available on the system."""
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_python_run_instructions(sandbox_dir: str) -> str:
    """Generate instructions for running the code directly in Python."""
    return f"""
To run the application directly in Python:
1. cd {sandbox_dir}
2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   # OR
   .\\venv\\Scripts\\activate  # On Windows
3. Install dependencies:
   pip install -r requirements.txt
4. Run the application:
   python main.py
"""


def build_docker_image(sandbox_dir: str) -> Tuple[bool, str, str]:
    """
    Build Docker image in the specified directory.
    Returns: (success, run_command, error_message)
    """
    try:
        result = subprocess.run(
            ["docker", "build", "-t", "execution", "."],
            cwd=sandbox_dir,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            return True, "docker run -it --env-file .env execution", ""
        return False, "", result.stderr
    except Exception as e:
        return False, "", str(e)
