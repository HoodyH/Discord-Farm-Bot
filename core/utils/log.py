from datetime import datetime


class Log(object):

    @staticmethod
    def print_on_ready(user):
        print("+-----------------------------------------")
        print("| Client successfully connected as:")
        print("| Username: {0.name}\n| ID: {0.id}".format(user))
        print("+-----------------------------------------")

    @staticmethod
    def print_action_log(user, action):
        print("+-----------------------------------------")
        print("| User {}[{}] at {}".format(user.name, user.id, str(datetime.now()).split(".")[0]))
        print("| He has {}".format(action))
        print("+-----------------------------------------")