import os
import subprocess
# import pprint

from my_class.ssh_local_device import *
from my_class.class_input_command import *

# ========================INPUT-PARAMETER=======================


def parser(command_terminal):
    command = ssh.exec_cmd(command_terminal)
    temp_file = open('temp', 'w')

    temp_file.write(command)
    temp_file.close()
    temp_file = open('temp', 'r')

    list_return = []
    for parameter in temp_file:
        list_temp = []
        if parameter != '\n':
            i = 0
            list_parser = parameter.split(' ')
            for temp in list_parser:
                if temp != '':
                    list_temp.append(temp)
                    i += 1
            list_return.append(list_temp)

    temp_file.close()

    return list_return


def ip_for_client_l2tp():
    command = '/ppp secret print'
    test2 = parser(command)
    list_summ = []

    for l2tp in test2:
        if int(len(l2tp)) == 7:
            ip_clients = l2tp[5]
            list_ip_clients = ip_clients.split('.')

            a = int(list_ip_clients[0])
            b = int(list_ip_clients[1])
            c = int(list_ip_clients[2])
            d = int(list_ip_clients[3])

            summ = str(a * 255 ** 3 + b * 255 ** 2 + c * 255 + d)

            list_summ.append(summ)

        else:
            pass

    list_summ = sorted(list_summ, reverse=True)

    last_summ = int(list_summ[0]) + 1
    temp = int(last_summ)

    d_max = str(temp % 255)
    temp = int(temp / 255)
    c_max = str(temp % 255)
    temp = int(temp / 255)
    b_max = str(temp % 255)
    temp = int(temp / 255)
    a_max = str(temp % 255)

    new_ip = str(a_max + '.' + b_max + '.' + c_max + '.' + d_max)
    return new_ip


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
    ip_device = "192.168.88.1"
    port_access = 22
    login_local = "admin"
    pass_local = ""

    return ip_device, port_access, login_local, pass_local


def server():
    # parameters server
    ip_device = "86.62.82.242"
    port_access = 64222
    login_server = "ansible"
    pass_server = "Pdl48zx0ma3st15!"

    return ip_device, port_access, login_server, pass_server


# =========================FIREWALL============================

def parser_mac():
    command_parser = '/ip dhcp-client print'
    list_return = parser(command_parser)
    ii = 0
    for parser_elements in list_return:
        count = int(len(list_return[ii]))
        if count != 6:
            ii += 1
        else:
            pass

    command_parser = '/interface ethernet print'
    temp = parser(command_parser)
    i = 0
    for par in temp:
        count = int(len(par[i]))
        if count != 7:
            ii += 1
            if par[2] == parser_elements[0]:
                parser_mac_address = par[4]

    return parser_mac_address


def firewall():
    type_error = 'firewall'
    dir_command = '/ip firewall filter add'

    # -------------------------FIREWALL-FILTER-DELETE-------------------------------------------------
    type_def_filter_delete = "firewall_filter_delete"
    command = ssh.exec_cmd("/ip firewall filter {:foreach c in=[find] do={:do {remove $c;} on-error={}}} ")
    error_usl(command, type_def_filter_delete)

    # -------------------------FIREWALL-FILTER-ADD-RULES----------------------------------------------
    run_configuration_across_ssh(type_error, dir_cfg, dir_command)


def mangle():
    type_error = 'mangle'
    dir_command = '/ip firewall mangle add'

    # -------------------------FIREWALL-MANGLE-DELETE-------------------------------------------------
    type_def_mangle = "firewall_mangle_delete"
    command = ssh.exec_cmd('/ip firewall mangle remove numbers=[find comment="auto mangle rule"]')
    error_usl(command, type_def_mangle)

    # -------------------------FIREWALL-MANGLE-ADD-RULES----------------------------------------------
    run_configuration_across_ssh(type_error, dir_cfg, dir_command)


def address_list():
    type_error = 'address-list'
    dir_command = '/ip firewall address-list add'

    # -------------------------FIREWALL-ADDRESS-LIST-DELETE-------------------------------------------------
    type_def_address_list_delete = "firewall_address_list_delete"
    command = ssh.exec_cmd("/ip firewall address-list remove numbers=[find list=remote_access]")
    error_usl(command, type_def_address_list_delete)

    # -------------------------FIREWALL-ADDRESS-LIST-ADD----------------------------------------------
    run_configuration_across_ssh(type_error, dir_cfg, dir_command)


def service_port():
    type_error = 'service-port'
    dir_command = '/ip firewall service-port set'
    run_configuration_across_ssh(type_error, dir_cfg, dir_command)


# ===========================QUEUE===============================
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
    run_configuration_across_ssh(type_error, dir_cfg, dir_command)


