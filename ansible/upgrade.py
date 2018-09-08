#! /usr/bin/python
import sys

sys.path.append("/home/dk/ansible")

from my_class.ssh_local_device import *
from my_class.parser_output_ssh import *
from ansible.module_utils.basic import *


def parser(command_terminal):
    command = ssh.exec_cmd(command_terminal)
    parser_output_ssh.set_output_command(command)
    list_return = parser_output_ssh.result()


    return list_return


def update():
    type_def = "upgrade_system"

    command_current = "/system package update set channel=current"
    ssh.exec_cmd(command_current)

    command_check = "/system package update check-for-updates"
    version = parser(command_check)

    current_version = version[5][1].strip('\r\n')
    latest_version = version[6][1].strip('\r\n')

    if latest_version == current_version:
        pass

    elif latest_version != 'ERROR:':
        print('current-version:', current_version.strip('\n'))
        print('latest-version:', latest_version.strip('\n'))

        if current_version == latest_version:
            test_fuck = 2
        else:
            ssh.exec_cmd('/system package update download')
            test_fuck = 1
    return test_fuck


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
        test = update()
    module.exit_json(changed=False, msg=msg, XXXX=test)
