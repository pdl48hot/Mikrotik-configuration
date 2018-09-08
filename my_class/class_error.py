class class_error:

    @staticmethod
    def set_type_input(type_input):
        class_error.set_type_input = type_input

    @staticmethod
    def set_command_output(command_output):
        class_error.command_output = command_output

    @staticmethod
    def result():
        if class_error.command_output == "failure: user with the same name already exisits\n":
            error = ('already created <type:%s>:' % class_error.set_type_input)
            return error
        elif class_error.command_output != "":
            error = ("error <type:%s>:" % class_error.set_type_input, class_error.command_output)

            return error