#! /usr/bin/python

from my_class.class_input_command import *
from my_class.ssh_local_device import *
from my_class.parser_output_ssh import *

def parser(command_terminal):
    command = ssh.exec_cmd(command_terminal)
    parser_output_ssh.set_output_command(command)
    list_return = parser_output_ssh.result()

    return list_return


def error_usl(command_input, type_input):
    if command_input == "failure: user with the same name already exisits\n":
        print('already created <type:%s>:' % type_input)

    elif command_input != "":
        print("error <type:%s>:" % type_input, command_input)


def run_configuration_across_ssh(type_error, dir_cfg_def, dir_command):

    # input all parameters
    class_input_command.set_type_error(type_error)
    class_input_command.set_dir_cfg_def(dir_cfg_def)
    class_input_command.set_dir_command(dir_command)

    # run command across ssh_client
    list_input_command = class_input_command.result()

    for input_command in list_input_command:

        temp = ssh.exec_cmd(input_command)
        error_usl(temp, type_error)


def clients():
    # clients
    # ip_device = input("input device IP: ")
    ip_device = "10.10.0.79"
    port_access = 22
    login_local = "rinet"
    pass_local = "rinetsupport"

    return ip_device, port_access, login_local, pass_local

def logging():
    type_error = 'logging'
    dir_command = '/system logging set'
    run_configuration_across_ssh(type_error, dir_cfg, dir_command)


dir_cfg = 'C:\\Python\\Mikrotik\\config\\mikrotik-config.yml'

if __name__ == '__main__':


    # parameters for ssh client
    hostname, port, username, password = clients()

    with ssh_local_device(hostname=hostname, username=username,
                          password=password, port=port) as ssh:

            logging()
