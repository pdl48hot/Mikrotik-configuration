# Import necessary functions from Jinja2 module
from jinja2 import *

# Import YAML module
import yaml

# Load data from YAML into Python dictionary
config_data = yaml.load(open('C:\\Python\\Mikrotik\\config\\test-cfg-2.yml'))

# Load Jinja2 template
env = Environment(loader=FileSystemLoader('C:\\Python\\Mikrotik\\templates'), trim_blocks=True,
                  lstrip_blocks=True)
template = env.get_template('template2.rsc')

# Render the template with data and print the output
print(template.render(config_data))
