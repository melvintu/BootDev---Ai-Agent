import os

def get_files_info(working_directory, directory="."):
    
    #joined_path = os.path.join(working_directory, directory)

    if directory.startswith("/"):
        removed_slash = directory.replace("/", "")
        joined_path = os.path.join(working_directory, removed_slash)
    else:
        added_slash = f"/{directory}"
        joined_path = os.path.join(working_directory, added_slash)
        #print(joined_path)

    #print(full_path, "this is the full path")
    if os.path.isdir(joined_path):
        print("not a directory", joined_path)
        return f'Error: "{directory}" is not a directory'
    else:
        print(joined_path, "is a directory")
    
    
   # if working_directory not in os.path.abspath(joined_path):
        #print("outside working directory", os.path.abspath(joined_path))
        #return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    

    #print(True, joined_path)
    #items = os.listdir(directory) #creates a list of each item in the directory
    #contents = {}
    #for item in items:
     #   if os.path.isfile(item):
      #      print(True)
       #     return
