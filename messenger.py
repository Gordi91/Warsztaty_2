from models.message import Message
from models.user import User
from models.sql_connection import create_connection, close_connection

import argparse

HELP_MESSAGE = """Help:
-u - username
-p - password
-l - list
-t - consignee
-s - message
To list all messages sent to you pass -u <username> -p <password> -l
To send message pass -u <username> -p <password> -t <email> -s <message>
"""


def arg_parser():

    parser = argparse.ArgumentParser(description="Opis funkcji")

    parser.add_argument('-u', '--username',
                        help="User name",
                        nargs=1)
    parser.add_argument('-p', '--password',
                        help="User password",
                        nargs=1)
    parser.add_argument('-l', '--list',
                        help="Show all messages",
                        action="store_true")
    parser.add_argument('-t', '--to',
                        help="Destination e-mail",
                        nargs=1)
    parser.add_argument('-s', '--send',
                        help="Your message",
                        nargs=1)
    return parser.parse_args()


def user_operations():
    args = arg_parser()

    if args.username and args.password:
        cnx, cursor = create_connection()
        user = User.check_and_load_user(cursor, args.username[0], args.password[0])
        if user:
            if args.list and not args.send and not args.to:
                messages = Message.load_all_messages_for_user(cursor, user.id)
                if messages:
                    message_table = "__ID__|__CONSIGNEE__|__TEXT__|__DATE_TIME__\n"
                    for message in messages:
                        message_table += "{} | {} | {} | {} \n"
                        message_table = message_table.format(message.id,
                                                             message.to_id,
                                                             message.text,
                                                             message.creation_date.strftime("%b %d %Y %H:%M:%S"))
                    print(message_table)
                else:
                    print("No messages to show")

            elif args.send and args.to and not args.list:
                if args.send[0] != "":
                    print(args.to[0])
                    consignee = User.load_user_by_email(cursor, args.to[0])
                    if consignee:
                        new_message = Message(user, consignee, args.send[0])
                        new_message.save_to_db(cursor)
                        print("Message sent")
                    else:
                        print("Consignee doesn't exist")
                else:
                    print("No message to send")

        else:
            print("Invalid password or user")
        close_connection(cnx, cursor)
    else:
        print(HELP_MESSAGE)


user_operations()
