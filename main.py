import paramiko
import random
from pyparsing import *
from yaml import Loader, load
import os

# from pprint import *

my_dir = os.getcwd ()


class ssh_local_device:
    def __init__(self, **kwargs):
        self.client = paramiko.SSHClient ()
        self.client.set_missing_host_key_policy (paramiko.AutoAddPolicy ())
        self.kwargs = kwargs

    def __enter__(self):
        """код для подключения к удаленному хосту с импрортируемым модулем paramiko"""
        kw = self.kwargs
        self.client.connect (hostname=kw.get ('hostname'), username=kw.get ('username'),
                             password=kw.get ('password'), port=int (kw.get ('port', 22)))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close ()

    def exec_cmd(self, cmd):
        """ Необходимо выполнить команду с помощью скрипта (к прим. ls -al)"""
        stdin, stdout, stderr = self.client.exec_command (cmd)
        data = stdout.read ()
        # if stderr:
        # raise stderr
        return data.decode ()


# готово
def treatment(dir_cfg, dir_command, type_def):
    global conformity_check
    yml_file = open (dir_cfg, 'r')
    treatment_file = load (yml_file, Loader=Loader)

    for treatment_filter in treatment_file:
        new_rules_def = [dir_command]

        for (param, value) in treatment_filter.items ():
            new_rules_def.append (' ' + str (param) + '=' + str (value))

            conformity_check = ' module=%s' % type_def

        if new_rules_def[1] == conformity_check:
            new_rules_def.remove (new_rules_def[1])
            command = ''.join (new_rules_def)
            add_firewall_rules = ssh.exec_cmd (command)
            error_usl (add_firewall_rules, type_def)
            # print(command)
        else:
            pass


# готово
def treatment_for_qos(dir_cfg, dir_command, type_def, queue_tree_rate_def):
    global conformity_check
    yml_file = open (dir_cfg, 'r')
    treatment_file = load (yml_file, Loader=Loader)

    for treatment_filter in treatment_file:
        new_rules_def = [dir_command]

        for (param, value) in treatment_filter.items ():
            if value == 'tx_rate':

                new_rules_def.append (' ' + str (param) + '=' + str (queue_tree_rate_def))

                conformity_check = ' module=%s' % type_def
            else:
                new_rules_def.append (' ' + str (param) + '=' + str (value))

                conformity_check = ' module=%s' % type_def

        if new_rules_def[1] == conformity_check:
            new_rules_def.remove (new_rules_def[1])
            command = ''.join (new_rules_def)
            add_firewall_rules = ssh.exec_cmd (command)
            error_usl (add_firewall_rules, type_def)

        else:
            pass


def treatment_for_dhcp(dir_cfg, dir_command, type_def, my_network_def, ip_dhcp_server_def):
    global conformity_check
    yml_file = open (dir_cfg, 'r')
    treatment_file = load (yml_file, Loader=Loader)

    for treatment_filter in treatment_file:
        new_rules_def = [dir_command]

        for (param, value) in treatment_filter.items ():
            if value == 'network':

                new_rules_def.append (' ' + str (param) + '=' + str (my_network_def))

                conformity_check = ' module=%s' % type_def

            elif value == 'ip_dhcp_server':

                new_rules_def.append (' ' + str (param) + '=' + str (ip_dhcp_server_def))

                conformity_check = ' module=%s' % type_def

            else:
                new_rules_def.append (' ' + str (param) + '=' + str (value))

                conformity_check = ' module=%s' % type_def

        if new_rules_def[1] == conformity_check:
            print ('conformity_check: ', conformity_check)
            new_rules_def.remove (new_rules_def[1])
            print (new_rules_def)
            command = ''.join (new_rules_def)
            add_firewall_rules = ssh.exec_cmd (command)
            error_usl (add_firewall_rules, type_def)

        else:
            pass


# готово
def treatment_firewall_rules(dir_cfg, dir_command, type_def):
    yml_file = open (dir_cfg, 'r')
    treatment_file = load (yml_file, Loader=Loader)

    for treatment_filter in treatment_file:
        new_rules_def = [dir_command]

        for (param, value) in treatment_filter.items ():
            new_rules_def.append (' ' + str (param) + '=' + str (value))

        command = ''.join (new_rules_def)
        add_firewall_rules = ssh.exec_cmd (command)
        error_usl (add_firewall_rules, type_def)


# ============================FOR_CLASS_MIKROTIK_CONNECT=================================

def server(login_name_def):
    type_def = "server"
    # random_pass = random_gen ()
    comand = ssh.exec_cmd (
        "/ppp secret add name=%s password=%s profile=profile-l2tp remote-address=10.10.0.68 "
        "service=l2tp" % login_name_def)

    error_usl (comand, type_def)
    # return random_pass


