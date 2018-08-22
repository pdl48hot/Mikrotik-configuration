import yaml
import os


def treatment(dir_cfg_def, dir_command_def, type_def):
    with open(dir_cfg_def, 'r') as treatment_func:
        config = treatment_func.read()

    data = yaml.safe_load(config)
    dictList = data[type_def]

    for iterator in dictList:

        # lists
        new_rules_def = [dir_command_def]

        # My attempt:
        for key, value in iterator.items():
            aKey = ' ' + str(key) + '=' + str(value)
            new_rules_def.append(aKey)

        command = ''.join(new_rules_def)
        # add_firewall_rules = ssh.exec_cmd(command)
        # error_usl(add_firewall_rules, type_def)
        print(command)


my_dir = os.getcwd()

if __name__ == '__main__':
    type_error = 'logging'
    dir_mikrotik_cfg = my_dir + '\\test.yml'
    dir_command = '/system logging set'
    treatment(dir_mikrotik_cfg, dir_command, type_error)
