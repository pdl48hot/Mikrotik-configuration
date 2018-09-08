#! /usr/bin/python
import sys

sys.path.append("/home/dk/ansible")

from my_class.class_input_command import *
from my_class.ssh_local_device import *
from my_class.parser_output_ssh import *
from ansible.module_utils.basic import *


def run_configuration_across_ssh(type_error, dir_cfg_def, dir_command):
    # input all parameters
    class_input_command.set_type_error(type_error)
    class_input_command.set_dir_cfg_def(dir_cfg_def)
    class_input_command.set_dir_command(dir_command)

    # run command across ssh_client
    list_input_command = class_input_command.result()
    list_output_command = []
    for input_command in list_input_command:
        output_command = ssh.exec_cmd(input_command)
        list_output_command.append(output_command)

    return list_output_command


def ntp():
    dir_command = '/system ntp client set'
    type_error = "ntp"
    run_configuration_across_ssh(type_error, dir_cfg, dir_command)


def clock():
    dir_command = '/system clock set'
    type_error = "clock"
    run_configuration_across_ssh(type_error, dir_cfg, dir_command)


dir_cfg = '/home/dk/ansible/config/mikrotik-config.yml'

if __name__ == '__main__':
    module = AnsibleModule(
        argument_spec=dict(
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=True),
            port=dict(required=True),

        )
    )

    hostname = module.params['hostname']
    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    changed = False
    msg = ""

    with ssh_local_device(hostname=hostname, username=username,
                          password=password, port=port) as ssh:
        ntp()
        clock()

    module.exit_json(changed=False, msg=msg)