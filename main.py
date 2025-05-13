import argparse

from src.flow import create_flow


def parse_args():
    parser = argparse.ArgumentParser(description="Generate code based on requirement")
    parser.add_argument(
        "--requirement",
        type=str,
        help="requirement for code generation",
        default="Send an email to a friend about a place to go in a city.",
    )
    parser.add_argument(
        "--sandbox-dir",
        type=str,
        help="directory for generated code",
        default="execution_sandbox",
    )
    return parser.parse_args()


def main():
    # Parse command line arguments
    args = parse_args()

    def read_file_content(file_path):
        with open(file_path, "r") as file:
            return file.read()

    # Read PocketFlow documentation from file
    pocketflow_doc = read_file_content("src/prompt/pocketflow_doc.txt")

    # Initialize shared store with required data
    shared = {
        # For WriteCode node
        "requirement": args.requirement,
        "pocketflow_doc_str": pocketflow_doc,
        "execution_sandbox_dir": args.sandbox_dir,
        "tools_file_path": f"{args.sandbox_dir}/utils/tools.py",
    }

    # Create and run the flow
    main_flow = create_flow()
    main_flow.run(shared)


if __name__ == "__main__":
    main()
