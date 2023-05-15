import os
def delete_file(path):
    os.path.isfile(path) and os.remove(path)