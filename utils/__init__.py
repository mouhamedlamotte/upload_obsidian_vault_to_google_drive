import os

def getFullPath (baseDir, filepaths = list[str]) :
    return os.path.join(baseDir, *filepaths)