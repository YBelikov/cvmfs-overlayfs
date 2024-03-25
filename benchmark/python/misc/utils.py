import os 

def list_absolute_file_paths(path):
    return [os.path.join(path, file) for file in os.listdir(path)]

def system(command):
    ret = os.system(command)
    if ret != 0:
        raise RuntimeError("Command failed: " + command)
    return True