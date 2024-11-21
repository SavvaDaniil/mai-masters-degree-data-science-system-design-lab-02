
from internal.data.ApplicationMongoDbContext import ApplicationMongoDbContext
from internal.entity.User import User
from internal.factory.UserFactory import UserFactory
from typing import List, Union
from bson.objectid import ObjectId
#from sqlalchemy import or_

from logging import Logger, getLogger

class UserRepository():

    
    def __init__(self) -> None:
        self.__table_name = "user"

    def find_by_id(self, id: str) -> User:
        dbc_client = ApplicationMongoDbContext()
        db = dbc_client.get_database()
        collection = db[self.__table_name]

        query_result = collection.find_one({"_id" : ObjectId(id)})
        #print("query_result")
        #print(query_result)
        if query_result is None:
            return None

        userFactory: UserFactory = UserFactory()
        user: User = userFactory.create_from_row(query_result)

        dbc_client.close()
        return user
    
    def find_by_username(self, username: str) -> User:
        dbc_client = ApplicationMongoDbContext()
        db = dbc_client.get_database()
        collection = db[self.__table_name]

        query_result = collection.find_one({"username" : username})
        #print("query_result")
        #print(query_result)
        if query_result is None:
            return None

        userFactory: UserFactory = UserFactory()
        user: User = userFactory.create_from_row(query_result)

        dbc_client.close()
        return user
    
    def list_all(self) -> List[User]:
        dbc_client = ApplicationMongoDbContext()
        db = dbc_client.get_database()
        collection = db[self.__table_name]

        query_results = collection.find()
        if query_results is None:
            return None

        userFactory: UserFactory = UserFactory()
        users: List[User] = []
        for query_result in query_results:
            users.append(userFactory.create_from_row(query_result))

        dbc_client.close()
        return users

    def add(self, user: User) -> None:
        if user is None:
            raise Exception("user is None")

        dbc_client = ApplicationMongoDbContext()
        db = dbc_client.get_database()
        collection = db[self.__table_name]

        insert_query = {
            "username" : user.username,
            "password" : user.password,
            "auth_key" : user.auth_key,
            "access_token" : user.access_token,
            "is_active" : user.is_active,
            "lastname" : user.lastname,
            "firstname" : user.firstname,
            "date_of_add" : user.date_of_add
        }

        inserted_id = collection.insert_one(insert_query)
        #print("type of inserted_id: " + str(type(inserted_id)))
        user._id = inserted_id
        dbc_client.close()


    def update(self, user: User) -> None:
        
        dbc_client = ApplicationMongoDbContext()
        db = dbc_client.get_database()
        collection = db[self.__table_name]

        #print("update VKUser._id: " + str(VKUser._id))
        filter = {
            "_id" : ObjectId(user._id)
        }
        #print("update comments_count: " + str(VKUser.comments_count))
        update_query = { 
            "$set" : {
                "username" : user.username,
                "password" : user.password,
                "auth_key" : user.auth_key,
                "access_token" : user.access_token,
                "is_active" : user.is_active,
                "lastname" : user.lastname,
                "firstname" : user.firstname,
                "date_of_add" : user.date_of_add
            }
        }

        collection.update_one(filter, update_query)
        dbc_client.close()

    def search(self, skip: int, take: int, query_strs: Union[List[str], None]) -> List[User]:
        dbc_client = ApplicationMongoDbContext()
        db = dbc_client.get_database()
        collection = db[self.__table_name]

        if query_strs is not None and len(query_strs) > 0:

            # query_results = collection.find({"$or" : [
            #     {"lastname" : {'$in' : query_strs}},
            #     {"username" : {'$in' : query_strs}},
            #     {"firstname" : {'$in' : query_strs}}
            # ]}).skip(skip).limit(take)

            query_results = collection.find({"$or" : [
                {"username" : {'$regex' : "|".join(query_strs)}},
                {"lastname" : {'$regex' : "|".join(query_strs)}},
                {"firstname" : {'$regex' : "|".join(query_strs)}}
            ]}).skip(skip).limit(take)
        else:
            query_results = collection.find().skip(skip).limit(take)
        userFactory: UserFactory = UserFactory()
        users: List[User] = []
        for query_result in query_results:
            users.append(userFactory.create_from_row(query_result))

        dbc_client.close()

        return users
        
    
    """
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
    """
    