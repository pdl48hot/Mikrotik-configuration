import yaml
import os


class account:

    def __init__(self):
        pass

    @staticmethod
    def result(user_uid):
        my_dir = os.getcwd()
        dir_account = my_dir + '\\accounts.yml'

        try:
            with open(dir_account, 'r') as load_account:
                data_load = yaml.safe_load(load_account)
                login_server = (data_load['accounts'][user_uid]['name_server'])
                password_server = (data_load['accounts'][user_uid]['password_server'])
        except:
            pass

        return login_server, password_server
