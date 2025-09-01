import os
import subprocess

def run_protoc():
    """Run the protoc command to generate Python files from .proto definitions."""
    commands = [
        "python -m grpc_tools.protoc -Iprotos --python_out=gateway/generated --grpc_python_out=gateway/generated protos/fusion/v1/detections.proto",
        "python -m grpc_tools.protoc -Iprotos --python_out=gateway/generated protos/fusion/v1/observations.proto"
    ]

    for command in commands:
        print(f"Running: {command}")
        subprocess.run(command, shell=True, check=True)

def create_init_files():
    """Create __init__.py files in the necessary directories."""
    init_files = [
        "gateway/generated/__init__.py",
        "gateway/generated/fusion/__init__.py",
        "gateway/generated/fusion/v1/__init__.py"
    ]

    for file_path in init_files:
        if not os.path.exists(file_path):
            print(f"Creating: {file_path}")
            open(file_path, 'a').close()

def main():
    run_protoc()
    create_init_files()

if __name__ == "__main__":
    main()
