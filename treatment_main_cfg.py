from class_treatment import *
import os

def class_def(type_error, dir_cfg_def, dir_command):
    class_treatment.set_type(type_error)
    class_treatment.set_dir_cfg_def(dir_cfg_def)
    class_treatment.set_dir_command(dir_command)
    class_treatment.result()


def firewall():
    type_error = 'firewall'
    dir_command = '/ip firewall filter add'

    # -------------------------FIREWALL-FILTER-DELETE-------------------------------------------------
    type_def_filter_delete = "firewall_filter_delete"
    #command = ssh_local_device.exec_cmd("/ip firewall filter {:foreach c in=[find] do={:do {remove $c;} on-error={}}} ")
    #error_usl(command, type_def_filter_delete)

    # -------------------------FIREWALL-FILTER-ADD-RULES----------------------------------------------
    class_def(type_error, dir_cfg, dir_command)


my_dir = os.getcwd()
dir_cfg = my_dir + '\\mikrotik-config.yml'

firewall()