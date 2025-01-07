import os
from goodeDriveManagement import GoogleDriveManager
import json

drive = GoogleDriveManager()

folder_path = "/media/mouhamed/0003-CB5F/notes/obsidian"

list_dir = os.listdir(folder_path)

folders = [file for file in list_dir if os.path.isdir(os.path.join(folder_path, file)) ]
files = [file for file in list_dir if not os.path.isdir(os.path.join(folder_path, file)) ]

print(folders)
print(files)

drive.create_folder("Obsidian")
ObsidianId = drive.getId("Obsidian")

print(ObsidianId)

for file in files :
    print("creating files")
    rmtFile = drive.create_file(file, [ObsidianId])
    if (rmtFile):
        rmtFile.SetContentFile(os.path.join(folder_path, file))
        rmtFile.Upload()

for folder in folders :
    print("creating folders")
    drive.create_folder(folder, [ObsidianId])
    

print(drive.list_dir(ObsidianId)[0])

with open("f.json" , "w") as f :
    json.dump(drive.list_dir(ObsidianId)[0], f)