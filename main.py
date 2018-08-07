import paramiko
import random
from pyparsing import *
from pprint import *


class ssh_local_device:
    def __init__(self, **kwargs):
        self.client = paramiko.SSHClient ()
        self.client.set_missing_host_key_policy (paramiko.AutoAddPolicy ())
        self.kwargs = kwargs

    def __enter__(self):
        """Ккод для подключения к удаленному хосту с импрортируемым модулем paramiko"""
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


class ssh_server_device:
    def __init__(self, **kwargs):
        self.client = paramiko.SSHClient ()
        self.client.set_missing_host_key_policy (paramiko.AutoAddPolicy ())
        self.kwargs = kwargs

    def __enter__(self):
        """Ккод для подключения к удаленному хосту с импрортируемым модулем paramiko"""
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


# ============================FOR_CLASS_MIKROTIK_CONNECT=================================

def server(login_name):
    type_def = "server"
    random_pass = random_gen ()
    comand = ssh.exec_cmd (
        "/ppp secret add name=%s password=%s profile=profile-l2tp remote-address=10.10.0.68 "
        "service=l2tp" % (login_name, random_pass))

    error_usl (comand, type_def)
    return random_pass


def client(login_name_device, random_pass_device):
    type_def = "l2tp-zabbix"
    comand = ssh.exec_cmd (
        "/interface l2tp-client add allow=mschap1,mschap2 connect-to=86.62.82.242 disabled=no "
        "name=l2tp-zabbix password=%s user=%s" % (random_pass_device, login_name_device))
    error_usl (comand, type_def)


def error_usl(comand_input, type_input):
    if comand_input != "":

        if type_input == "loging":
            print ("error <type:loging>:", comand_input)

        elif type_input == "users":
            print ("error <type:users>:", comand_input)

        elif type_input == "server":
            print ("error <type:server>:", comand_input)

        elif type_input == "l2tp-zabbix":
            print ("error <type:l2tp-zabbix>:", comand_input)

        elif type_input == "clock":
            print ("error <type:clock>:", comand_input)

        elif type_input == "firewall_filter":
            print ("error <type:firewall_filter>:", comand_input)

        elif type_input == "firewall_address_list":
            print ("error <type:firewall_address_list>:", comand_input)

        elif type_input == "firewall_address_list_delete":
            print ("error <type:firewall_address_list_delete>:", comand_input)

        elif type_input == "firewall_filter_delete":
            print ("error <type:firewall_filter_delete>:", comand_input)

        elif type_input == "scheduler":
            print ("error <type:firewall_filter_delete>:", comand_input)




def random_gen():
    str1 = "123456789"
    str2 = "qwertyuiopasdfghjklzxcvbnm"
    str3 = str2.upper ()
    str4 = str1 + str2 + str3
    ls = list (str4)
    random.shuffle (ls)
    random_def_pass = ''.join ([random.choice (ls) for x in range (15)])
    return random_def_pass


def parser_model_serial(out_comand):
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



