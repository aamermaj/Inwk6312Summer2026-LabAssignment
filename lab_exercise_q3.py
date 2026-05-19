import yaml
from jinja2 import Environment, FileSystemLoader
from netmiko import Netmiko

# =====================
# Read YAML files
# =====================
hosts = yaml.load(open('lab_hosts.yml'), Loader=yaml.SafeLoader)

# =====================
# Setup Jinja2
# =====================
env = Environment(
    loader=FileSystemLoader('.'),
    trim_blocks=True,
    autoescape=True
)

template = env.get_template('lab_config_template.j2')

# =====================
# Loop through devices
# =====================
for host in hosts["hosts"]:

    print("=" * 60)
    print(f"Connecting to {host['hostname']} ({host['name']})...")
    print("=" * 60)

    # Render config for this specific host
    config = template.render(host=host)

    print("Generated Config:")
    print("-" * 60)
    print(config)
    print("-" * 60)

    # Connect via Netmiko
    net_connect = Netmiko(
        host=host["name"],
        username=host["username"],
        password=host["password"],
        secret=host["secret"],
        port=host["port"],
        device_type=host["type"]
    )

    print(f"Logged into {host['hostname']} successfully")

    # Enter enable mode
    net_connect.enable()

    # Push config to device
    output = net_connect.send_config_set(config.split("\n"))

    print(f"Config pushed to {host['hostname']} successfully")
    print(output)

    # Disconnect
    net_connect.disconnect()
    print(f"Disconnected from {host['hostname']}")
    print()

print("=" * 60)
print("All devices configured successfully")
print("=" * 60)
