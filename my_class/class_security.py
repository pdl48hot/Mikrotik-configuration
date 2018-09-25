import yaml
import os


class account:

    def __init__(self):
        pass

    @staticmethod
    def result(user_uid):
        my_dir = os.getcwd()
        dir_account = 'C:\\Python\\Key_for_python\\accounts.yml'
        if user_uid != 0:
            with open(dir_account, 'r') as load_account:
                data_load = yaml.safe_load(load_account)

                login_server = (data_load['accounts'][user_uid]['name'])
                password_server = (data_load['accounts'][user_uid]['password'])
                return login_server, password_server

        else:
            with open(dir_account, 'r') as load_account:
                data_load = yaml.safe_load(load_account)

                login_server = (data_load['accounts'][user_uid]['name'])
                password_server = (data_load['accounts'][user_uid]['password'])
                port_access = (data_load['accounts'][user_uid]['port'])
                hostname = (data_load['accounts'][user_uid]['hostname'])
                return login_server, password_server, port_access, hostname

