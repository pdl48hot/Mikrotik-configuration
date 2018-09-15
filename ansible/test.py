#! /usr/bin/python
import yaml
import pprint


def logging():
    type_func = 'logging'

    with open(dir_cfg, 'r') as cfg_lines:
        config = cfg_lines.read()
        #print(config)
        yaml_data = yaml.safe_load(config)
        #pprint.pprint(yaml_data)
        parser_yaml = yaml_data[type_func]
        print(parser_yaml)


if __name__ == '__main__':
    hostname = '10.9.0.4'
    username = 'zabbix'
    password = 'Putilin48'
    port = 22
    #dir_cfg = 'C:\\Python\\Mikrotik\\config\\mikrotik-config.yml'
    dir_cfg = '/home/dk/ansible/config/mikrotik-config.yml'

    logging()
