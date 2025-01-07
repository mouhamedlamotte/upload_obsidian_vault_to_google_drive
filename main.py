from constants import LOCAL_VAULT
from goodeDriveManagement import GoogleDriveManager
from utils import getFilesNfolders, getFullPath
import uuid


class Sync():
    def __init__(self, vaultName) :
        self.drive = GoogleDriveManager()
        self.vaultId = self.drive.getId(vaultName)
        self.vault_dir = self.drive.list_dir(self.vaultId)

    def syncFiles(self, local_files, remote_files, parentsIds : list[str] | None =None) :

        print("local_files", local_files)
        print("remote_files", remote_files)
        remote_files_titles = [file.get('title') for file in remote_files]
        for file in local_files :
            if file.get('title') not in remote_files_titles :
                newFile = self.drive.create_file(file.get('title'), parentsIds)
                if newFile:
                    newFile.SetContentFile(getFullPath(LOCAL_VAULT.get("baseDir"), [file.get('title')]))
                    newFile.Upload()
            else :
                print("file already exist")

     # TODO : remove files
    def syncFolders(self, local_folders, remote_folders, parentsIds : list[str] | None =None):
        remote_folders_titles = [folder.get('title') for folder in remote_folders]
        for folder in local_folders:
            if folder.get('title') not in   remote_folders_titles :
                self.drive.create_folder(folder.get('title'), parentsIds)

    def sync(self):
        folders, files = getFilesNfolders.getFilesAndFolders()
        remote_folders = [folder for folder in self.vault_dir if folder.get('type') == "folder"]
        remote_files = [file for file in self.vault_dir if file.get('type') == "file"]
        self.syncFiles(files, remote_files, [self.vaultId])
        # self.syncFolders(folders, remote_folders, [self.vaultId])



sync = Sync("Obsidian")
sync.sync()