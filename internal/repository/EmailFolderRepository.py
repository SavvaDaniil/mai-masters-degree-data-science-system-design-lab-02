
from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import EmailFolder
from typing import List, Union
from sqlalchemy import or_

from logging import Logger, getLogger


class EmailFolderRepository:

    def __init__(self):
        self.logger: Logger = getLogger()

    def find_by_id(self, id: int) -> EmailFolder:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(EmailFolder).filter(EmailFolder.id == id).order_by(EmailFolder.id).first()
        finally:
            session.close()
            
        return obj

    def list_by_user_id(self, user_id: int) -> List[EmailFolder]:
        objs = None
        session = ApplicationDbContext.create_session()
        try: 
            objs = session.query(EmailFolder).filter(EmailFolder.user_id == user_id).order_by(EmailFolder.date_of_add.desc()).all()
        finally:
            session.close()
        return objs
    
    
    def add(self, obj: EmailFolder) -> EmailFolder:
        session = ApplicationDbContext.create_session()
        session.add(obj)
        session.commit()
        session.refresh(obj)
        session.close()
        return obj
    

    def update(self, emailFolder: EmailFolder) -> bool:
        session = ApplicationDbContext.create_session()
        try: 
            session.query(EmailFolder)\
                .filter(EmailFolder.id == emailFolder.id)\
                .update({
                    EmailFolder.user_id : emailFolder.user_id,
                    EmailFolder.title : emailFolder.title,
                    EmailFolder.date_of_add : emailFolder.date_of_add,

                }, synchronize_session = False)
            session.commit()
        except Exception as e:
            self.logger.error("update Exception: " + str(e))
            return False
        finally:
            session.close()
            
        return True
    
    def delete(self, obj: EmailFolder) -> None:
        session = ApplicationDbContext.create_session()
        session.delete(obj)
        session.commit()
