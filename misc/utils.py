import os 

def list_absolute_file_paths(path):
    return [os.path.join(path, file) for file in os.listdir(path)]