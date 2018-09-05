import yaml


class class_treatment:

    def __init__(self):
        pass

    @staticmethod
    def set_type(type_func):
        class_treatment.type_func = type_func

    @staticmethod
    def set_dir_cfg_def(dir_config):
        class_treatment.dir_config_file = dir_config

    @staticmethod
    def set_dir_command(dir_command):
        class_treatment.dir_command = dir_command

    @staticmethod
    def set_queue_rate(queue_rate):
        class_treatment.queue_rate = queue_rate

    @staticmethod
    def set_ppp_account(ppp_account):
        class_treatment.ppp_account = ppp_account

    @staticmethod
    def set_ppp_password(ppp_password):
        class_treatment.ppp_password = ppp_password

    @staticmethod
    def set_ppp_next_ip(ppp_next_ip):
        class_treatment.ppp_next_ip = ppp_next_ip

    @staticmethod
    def result():

        temp = []
        with open(class_treatment.dir_config_file, 'r') as treatment_func:
            config = treatment_func.read()

        data = yaml.safe_load(config)
        dictList = data[class_treatment.type_func]

        for iterator in dictList:

            # lists
            new_rules_def = [class_treatment.dir_command]

            # My attempt:
            for key, value in iterator.items():
                try:
                    if value == 'tx_rate':
                            new_rules_def.append(' ' + str(key) + '=' + str(class_treatment.queue_rate))

                    elif value == 'ppp_login':
                            new_rules_def.append(' ' + str(key) + '=' + str(class_treatment.ppp_account))

                    elif value == 'ppp_password':
                            new_rules_def.append(' ' + str(key) + '=' + str(class_treatment.ppp_password))

                    elif value == 'ppp_ip':
                            new_rules_def.append(' ' + str(key) + '=' + str(class_treatment.ppp_next_ip))

                    else:
                        aKey = ' ' + str(key) + '=' + str(value)
                        new_rules_def.append(aKey)
                except:
                    pass

            command = ''.join(new_rules_def)
            temp.append(command)
            # print(temp)
        return temp