# ===========================MAIN===============================
def users(network_work, dir_key_user):
    mac_up = parser_mac()
    dir_command = '/user add'
    type_error = "users"
    class_treatment.set_queue_rate(queue_tree_rate_def)
    run_configuration_across_ssh(type_error, dir_cfg, dir_command)

    password = subprocess.check_output([dir_key_user, '%s' % mac_up],
                                       shell=True, universal_newlines=True)
    password = password.strip('\n')

    # -----------------settings-rinet---------------------------
    ssh.exec_cmd('/user set rinet password="%s"' % password)

    # -----------------settings-admin---------------------------
    ssh.exec_cmd('/user set admin address=%s' % network_work)
    print('Password for Rinet account: ', password)
    return password


def ntp():
    dir_command = '/system ntp client set'
    type_error = "ntp"
    class_treatment.set_queue_rate(queue_tree_rate_def)
    run_configuration_across_ssh(type_error, dir_cfg, dir_command)


def clock():
    dir_command = '/system clock set'
    type_error = "clock"
    class_treatment.set_queue_rate(queue_tree_rate_def)
    run_configuration_across_ssh(type_error, dir_cfg, dir_command)


def logging():
    type_error = 'logging'
    dir_command = '/system logging set'
    run_configuration_across_ssh(type_error, dir_cfg, dir_command)


def identity():
    type_def = "identity"
    login_name_device = input("Введите логин объекта:")
    command = ssh.exec_cmd('/system identity set name="%s"' % login_name_device)
    error_usl(command, type_def)

    return login_name_device


# ===========================PPP-ACCOUNT===========================
def created_ppp_account_too_server(login_device, password, ip_l2tp):
    type_error = 'ppp-secret-server'
    dir_command = '/ppp secret add'

    class_treatment.set_ppp_account(login_device)
    class_treatment.set_ppp_password(password)
    class_treatment.set_ppp_next_ip(ip_l2tp)

    run_configuration_across_ssh(type_error, dir_cfg, dir_command)


def created_ppp_account_too_clients(login_device, password, ip_l2tp):
    type_error = 'ppp-secret-client'
    dir_command = '/interface l2tp-client add'

    class_treatment.set_ppp_account(login_device)
    class_treatment.set_ppp_password(password)
    class_treatment.set_ppp_next_ip(ip_l2tp)

    run_configuration_across_ssh(type_error, dir_cfg, dir_command)


# =========================SYSTEM==================================
# Требуется upgrade кода
def upgrade():
    # type_def = "upgrade_system"
    command_check = "/system package update check-for-updates"

    version = parser(command_check)
    current_version = version[4][1]
    latest_version = version[5][1]

    if latest_version == current_version:
        pass

    elif latest_version != 'ERROR:':
        print('current-version:', current_version.strip('\n'))
        print('latest-version:', latest_version.strip('\n'))

        upgrade_system = input('you want upgrade the system? (yes/no): ')
        if upgrade_system == 'yes':
            ssh.exec_cmd('/system package update download')
            ssh.exec_cmd('/system reboot')
        else:
            pass


def scheduler():
    type_def = "scheduler"
    command = ssh.exec_cmd('/system scheduler add name=reset start-time=startup on-event="system reset-configuration"')
    error_usl(command, type_def)


my_dir = os.getcwd()
my_network = '192.168.0.0/16'
queue_tree_rate_def = 'none'
dir_cfg = my_dir + '\\config\\mikrotik-config.yml'
dir_key = my_dir + '\\Key\\Key.dll'
class_treatment = class_treatment()

type_devices = input('Введите тип устройства (router (1) / AP (2) / test(3): ')

if __name__ == '__main__':

    # parameters for ssh client
    ip_device_clients, port_access_clients, login_local_device, pass_local_device = clients()

    # parameters server
    ip_device_server, port_access_server, login_server_device, pass_server_device = server()

    with ssh_local_device(hostname=ip_device_server, username=login_server_device,
                          password=pass_server_device, port=port_access_server) as ssh:

        ip_l2tp_client = ip_for_client_l2tp()

    with ssh_local_device(hostname=ip_device_clients, username=login_local_device,
                          password=pass_local_device, port=port_access_clients) as ssh:

        # __init__ class

        # ssh_local_device = ssh_local_device()

        if type_devices == '1':
            upgrade()

            logging()
            ntp()
            clock()
            login = identity()
            firewall()
            mangle()
            address_list()
            service_port()
            password_mac = users(my_network, dir_key)

            queue_tree_rate_def = input("Введите скорость интернета: (*1m/1M): ")
            queue_tree_rate_def = queue_tree_rate_def.upper()
            queue()

            created_ppp_account_too_clients(login, password_mac, ip_l2tp_client)

        elif type_devices == '2':
            upgrade()
            logging()
            ntp()
            clock()
            login = identity()

            password_mac = users(my_network, dir_key)

            created_ppp_account_too_clients(login, password_mac, ip_l2tp_client)

        elif type_devices == '3':
            logging()
            ntp()
            clock()

        with ssh_local_device(hostname=ip_device_server, username=login_server_device,
                              password=pass_server_device, port=port_access_server) as ssh:
            try:
                created_ppp_account_too_server(login, password_mac, ip_l2tp_client)
            except:
                print('<error: ppp client not created>')
