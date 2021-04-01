from datetime import datetime


class Log:

    @staticmethod
    def get_ready_log(user):
        return f'| Client successfully connected as:\n' \
               f'| Username: {user.name}\n| ID: {user.id}\n' \
               f'-----------------------------------------'

    @staticmethod
    def get_action_log(user, action):
        return f'| User {user.name}[{user.id}] at {str(datetime.now()).split(".")[0]}\n' \
               f'| He has {action}\n' \
               f'+-----------------------------------------'

    @staticmethod
    def print_on_ready(user):
        print(Log.get_ready_log(user))

    @staticmethod
    def print_action_log(user, action):
        print(Log.get_action_log(user, action))
