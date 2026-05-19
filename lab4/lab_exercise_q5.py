import yaml
import logging
from netmiko import Netmiko

# =====================
# Setup Logger
# =====================
logging.basicConfig(
    filename='routing_table.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# =====================
# Read YAML file
# =====================
try:
    hosts = yaml.load(open('lab_hosts.yml'), Loader=yaml.SafeLoader)
    logger.info("Successfully loaded lab_hosts.yml")
except FileNotFoundError:
    logger.error("lab_hosts.yml not found. Exiting.")
    exit()

# =====================
# Loop through devices
# =====================
for host in hosts["hosts"]:

    logger.info("=" * 60)
    logger.info(f"Connecting to {host['hostname']} ({host['name']})")
    logger.info("=" * 60)

    try:
        net_connect = Netmiko(
            host=host["name"],
            username=host["username"],
            password=host["password"],
            secret=host["secret"],
            port=host["port"],
            device_type=host["type"]
        )
        logger.info(f"Successfully connected to {host['hostname']}")

        output = net_connect.send_command("show ip route", use_textfsm=True)

        print(f"\n{'='*60}")
        print(f"Routing Table for {host['hostname']}")
        print(f"{'='*60}")
        print(f"{'Protocol':<12} {'Network':<20} {'Distance':<10} {'Metric':<10}")
        print(f"{'-'*52}")

        for route in output:
            print(f"{route['protocol']:<12} {route['network']:<20} {route['distance']:<10} {route['metric']:<10}")
            logger.debug(f"{host['hostname']} route: {route}")

        net_connect.disconnect()
        logger.info(f"Disconnected from {host['hostname']} successfully")

    except Exception as e:
        logger.error(f"Failed to connect to {host['hostname']}: {e}")
        continue

logger.info("Script completed successfully")
