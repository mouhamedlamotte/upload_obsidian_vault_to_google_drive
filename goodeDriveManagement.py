from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive



class GoogleDriveManager():
    def __init__(self):
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)
        self.folder_id = "automations"


    def authenticate(self):
        self.gauth.LocalWebserverAuth()

    def create_file(self, fileName, parentsIds : list[str] | None =None):
        for id in parentsIds :
            print("id", id)
            if (self.getId(fileName, id)):
                print("file already exist")
                return

        file_metadata = {
            'title': fileName,
        }

        if parentsIds :
            file_metadata["parents"] = [{
                'kind': 'drive#fileLink',
                "id" : p_id
            } for p_id in parentsIds]

        print(file_metadata)

        file = self.drive.CreateFile(file_metadata)
        file.Upload()
        return file

    def create_folder(self, folderName, parentsIds : list[str] | None =None):
        if (self.getId(folderName)):
            print("folder already exist")
            return

        file_metadata = {
            'title': folderName,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        if parentsIds :
            file_metadata["parents"] = [{
                'kind': 'drive#fileLink',
                "id" : p_id
            } for p_id in parentsIds]


        folder = self.drive.CreateFile(file_metadata)
        folder.Upload()
        return folder

    def getId(self, folderName, parentsId : str ='root') :
        q = f"'{parentsId}' in parents and trashed=false"
        folders = self.drive.ListFile({'q': q}).GetList()
        try :
            return  [file["id"] for file in folders if file["title"] == folderName][0]
        except :
            return

    def list_dir(self, folderId) :
        return self.drive.ListFile({'q': f"'{folderId}' in parents and trashed=false"}).GetList()