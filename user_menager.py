from models.user import User
from models.sql_connection import create_connection, close_connection
from clcrypto import generate_salt
from psycopg2 import IntegrityError
import argparse


HELP_MESSAGE = """Help:
-u - username
-p - password
-a - email
-l - list
-n - new password
-d - delete
-e - edit
Create new user:\t -u <username> -p <password> -a <email>
Change password:\t -u <username> -p <password> -e -n <new password>
Delete user:\t\t -u <username> -p <password> -d
Print users table:\t -l
"""


def arg_parser():

    parser = argparse.ArgumentParser(description="User menager")

    parser.add_argument('-u', '--username',
                        help="User name",
                        nargs=1)
    parser.add_argument('-a', '--email',
                        help="User name",
                        nargs=1)
    parser.add_argument('-p', '--password',
                        help="User password",
                        nargs=1)
    parser.add_argument('-n', '--new_pass',
                        help="New password",
                        nargs=1)
    parser.add_argument('-l', '--list',
                        help="Show all users",
                        action="store_true")
    parser.add_argument('-d', '--delete',
                        help="Delete user",
                        action="store_true")
    parser.add_argument('-e', '--edit',
                        help="Edit user login or password",
                        action="store_true")
    return parser.parse_args()


def user_operations():
    args = arg_parser()

    if args.username and args.password and args.email and not args.edit and not args.delete:
        #  Creates new user
        create_user(args.username[0], args.password[0], args.email[0])

    elif args.username and args.password and args.edit and args.new_pass:
        #  Change user password
        cnx, cursor = create_connection()
        user = User.check_and_load_user(cursor, args.username[0], args.password[0])
        if user:
            if len(args.new_pass[0]) >= 8:
                salt = generate_salt()
                user.set_password(args.new_pass[0], salt)
                user.save_to_db(cursor)
                print("Password changed")
            else:
                print("Password to short")
        else:
            print("Invalid password or user")
        close_connection(cnx, cursor)

    elif args.username and args.password and args.delete:
        #  Delete user
        cnx, cursor = create_connection()
        user = User.check_and_load_user(cursor, args.username[0], args.password[0])
        if user:
            user.delete(cursor)
            print("User deleted")
        close_connection(cnx, cursor)

    elif args.list and not args.username and not args.password:
        #  Prints users table
        cnx, cursor = create_connection()
        load_users = User.load_all_users(cursor)
        user_table = "__ID__|__Username__|__Email__\n"
        for user in load_users:
            user_table += "{} | {} | {} \n".format(user.id, user.username, user.email)
        close_connection(cnx, cursor)
        print(user_table)
    else:
        print(HELP_MESSAGE)


def create_user(username, password, email):
    new_user = User()
    new_user.username = username
    new_user.email = email
    new_user.set_password(password, generate_salt())
    cnx, cursor = create_connection()
    try:
        new_user.save_to_db(cursor)
        print("User created")
    except IntegrityError:
        print("User already created, please try another email")
    finally:
        close_connection(cnx, cursor)


user_operations()
