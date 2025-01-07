import os
import os
from constants import LOCAL_VAULT
import uuid

from datetime import datetime

def getFullPath (baseDir, filepaths = list[str]) :
    return os.path.join(baseDir, *filepaths)



def getFilesAndFolders(folder_path = LOCAL_VAULT) :
    folders = [{
    "id": str(uuid.uuid4()),
    "title": folder,
    "edit_date": datetime.fromtimestamp(os.path.getmtime(os.path.join(folder_path, folder))).strftime("%Y-%m-%d %H:%M:%S"),
    "type": "folder"
} for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder)) ]
    files = [{
    "id": str(uuid.uuid4()),
    "title": file,
    "edit_date": datetime.fromtimestamp(os.path.getmtime(os.path.join(folder_path, file))).strftime("%Y-%m-%d %H:%M:%S"),
    "type": "file"
} for file in os.listdir(folder_path) if not os.path.isdir(os.path.join(folder_path, file)) ]
    return folders, files