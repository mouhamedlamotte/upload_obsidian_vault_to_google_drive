# Specify the python executable to use
# !./venv/bin/python3

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive



class GoogleDriveManager():
    def __init__(self):
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)
        self.folder_id = "automations"

    def get_folder_by_name(self, folderName):
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            if file['title'] == folderName:
                return file['id']
        return None

    def authenticate(self):
        self.gauth.LocalWebserverAuth()

    def create_folder(self, folderName):
        folder_id = self.get_folder_by_name(folderName)
        if folder_id:
            print(f"Folder {folderName} already exists")
            return

        file_metadata = {
            'title': folderName,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        folder = self.drive.CreateFile(file_metadata)
        folder.Upload()

if __name__ == "__main__":
    gd = GoogleDriveManager()
    gd.create_folder("test_folder")
