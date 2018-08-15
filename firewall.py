from yaml import Loader, load
import os

my_dir = os.getcwd()

yml_firewall_file = open(my_dir + '\\firewall\\firewall.txt', 'r')
firewall_file = load (yml_firewall_file, Loader=Loader)
for firewall_filter in firewall_file:
    newrules = []
    newrules.append ("/ip firewall filter ")

    for (param, value) in firewall_filter.items ():
        newrules.append (" " + str (param) + "=" + str (value))
    print(newrules)

