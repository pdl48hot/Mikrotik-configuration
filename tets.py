import os
from class_treatment import *
from ssh_local_device import *

# ========================INPUT-PARAMETER=======================


def error_usl(command_input, type_input):
    if command_input != "":
        print("error <type:%s>:" % type_input, command_input)


def class_def(type_error, dir_cfg_def, dir_command):
    class_treatment.set_type(type_error)
    class_treatment.set_dir_cfg_def(dir_cfg_def)
    class_treatment.set_dir_command(dir_command)
    input_command_list = class_treatment.result()
    for input_command in input_command_list:
        temp = ssh.exec_cmd(input_command)
        error_usl(temp, type_error)


def clients():
    # clients
    ip_device_clients = "192.168.88.1"
    port_access_clients = 22
    login_local_device = "admin"
    pass_local_device = ""

    return ip_device_clients, port_access_clients, login_local_device, pass_local_device

def server():
    # parameters server
    ip_device_server = "86.62.82.242"
    port_access_server = 64322
    login_server_device = "zabbix_api"
    pass_server_device = "Pdl48zx0ma3st15!"

    return ip_device_server, port_access_server, login_server_device, pass_server_device

# =========================FILTER==============================


def logging():
    type_error = 'logging'
    dir_command = '/system logging set'
    class_def(type_error, dir_cfg, dir_command)


def firewall():
    type_error = 'firewall'
    dir_command = '/ip firewall filter add'

    # -------------------------FIREWALL-FILTER-DELETE-------------------------------------------------
    type_def_filter_delete = "firewall_filter_delete"
    command = ssh.exec_cmd("/ip firewall filter {:foreach c in=[find] do={:do {remove $c;} on-error={}}} ")
    error_usl(command, type_def_filter_delete)

    # -------------------------FIREWALL-FILTER-ADD-RULES----------------------------------------------
    class_def(type_error, dir_cfg, dir_command)


def mangle():
    type_error = 'mangle'
    dir_command = '/ip firewall mangle add'

    # -------------------------FIREWALL-MANGLE-DELETE-------------------------------------------------
    type_def_mangle = "firewall_mangle_delete"
    command = ssh.exec_cmd('/ip firewall mangle remove numbers=[find comment="auto mangle rule"]')
    error_usl(command, type_def_mangle)

    # -------------------------FIREWALL-MANGLE-ADD-RULES----------------------------------------------
    class_def(type_error, dir_cfg, dir_command)


def address_list():
    type_error = 'address-list'
    dir_command = '/ip firewall address-list add'

    # -------------------------FIREWALL-ADDRESS-LIST-DELETE-------------------------------------------------
    type_def_address_list_delete = "firewall_address_list_delete"
    command = ssh.exec_cmd("/ip firewall address-list remove numbers=[find list=remote_access]")
    error_usl(command, type_def_address_list_delete)

    # -------------------------FIREWALL-ADDRESS-LIST-ADD----------------------------------------------
    class_def(type_error, dir_cfg, dir_command)


def queue():
    dir_command = '/queue tree add'
    type_error = "queue"
    pcq_upload_def = 'pcq_upload'
    pcq_download_def = 'pcq_download'

    # -------------------------QUEUE-TREE-DELETE-------------------------------------------------
    command = ssh.exec_cmd('/queue tree remove numbers="%s"' % pcq_upload_def)
    error_usl(command, type_error)

    command = ssh.exec_cmd('/queue tree remove numbers="%s"' % pcq_download_def)
    error_usl(command, type_error)

    # -------------------------QUEUE-TREE-ADD----------------------------------------------------
    class_treatment.set_queue_rate(queue_tree_rate_def)
    class_def(type_error, dir_cfg, dir_command)


def users():
    dir_command = '/user add'
    type_error = "users"
    class_treatment.set_queue_rate(queue_tree_rate_def)
    class_def(type_error, dir_cfg, dir_command)


def ntp():
    dir_command = '/system ntp client set'
    type_error = "ntp"
    class_treatment.set_queue_rate(queue_tree_rate_def)
    class_def(type_error, dir_cfg, dir_command)


def clock():
    dir_command = '/system clock set'
    type_error = "clock"
    class_treatment.set_queue_rate(queue_tree_rate_def)
    class_def(type_error, dir_cfg, dir_command)


def identity():
    type_def = "identity"
    login_name_device = input("Введите логин объекта:")
    command = ssh.exec_cmd('/system identity set name="%s"' % login_name_device)
    error_usl(command, type_def)


# Требуется upgrade кода
def upgrade():
    type_def = "upgrade_system"
    command = ssh.exec_cmd("/system package update download")

    reboot_command = input("reboot this device? (yes/no):")

    upgrade_func = 0

    while upgrade_func == 0:

        if reboot_command == "yes":
            command = ssh.exec_cmd("/system reboot")
            upgrade_func = 1

        elif reboot_command == "no":
            print("by my friend")
            upgrade_func = 1

        else:
            command = input("Введена неверная команда, повторите:")

    error_usl(command, type_def)


def scheduler():
    type_def = "scheduler"
    command = ssh.exec_cmd('system scheduler add name=reset start-time=startup on-event="system reset-configuration"')
    error_usl(command, type_def)


my_dir = os.getcwd()
dir_cfg = my_dir + '\\mikrotik-config.yml'

if __name__ == '__main__':

    # parameters for ssh client
    ip_device_clients, port_access_clients, login_local_device, pass_local_device = clients()

    # parameters server
    ip_device_server, port_access_server, login_server_device, pass_server_device = server()

    with ssh_local_device(hostname=ip_device_clients, username=login_local_device,
                          password=pass_local_device, port=port_access_clients) as ssh:

        baba = 0

        while baba == 0:
            out = ssh.exec_cmd("/system routerboard print")

            first_start = input('Первый прогон? (yes/no):')

            if first_start != "yes":
                my_network = input("Введите вашу подсеть: ")

                queue_tree_rate_def = input("Введите скорость интернета: (*10M): ")

                # __init__ class
                class_treatment = class_treatment()
                ssh_local_device = ssh_local_device()

                logging()
                ntp()
                clock()
                identity()
                firewall()
                mangle()
                address_list()
                users()
                queue()
                baba = 1

