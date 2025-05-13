import argparse
import os
import subprocess
import tempfile

from flow import create_flow
from utils.build_mermaid import build_mermaid


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate flow diagram")
    parser.add_argument(
        "-o",
        "--output",
        default="flow.png",
        help="Output file path (default: flow.png)",
    )
    args = parser.parse_args()

    # Create and run the flow
    flow = create_flow()
    mermaid_diagram = build_mermaid(flow.start_node)

    # Create a temporary directory and file
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.mmd")

        # Save the diagram to the temporary file
        with open(input_path, "w") as f:
            f.write(mermaid_diagram)

        # Use mmdc to convert to specified format
        try:
            subprocess.run(
                ["mmdc", "-i", input_path, "-o", args.output, "-t png", "-s 3"],
                check=True,
            )
            print(f"Successfully generated {args.output}")
        except subprocess.CalledProcessError as e:
            print(f"Error generating {args.type}: {e}")
        except FileNotFoundError:
            print(
                "Error: mmdc command not found. Please make sure @mermaid-js/mermaid-cli is installed."
            )


if __name__ == "__main__":
    main()