def client(login_name_device, random_pass_device):
    type_def = "l2tp-zabbix"
    comand = ssh.exec_cmd (
        "/interface l2tp-client add allow=mschap1,mschap2 connect-to=86.62.82.242 disabled=no "
        "name=l2tp-zabbix password=%s user=%s" % (random_pass_device, login_name_device))
    error_usl (comand, type_def)


def error_usl(command_input, type_input):
    if command_input != "":
        print ("error <type:%s>:" % type_input, command_input)


def random_gen():
    str1 = "123456789"
    str2 = "qwertyuiopasdfghjklzxcvbnm"
    str3 = str2.upper ()
    str4 = str1 + str2 + str3
    ls = list (str4)
    random.shuffle (ls)
    # random_def_pass = ''.join ([random.choice (ls) for x in range (15)])
    # return random_def_pass


def parser_model_serial(out_comand):
    global model_device, serial_number
    out_comand_treatment = out_comand.splitlines ()
    out_comand_treatment.pop ()
    out_comand_treatment_count = int (len (out_comand_treatment))
    start = 0
    i = 0
    while start == 0:

        if i < out_comand_treatment_count:
            name_group = Word (alphas + '-:')
            name_parametr = Word (alphas + nums + '-. ')
            parser_module = name_group + name_parametr
            parser_group = parser_module.parseString (out_comand_treatment[i])

            if parser_group[0] == "model:":
                model_device = parser_group[1]

            elif parser_group[0] == "serial-number:":
                serial_number = parser_group[1]

            i += 1
        else:
            start = 1

    return model_device, serial_number


# ============================FOR_CLASS_MIKROTIK_CONFIG=================================
def scheduler():
    type_def = "scheduler"
    comand = ssh.exec_cmd ('system scheduler add name=reset start-time=startup on-event="system reset-configuration"')
    error_usl (comand, type_def)


def upgrade():
    type_def = "upgrade_system"
    comand = ssh.exec_cmd ("/system package update download")

    reboot_comand = input ("reboot this device? (yes/no):")

    upgrade_func = 0

    while upgrade_func == 0:

        if reboot_comand == "yes":
            comand = ssh.exec_cmd ("/system reboot")
            upgrade_func = 1

        elif reboot_comand == "no":
            print ("by my friend")
            upgrade_func = 1

        else:
            comand = input ("Введена неверная команда, повторите:")

    error_usl (comand, type_def)


# готово
def users(my_network_def):
    dir_mikrotik_cfg = my_dir + '\\mikrotik.cfg'
    dir_command = '/user add'
    type_error_ntp = "users"
    command = ssh.exec_cmd ('/user set admin address="%s" comment="" ' % my_network_def)
    error_usl (command, type_error_ntp)
    treatment (dir_mikrotik_cfg, dir_command, type_error_ntp)


# готово!
def clock():
    dir_mikrotik_cfg = my_dir + '\\mikrotik.cfg'
    dir_command = '/system clock set'
    type_error_ntp = "clock"
    treatment (dir_mikrotik_cfg, dir_command, type_error_ntp)


def queue(queue_tree_rate_def):
    pcq_upload_def = 'pcq_upload'
    pcq_download_def = 'pcq_download'
    dir_mikrotik_cfg = my_dir + '\\mikrotik.cfg'
    dir_command = '/queue tree add'
    type_error_ntp = "queue"

    # -------------------------QUEUE-TREE-DELETE-------------------------------------------------
    command = ssh.exec_cmd ('/queue tree remove numbers="%s"' % pcq_upload_def)
    error_usl (command, type_error_ntp)

    command = ssh.exec_cmd ('/queue tree remove numbers="%s"' % pcq_download_def)
    error_usl (command, type_error_ntp)

    # -------------------------QUEUE-TREE-ADD-------------------------------------------------
    treatment_for_qos (dir_mikrotik_cfg, dir_command, type_error_ntp, queue_tree_rate_def)


# готово!
def identity():
    type_def = "identity"
    login_name_device = input ("Введите логин объекта:")
    command = ssh.exec_cmd ('/system identity set name="%s"' % login_name_device)
    error_usl (command, type_def)


# готово
def logging():
    dir_mikrotik_cfg = my_dir + '\\mikrotik.cfg'
    dir_command = '/system logging set'
    type_error_ntp = 'logging'
    treatment (dir_mikrotik_cfg, dir_command, type_error_ntp)


# готово
def ntp():
    dir_mikrotik_cfg = my_dir + '\\mikrotik.cfg'
    dir_ntp_command = '/system ntp client set'
    type_error_ntp = 'ntp'
    treatment (dir_mikrotik_cfg, dir_ntp_command, type_error_ntp)


