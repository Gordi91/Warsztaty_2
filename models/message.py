class Message:
    __id = None
    from_id = None
    to_id = None
    text = None
    __creation_date = None

    def __init__(self):
        self.__id = -1
        self.from_id = ""
        self.to_id = ""
        self.text = ""
        self.__creation_date = ""

    @property
    def id(self):
        return self.__id

    @property
    def creation_date(self):
        return self.__creation_date

    @staticmethod
    def load_message_by_id(cursor, message_id):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE id=%s"
        cursor.execute(sql, (message_id,))
        data = cursor.fetchone()
        if data:
            loaded_message = Message()
            loaded_message.__id = data[0]
            loaded_message.from_id = data[1]
            loaded_message.to_id = data[2]
            loaded_message.text = data[3]
            loaded_message.__creation_date = data[4]
            return loaded_message
        else:
            return None

    @staticmethod
    def load_all_messages(cursor):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM messages"
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.from_id = row[1]
            loaded_message.to_id = row[2]
            loaded_message.text = row[3]
            loaded_message.__creation_date = row[4]
            ret.append(loaded_message)
        return ret

    @staticmethod
    def load_all_messages_for_user(cursor, user_id):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE to_id=%s"
        sql += "ORDER BY creation_date ASC"
        ret = []
        cursor.execute(sql, (user_id,))
        for row in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.from_id = row[1]
            loaded_message.to_id = row[2]
            loaded_message.text = row[3]
            loaded_message.__creation_date = row[4]
            ret.append(loaded_message)
        return ret

    def save_to_db(self, cursor):
        if self.__id == -1:
            # saving new instance using prepared statements
            sql = """INSERT INTO messages(from_id, to_id, text)
                     VALUES (%s, %s, %s) RETURNING id;"""
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            return True
