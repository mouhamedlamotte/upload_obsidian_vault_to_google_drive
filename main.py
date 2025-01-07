from constants import LOCAL_VAULT
from goodeDriveManagement import GoogleDriveManager
from utils import getFilesAndFolders, getFullPath
import uuid


class Sync():
    def __init__(self, vaultName) :
        self.drive = GoogleDriveManager()
        self.vaultId = self.drive.getId(vaultName)
        self.vault_dir = self.drive.list_dir(self.vaultId)

    def syncFiles(self, local_files, remote_files, parentsIds : list[str] | None =None, vaultpath='') :

        remote_files_titles = [file.get('title').split("--")[1] for file in remote_files]
        for file in local_files :
            if file.get('title') not in remote_files_titles :
                title = "{}--{}".format( file.get('edit_date'), file.get('title'))
                newFile = self.drive.create_file(title, parentsIds)
                if newFile:
                    newFile.SetContentFile(getFullPath(vaultpath, [file.get('title')]))
                    newFile.Upload()
            else :
                local_edit_date = file.get('edit_date')
                remote_edit_date = [f.get('title').split('--')[0] for f in remote_files if f.get('title').split('--')[1] == file.get('title')][0]
                remote_id = [f.get('id') for f in remote_files if f.get('title').split('--')[1] == file.get('title')][0]
                if local_edit_date != remote_edit_date :
                    content = getFullPath(vaultpath, [file.get('title')])
                    new_title = "{}--{}".format( file.get('edit_date'), file.get('title'))
                    self.drive.update_file(remote_id, content, new_title, parentsIds[0])

    def syncFolders(self, local_folders, remote_folders, parentsIds : list[str] | None =None):
        remote_folders_titles = [folder.get('title').split('--')[1] for folder in remote_folders]
        for folder in local_folders:
            if folder.get('title') not in   remote_folders_titles :
                title = "{}--{}".format(folder.get('edit_date'),folder.get('title'))
                self.drive.create_folder(title, parentsIds)

    def sync(self,vaultId, remote_folders, local_folders, remote_files, local_files, vaultpath=''):
        self.syncFolders(local_folders, remote_folders, [vaultId])
        self.syncFiles(local_files, remote_files, [vaultId], LOCAL_VAULT + vaultpath)


        for folder in local_folders :
            current_vaultpath = '{}/{}'.format(vaultpath, folder.get('title'))
            path = LOCAL_VAULT + current_vaultpath
            local_folders, local_files = getFilesAndFolders(path)
            title = "{}--{}".format(folder.get('edit_date'),folder.get('title'))
            remote_folder_id = self.drive.getId(title, vaultId)
            if remote_folder_id :
                remote_folders = [folder for folder in self.drive.list_dir(remote_folder_id) if folder.get('type') == "folder"]
            else :
                remote_folders = []
            self.sync(remote_folder_id, remote_folders, local_folders, remote_files, local_files, current_vaultpath)

    def run(self):
        local_folders, local_files = getFilesAndFolders()
        remote_folders =  [folder for folder in self.vault_dir if folder.get('type') == "folder"]
        remote_files = [file for file in self.vault_dir if file.get('type') == "file"]
        self.sync(self.vaultId,remote_folders, local_folders, remote_files, local_files)

if __name__ == "__main__":
    app = Sync('Obsidian')
    app.run()