import os

def get_files_info(working_directory, directory="."):
    
    full_path = os.path.join(working_directory, directory)
    
    print(full_path)
    if os.path.isdir(full_path):
        print("not a directory")
        return f'Error: "{directory}" is not a directory'
    
    if os.path.abspath(full_path) != working_directory:
        print("outside working directory")
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    items = os.listdir(directory) #creates a list of each item in the directory
    contents = {}
    for item in items:
        if os.path.isfile(item):
            print(True)
            return
