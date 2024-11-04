from pydantic import BaseModel

class ConnectionEmailToEmailFolderNewDTO(BaseModel):
    email_id: int
    email_folder_id: int

class ConnectionEmailToEmailFolderDeleteDTO(ConnectionEmailToEmailFolderNewDTO):
    email_id: int
    email_folder_id: int