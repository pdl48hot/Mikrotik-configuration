import subprocess
import pprint
mac = '6C:3B:6B:04:1F:62'
test = subprocess.check_output(['C:\Python\Mikrotik\dll\Key.dll', '%s' % mac],
                               shell=True, universal_newlines=True)
test = test.strip('\n')

command_terminal = '/user add name=poh password=%s group=full' % str(test)
print(command_terminal)

