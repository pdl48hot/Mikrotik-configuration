from my_class.class_treatment import *

class class_input_command:

    def __init__(self):
        pass

    @staticmethod
    def set_type_error(type_error):
        class_input_command.type_error = type_error

    @staticmethod
    def set_dir_cfg_def(dir_cfg_def):
        class_input_command.dir_cfg_def = dir_cfg_def

    @staticmethod
    def set_dir_command(dir_command):
        class_input_command.dir_command = dir_command

    # @staticmethod
    # def set_ip_device_clients(ip_device_clients):
    #     class_ssh_input_command.ip_device_clients = ip_device_clients
    #
    # @staticmethod
    # def set_login_local_device(login_local_device):
    #     class_ssh_input_command.login_local_device = login_local_device
    #
    # @staticmethod
    # def set_pass_local_device(pass_local_device):
    #     class_ssh_input_command.pass_local_device = pass_local_device
    #
    # @staticmethod
    # def set_port_access_clients(port_access_clients):
    #     class_ssh_input_command.port_access_clients = port_access_clients

    @staticmethod
    def result():

        class_treatment.set_type(class_input_command.type_error)
        class_treatment.set_dir_cfg_def(class_input_command.dir_cfg_def)
        class_treatment.set_dir_command(class_input_command.dir_command)
        input_command_list = class_treatment.result()
        # print(input_command_list)
        list_input_command = []

        for input_command in input_command_list:
            # print(input_command)

            # with ssh_local_device(hostname=class_ssh_input_command.ip_device_clients,
            #                       username=class_ssh_input_command.login_local_device,
            #                       password=class_ssh_input_command.pass_local_device,
            #                       port=class_ssh_input_command.port_access_clients) as ssh:

            list_input_command.append(input_command)

        return list_input_command
