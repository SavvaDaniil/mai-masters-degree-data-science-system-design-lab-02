
from internal.data.ApplicationDbContext import ApplicationDbContext
from internal.Entities import User
from typing import List, Union
from sqlalchemy import or_

from logging import Logger, getLogger


class UserRepository():

    def __init__(self):
        self.logger: Logger = getLogger()

    def find_by_id(self, id: int) -> User:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(User).filter(User.id == id).order_by(User.id).first()
        finally:
            session.close()
            
        return obj
    
    def find_by_username(self, username: str) -> User:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(User).filter(User.username == username).order_by(User.id).first()
        finally:
            session.close()
            
        return obj
    
    def find_by_username_except_user_id(self, username: str, user_id: int) -> User:
        obj = None
        session = ApplicationDbContext.create_session()

        try: 
            obj = session.query(User).filter((User.username == username) & (User.id != user_id)).order_by(User.id).first()
        finally:
            session.close()
            
        return obj

    def search(self, skip: int, take: int, query_strs: Union[List[str], None]) -> List[User]:
        objs = None
        session = ApplicationDbContext.create_session()
        try: 
            objs = session.query(User)

            if query_strs is not None and len(query_strs) > 0:
                for query_string in query_strs:
                    query_string = "%" + query_string + "%"
                    objs = objs.filter(or_(User.username.like(query_string), User.lastname.like(query_string), User.firstname.like(query_string)))
                
            objs = objs.order_by(User.id.desc()).offset(skip).limit(take)\
                .all()
        finally:
            session.close()
        return objs
    
    
    def add(self, obj: User) -> User:
        session = ApplicationDbContext.create_session()
        session.add(obj)
        session.commit()
        session.refresh(obj)
        session.close()
        return obj
    

    def update(self, user: User) -> bool:
        session = ApplicationDbContext.create_session()
        try: 
            session.query(User)\
                .filter(User.id == user.id)\
                .update({
                    User.username : user.username,
                    User.password : user.password,
                    User.auth_key : user.auth_key,
                    User.access_token : user.access_token,
                    User.is_active : user.is_active,

                    User.secondname : user.secondname,
                    User.firstname : user.firstname,

                    User.date_of_add  : user.date_of_add,
                }, synchronize_session = False)
            session.commit()
        except Exception as e:
            self.logger.error("update Exception: " + str(e))
            return False
        finally:
            session.close()
            
        return True