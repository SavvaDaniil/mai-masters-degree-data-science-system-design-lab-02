from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import Message

from logging import Logger, getLogger

class MessageRepository():

    def __init__(self):
        self.logger: Logger = getLogger()

    def find_by_id(self, id: int) -> Message:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(Message).filter(Message.id == id).order_by(Message.id).first()
        finally:
            session.close()
            
        return obj
    
    
    def add(self, obj: Message) -> Message:
        session = ApplicationDbContext.create_session()
        session.add(obj)
        session.commit()
        session.refresh(obj)
        session.close()
        return obj
    

    def update(self, message: Message) -> bool:
        session = ApplicationDbContext.create_session()
        try: 
            session.query(Message)\
                .filter(Message.id == message.id)\
                .update({
                    Message.content : message.content,
                    Message.date_of_created : message.date_of_created,
                    Message.date_of_add : message.date_of_add,

                }, synchronize_session = False)
            session.commit()
        except Exception as e:
            self.logger.error("update Exception: " + str(e))
            return False
        finally:
            session.close()
            
        return True
    