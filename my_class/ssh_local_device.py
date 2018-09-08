import paramiko


class ssh_local_device:

    def __init__(self, **kwargs):
        self.client = paramiko.SSHClient ()
        self.client.set_missing_host_key_policy (paramiko.AutoAddPolicy ())
        self.kwargs = kwargs

    def __enter__(self):
        kw = self.kwargs  
        self.client.connect (hostname=kw.get ('hostname'), username=kw.get ('username'),
                             password=kw.get ('password'), port=int (kw.get ('port', 22)))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close ()

    def exec_cmd(self, cmd):

        stdin, stdout, stderr = self.client.exec_command (cmd)
        data = stdout.read ()
        # if stderr:
        # raise stderr
        return data.decode ()
