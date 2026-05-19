import yaml
from jinja2 import Environment, FileSystemLoader
from netmiko import Netmiko

# Read hosts from YAML file
hosts = yaml.load(open('hosts.yml'), Loader=yaml.SafeLoader)

# Read interfaces from YAML file
interfaces = yaml.load(open('interfaces.yml'), Loader=yaml.SafeLoader)

# Setup Jinja2 environment
env = Environment(
    loader=FileSystemLoader('.'),
    trim_blocks=True,
    autoescape=True
)

# Load the Jinja2 template
template = env.get_template('interfaces_config_template.j2')

# Render template with interface data
loopback_config = template.render(data=interfaces)

print("Generated Config:")
print("-" * 50)
print(loopback_config)
print("-" * 50)

# Loop through each host and push config
for host in hosts["hosts"]:
    print(f"\nConnecting to {host['name']}...")
    
    net_connect = Netmiko(
        host=host["name"],
        username=host["username"],
        password=host["password"],
        port=host["port"],
        device_type=host["type"]
    )
    
    print(f"Logged into {host['name']} successfully")
    
    output = net_connect.send_config_set(loopback_config.split("\n"))
    
    print(f"Pushed config into {host['name']} successfully")
    print(output)
    
    net_connect.disconnect()
    print(f"Disconnected from {host['name']}")

print("\nDone!")
