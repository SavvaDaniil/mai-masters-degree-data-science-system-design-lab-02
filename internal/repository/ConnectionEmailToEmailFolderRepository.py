
from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import ConnectionEmailToEmailFolder
from typing import List, Union
from sqlalchemy import or_

from logging import Logger, getLogger


class ConnectionEmailToEmailFolderRepository:

    def __init__(self):
        self.logger: Logger = getLogger()

    def find_by_id(self, id: int) -> ConnectionEmailToEmailFolder:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(ConnectionEmailToEmailFolder).filter(ConnectionEmailToEmailFolder.id == id).order_by(ConnectionEmailToEmailFolder.id).first()
        finally:
            session.close()
            
        return obj

    def find_by_email_id_with_email_folder_id(self, email_id: int, email_folder_id: int) -> ConnectionEmailToEmailFolder:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(ConnectionEmailToEmailFolder).filter(ConnectionEmailToEmailFolder.email_id == email_id, ConnectionEmailToEmailFolder.email_folder_id == email_folder_id).order_by(ConnectionEmailToEmailFolder.id.desc()).first()
        finally:
            session.close()
            
        return obj

    def list_by_email_folder_id(self, email_folder_id: int) -> List[ConnectionEmailToEmailFolder]:
        objs = None
        session = ApplicationDbContext.create_session()

        try: 
            objs = session.query(ConnectionEmailToEmailFolder).filter(ConnectionEmailToEmailFolder.email_folder_id == email_folder_id).order_by(ConnectionEmailToEmailFolder.id.desc()).all()
        finally:
            session.close()
            
        return objs
    
    
    def add(self, obj: ConnectionEmailToEmailFolder) -> ConnectionEmailToEmailFolder:
        session = ApplicationDbContext.create_session()
        session.add(obj)
        session.commit()
        session.refresh(obj)
        session.close()
        return obj
    

    def update(self, connectionEmailToEmailFolder: ConnectionEmailToEmailFolder) -> bool:
        session = ApplicationDbContext.create_session()
        try: 
            session.query(ConnectionEmailToEmailFolder)\
                .filter(ConnectionEmailToEmailFolder.id == connectionEmailToEmailFolder.id)\
                .update({
                    ConnectionEmailToEmailFolder.email_id : connectionEmailToEmailFolder.email_id,
                    ConnectionEmailToEmailFolder.email_folder_id : connectionEmailToEmailFolder.email_folder_id,
                    ConnectionEmailToEmailFolder.date_of_add : connectionEmailToEmailFolder.date_of_add,

                }, synchronize_session = False)
            session.commit()
        except Exception as e:
            self.logger.error("update Exception: " + str(e))
            return False
        finally:
            session.close()
            
        return True
    
    def delete(self, obj: ConnectionEmailToEmailFolder) -> None:
        session = ApplicationDbContext.create_session()
        session.delete(obj)
        session.commit()
