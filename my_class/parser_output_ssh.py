class parser_output_ssh:

    def __init__(self):
        pass

    @staticmethod
    def set_output_command(output_command):
        parser_output_ssh.output_command = output_command

    @staticmethod
    def result():

        temp_file = open('temp', 'w')
        temp_file.write(parser_output_ssh.output_command)
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
