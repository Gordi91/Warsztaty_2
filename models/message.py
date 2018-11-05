from models.user import User


class Message:
    __id = None
    from_user = None
    to_id = None
    text = None
    __creation_date = None

    def __init__(self, from_user, to_user, text):
        self.__id = -1
        self.from_user = from_user
        self.to_user = to_user
        self.text = text
        self.__creation_date = None

    @property
    def id(self):
        return self.__id

    @property
    def creation_date(self):
        return self.__creation_date

    @staticmethod
    def load_message(cursor, data):
        """Extract data from row of sql select query with id, from_id, to_id, text, creation_date columns"""
        loaded_message = Message(data[1], User.load_user_by_id(cursor, data[2]), data[3])
        loaded_message.__id = data[0]
        loaded_message.__creation_date = data[4]
        return loaded_message

    @staticmethod
    def load_message_by_id(cursor, message_id):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE id=%s"
        cursor.execute(sql, (message_id,))
        data = cursor.fetchone()
        if data:
            loaded_message = Message.load_message(cursor, data)
            return loaded_message
        else:
            return None

    @staticmethod
    def load_all_messages(cursor):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM messages"
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_message = Message.load_message(cursor, row)
            ret.append(loaded_message)
        return ret

    @staticmethod
    def load_all_messages_for_user(cursor, user_id):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE to_id=%s"
        sql += "ORDER BY creation_date ASC"
        ret = []
        cursor.execute(sql, (user_id,))
        for row in cursor.fetchall():
            loaded_message = Message.load_message(cursor, row)
            ret.append(loaded_message)
        return ret

    def save_to_db(self, cursor):
        if self.__id == -1:
            # saving new instance using prepared statements
            sql = """INSERT INTO messages(from_id, to_id, text)
                     VALUES (%s, %s, %s) RETURNING id;"""
            values = (self.from_user.id, self.to_user.id, self.text)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            return True
