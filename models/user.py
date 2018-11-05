from clcrypto import check_password, password_hash


class User(object):

    __id = None
    username = None
    __hashed_password = None
    email = None

    def __init__(self, username, email):
        self.__id = -1
        self.username = username
        self.email = email
        self.__hashed_password = ""

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    def set_password(self, password):
        """Sets hashed password"""
        self.__hashed_password = password_hash(password)

    def save_to_db(self, cursor):
        if self.__id == -1:
            # saving new instance using prepared statements
            sql = """INSERT INTO Users(username, email, hashed_password)
                     VALUES (%s, %s, %s) RETURNING id;"""
            values = (self.username, self.email, self.hashed_password)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET username=%s, email=%s, hashed_password=%s
            WHERE id=%s"""
            values = (self.username, self.email, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user(data):
        """Extract data from row of sql select query with id, username, to_id,
        text, creation_date columns and load user"""
        loaded_user = User(data[1], data[2])
        loaded_user.__id = data[0]
        loaded_user.__hashed_password = data[3]
        return loaded_user

    @staticmethod
    def load_user_by_id(cursor, user_id):
        sql = "SELECT id, username, email, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (user_id,))
        data = cursor.fetchone()
        if data:
            loaded_user = User.load_user(data)
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_email(cursor, user_id):
        sql = "SELECT id, username, email, hashed_password FROM users WHERE email=%s"
        cursor.execute(sql, (user_id,))
        data = cursor.fetchone()
        if data:
            loaded_user = User.load_user(data)
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, email, hashed_password FROM Users"
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_user = User.load_user(row)
            ret.append(loaded_user)
        return ret

    def delete(self, cursor):
        """Delete selected user from database"""
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.__id,))
        self.__id = -1
        return True

    @staticmethod
    def get_id(username, cursor):
        """Check if user is in database and returns it's ID. If user not present in database returns new user id = -1"""
        sql = "SELECT id FROM users WHERE username=%s"
        cursor.execute(sql, (username,))
        if cursor.rowcount > 0:
            user_id = cursor.fetchone()[0]
            return user_id
        else:
            return -1

    @staticmethod
    def get_id_by_email(email, cursor):
        """Check if users email is in database and returns it's ID. If email not present in database returns
        new user id = -1"""
        sql = "SELECT id FROM users WHERE email=%s"
        cursor.execute(sql, (email,))
        if cursor.rowcount > 0:
            user_id = cursor.fetchone()[0]
            return user_id
        else:
            return -1

    @staticmethod
    def check_and_load_user(cursor, username, password):
        user_id = User.get_id(username, cursor)
        if user_id != -1:
            user = User.load_user_by_id(cursor, user_id)
            if check_password(password, user.hashed_password):
                return user
            else:
                return None
        else:
            return None