# готово
def firewall():
    # -------------------------FIREWALL-FILTER-DELETE-------------------------------------------------
    type_def_filter_delete = "firewall_filter_delete"
    comand = ssh.exec_cmd ("/ip firewall filter {:foreach c in=[find] do={:do {remove $c;} on-error={}}} ")
    error_usl (comand, type_def_filter_delete)

    # -------------------------FIREWALL-FILTER-ADD-RULES----------------------------------------------
    dir_mikrotik_cfg = my_dir + '\\firewall\\firewall.txt'
    dir_ntp_command = '/ip firewall filter add'
    type_error_ntp = 'firewall filter'
    treatment_firewall_rules (dir_mikrotik_cfg, dir_ntp_command, type_error_ntp)

    # -------------------------FIREWALL-MANGLE-DELETE-------------------------------------------------
    type_def_mangle = "firewall_mangle_delete"
    comand = ssh.exec_cmd ('/ip firewall mangle remove numbers=[find comment="auto mangle rule"]')
    error_usl (comand, type_def_mangle)

    # -------------------------FIREWALL-MANGLE-ADD-RULES----------------------------------------------
    dir_mikrotik_cfg = my_dir + '\\firewall\\mangle.txt'
    dir_ntp_command = '/ip firewall mangle add'
    type_error_ntp = 'firewall-mangle'
    treatment_firewall_rules (dir_mikrotik_cfg, dir_ntp_command, type_error_ntp)

    # -------------------------FIREWALL-ADDRESS-LIST-DELETE-------------------------------------------------
    type_def_address_list_delete = "firewall_address_list_delete"
    comand = ssh.exec_cmd ("/ip firewall address-list remove numbers=[find list=remote_access]")
    error_usl (comand, type_def_address_list_delete)

    # -------------------------FIREWALL-ADDRESS-LIST-ADD----------------------------------------------
    dir_mikrotik_cfg = my_dir + '\\firewall\\address-list.txt'
    dir_ntp_command = '/ip firewall address-list add'
    type_error_ntp = 'firewall-address-list'
    treatment_firewall_rules (dir_mikrotik_cfg, dir_ntp_command, type_error_ntp)

    # -------------------------FIREWALL-SERVICE-PORT-SIP-SET----------------------------------------------
    dir_mikrotik_cfg = my_dir + '\\mikrotik.cfg'
    dir_ntp_command = '/ip firewall service-port set sip'
    type_error_ntp = 'service-port'
    treatment (dir_mikrotik_cfg, dir_ntp_command, type_error_ntp)


# не готово
def dhcp_server(my_network_def, ip_dhcp_server_def):
    dir_mikrotik_cfg = my_dir + '\\mikrotik.cfg'
    dir_command = '/ip dhcp-server add'
    type_error = 'dhcp-server'
    treatment_for_dhcp (dir_mikrotik_cfg, dir_command, type_error, my_network_def, ip_dhcp_server_def)


# def test():
#     command = ssh.exec_cmd ('/interface ethernet print')


# ============================MAIN-PROGRAMM=================================
0

if __name__ == '__main__':

    # clients
    ip_device_clients = "192.168.1.1"
    port_access_clients = 22
    login_local_device = "admin"
    pass_local_device = ""

    # server
    ip_device_server = "86.62.82.242"
    port_access_server = 64322
    login_server_device = "zabbix_api"
    pass_server_device = "Pdl48zx0ma3st15!"

    # with ssh_local_device (hostname=ip_device_server, username=login_server_device,
    #                       password=pass_server_device, port=port_access_server) as ssh:

    with ssh_local_device (hostname=ip_device_clients, username=login_local_device,
                           password=pass_local_device, port=port_access_clients) as ssh:

        password = str (random_gen ())
        baba = 0

        while baba == 0:
            out = ssh.exec_cmd ("/system routerboard print")
            model, serial = parser_model_serial (out)

            first_start = input ('Первый прогон? (yes/no):')

            if first_start != "yes":
                my_network = input ("Введите вашу подсеть: ")
                # ip_dhcp_server = input ("Введите ip mikotik: ")
                queue_tree_rate = input ("Введите скорость интернета: (*10M): ")

                # Модули для всех
                identity ()
                logging ()
                ntp ()
                clock ()
                users (my_network)
                # Важные модули
                firewall ()
                queue (queue_tree_rate)
                # test()
                # dhcp_server (my_network, ip_dhcp_server)
                # 
                baba = 1

            else:
                scheduler ()
                upgrade ()

                baba = 1
