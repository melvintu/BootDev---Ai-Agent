import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if abs_file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    commands = ["python", abs_file_path]
    try: 
        if args:
            commands.extend(args)
        completed_process = subprocess.run(commands,
                                           timeout=30, 
                                           capture_output=True,
                                           text=True,
                                           cwd=abs_working_dir
                                           )
        output = []
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}" 
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory path to the file which needs to be written into with the new string content",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="A list of arguments to be passed into the run_python_file, remain empty if no arguments are passed",
            ),
        },
    ),
    )