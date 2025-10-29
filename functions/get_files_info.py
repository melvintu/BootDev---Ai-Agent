import os

def get_files_info(working_directory, directory="."):
    
    joined_path = os.path.join(working_directory, directory)

    if os.path.isdir(r"{joined_path}"):
        print("not a directory", joined_path)
        return f'Error: "{directory}" is not a directory'

    if working_directory not in os.path.abspath(joined_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    items = os.listdir(joined_path) # creates a list of each item in the directory
    contents = [] # contains the list of tuples
    
    for item in items:
        item_full_path = os.path.join(joined_path, item)
        if os.path.isfile(item_full_path):
            item_file_size = os.path.getsize(item_full_path)
            contents.append((f"- {item}:", f"file_size={item_file_size}, is_dir=False"))
        else:
            contents.append((f"- {item}:", f"file_size={get_size(joined_path, item)}, is_dir=True"))

    contents_string = '\n'.join(map(lambda x: ' '.join(x), contents))
    if directory == ".":
        return f"Results for current directory:\n{contents_string}"
    else:
        return f"Results for '{directory}' directory:\n{contents_string}"



def get_size(working_directory, start_path='.'):
    total_size = 0

    full_path = os.path.join(working_directory, start_path)
    items = os.listdir(full_path)

    for item in items:
        item_full_path = os.path.join(full_path, item)
        if os.path.isfile(item_full_path):
            total_size += os.path.getsize(item_full_path)

    return total_size