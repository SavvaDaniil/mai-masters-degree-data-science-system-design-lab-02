import datetime

from internal.entity.User import User

class UserFactory():

    def create_from_row(self, row) -> User:
        if row is None:
            return None
        #print("row:")
        #print(row)
        #print("type of _id: " + str(type(row["_id"])))

        return User(
            _id=row["_id"],

            username=row["username"],
            password=row["password"],
            auth_key=row["auth_key"],
            access_token=row["access_token"],
            is_active=row["is_active"] if "is_active" in row else 0,
            lastname=row["lastname"],
            firstname=row["firstname"],
            date_of_add=row["date_of_add"]
        )