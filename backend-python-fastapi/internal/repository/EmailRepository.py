
from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import Email
from typing import List, Union
from sqlalchemy import or_

from logging import Logger, getLogger


class EmailRepository:

    def __init__(self):
        self.logger: Logger = getLogger()

    def find_by_id(self, id: int) -> Email:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(Email).filter(Email.id == id).order_by(Email.id).first()
        finally:
            session.close()
            
        return obj

    def find_by_code(self, code: str) -> Email:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(Email).filter(Email.code == code).order_by(Email.id).first()
        finally:
            session.close()
            
        return obj
    
    
    def add(self, obj: Email) -> Email:
        session = ApplicationDbContext.create_session()
        session.add(obj)
        session.commit()
        session.refresh(obj)
        session.close()
        return obj
    

    def update(self, email: Email) -> bool:
        session = ApplicationDbContext.create_session()
        try: 
            session.query(Email)\
                .filter(Email.id == email.id)\
                .update({
                    Email.code : email.code,
                    Email.user_from_id : email.user_from_id,
                    Email.user_to_id : email.user_to_id,
                    Email.subject : email.subject,
                    Email.text_message : email.text_message,

                    Email.is_sent : email.is_sent,
                    Email.date_of_add  : email.date_of_add,
                    Email.date_of_sent : email.date_of_sent,

                }, synchronize_session = False)
            session.commit()
        except Exception as e:
            self.logger.error("update Exception: " + str(e))
            return False
        finally:
            session.close()
            
        return True