def firewall():

    # -------------------------FIREWALL-FILTER-DELETE------------------------------------------

    type_def_filter_delete = "firewall_filter_delete"
    comand = ssh.exec_cmd ("/ip firewall filter {:foreach c in=[find] do={:do {remove $c;} on-error={}}} ")
    error_usl (comand, type_def_filter_delete)

    # -------------------------FIREWALL-FILTER-REMOVE-------------------------------------------------
    type_def_filter = "firewall_filter"
    comand = ssh.exec_cmd ('/ip firewall filter add action=accept chain=input '
                           'comment="remote access for rinet" in-interface=ether1 src-address-list=remote_access')
    error_usl (comand, type_def_filter)

    # -------------------------FIREWALL-FILTER--------------------------------------------------------
    comand = ssh.exec_cmd ('/ip firewall filter add action=accept chain=input connection-state=established,related')
    error_usl (comand, type_def_filter)
    comand = ssh.exec_cmd ('/ip firewall filter add action=accept chain=input protocol=icmp')
    error_usl (comand, type_def_filter)
    comand = ssh.exec_cmd ('/ip firewall filter add action=drop chain=input in-interface=ether1')
    error_usl (comand, type_def_filter)
    comand = ssh.exec_cmd ('/ip firewall filter add action=accept chain=forward connection-state=established,related')
    error_usl (comand, type_def_filter)
    comand = ssh.exec_cmd ('/ip firewall filter add action=drop chain=forward connection-state=invalid')
    error_usl (comand, type_def_filter)
    comand = ssh.exec_cmd ('/ip firewall filter add action=drop chain=forward '
                           'connection-nat-state=!dstnat connection-state=new in-interface=ether1')
    error_usl (comand, type_def_filter)

    # -------------------------FIREWALL-FILTER-ADDRESS-LIST-REMOWE------------------------------------------------
    type_def_address_list = "firewall_address_list"
    type_def_address_list_delete = "firewall_address_list_delete"

    comand = ssh.exec_cmd ("/ip firewall address-list remove numbers=[find list=remote_access]")
    error_usl (comand, type_def_address_list_delete)

    # -------------------------FIREWALL-FILTER-ADDRESS-LIST-------------------------------------------------
    comand = ssh.exec_cmd ("/ip firewall address-list add address=86.62.127.224/28 list=remote_access")
    error_usl (comand, type_def_address_list)
    comand = ssh.exec_cmd ("/ip firewall address-list add address=86.62.82.242 list=remote_access")
    error_usl (comand, type_def_address_list)
    comand = ssh.exec_cmd ("/ip firewall address-list add address=172.16.255.254 list=remote_access")
    error_usl (comand, type_def_address_list)

    # -------------------------FIREWALL-SERVICE-PORT-------------------------------------------------

    type_def_service_port = "firewall_service_port"

    comand = ssh.exec_cmd ('/ip firewall service-port set sip sip-direct-media=no')
    error_usl (comand, type_def_service_port)

    # -------------------------FIREWALL-MANGLE-------------------------------------------------
    type_def_mangle = "firewall_service_port"
    comand = ssh.exec_cmd ('/ip firewall mangle remove numbers=[find comment="auto mangle rule"]')
    error_usl (comand, type_def_mangle)

    comand = ssh.exec_cmd ('/ip firewall mangle add dst-address=!192.168.88.0/24 action=mark-connection chain=forward '
                           'connection-mark=no-mark new-connection-mark=new_mark_conn passthrough=yes comment="auto '
                           'mangle rule"')
    error_usl (comand, type_def_mangle)

    comand = ssh.exec_cmd ('/ip firewall mangle add action=mark-packet chain=forward '
                           'connection-mark=new_mark_conn new-packet-mark=mark_packet->new_con passthrough=yes '
                           'comment="auto mangle rule"')
    error_usl (comand, type_def_mangle)


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


def users():
    type_def = "users"
    comand = ssh.exec_cmd ("/user add "
                           "name=zabbix password=Putilin48 group=full address=10.10.0.1")
    error_usl (comand, type_def)
    comand = ssh.exec_cmd ("user set admin address=192.168.88.0/24")
    error_usl (comand, type_def)
    comand = ssh.exec_cmd ("/user add "
                           "name=rinet password=rinetsupport group=full")
    error_usl (comand, type_def)


def clock():
    type_def = "clock"
    command = ssh.exec_cmd ("/system clock set time-zone-autodetect= no time-zone-name= Europe/Moscow")
    error_usl (command, type_def)


def identity(login_name_device):
    type_def = "identity"
    command = ssh.exec_cmd ("/system identity set name= %s" % login_name_device)
    error_usl (command, type_def)


def ntp():

    type_def = "ntp"
    command = ssh.exec_cmd ("/system ntp client set enabled=yes primary-ntp=195.54.192.55")
    error_usl (command, type_def)


def loging():
    type_def = "loging"
    comand = ssh.exec_cmd ("/system logging set numbers=0 action=disk disabled=no topics=info,!ppp,!wireless ")
    error_usl (comand, type_def)

    comand = ssh.exec_cmd ("/system logging set numbers=1 action=disk disabled=no topics=error ")
    error_usl (comand, type_def)

    comand = ssh.exec_cmd ("/system logging set numbers=2 action=disk disabled=no topics=warning ")
    error_usl (comand, type_def)

    comand = ssh.exec_cmd ("/system logging set numbers=3 action=disk disabled=no topics=critical ")
    error_usl (comand, type_def)


# ============================MAIN-PROGRAMM=================================

if __name__ == '__main__':

    # clients
    ip_device_clients = "192.168.88.1"
    port_access_clients = 22
    login_local_device = "admin"
    pass_local_device = ""

    # server
    ip_device_server = "86.62.82.242"
    port_access_server = 64322
    login_server_device = "zabbix_api"
    pass_server_device = "Pdl48zx0ma3st15!"

    login_name = input ("Введите логин объекта:")

    #with ssh_server_device (hostname=ip_device_server, username=login_server_device,
     #                       password=pass_server_device, port=port_access_server) as ssh:


    with ssh_local_device (hostname=ip_device_clients, username=login_local_device,
                           password=pass_local_device, port=port_access_clients) as ssh:

        password = str (random_gen ())
        baba = 0

        while baba == 0:
            out = ssh.exec_cmd ("/system routerboard print")
            model, serial = parser_model_serial (out)



            first_start = input('Первый прогон? (yes/no):')
            if first_start != "yes":

                firewall ()
                ntp ()
                identity (login_name)
                loging ()
                users()
                baba = 1
            else:
                scheduler()
                upgrade ()
                baba = 1
