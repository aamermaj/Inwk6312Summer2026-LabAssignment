import yaml
import logging
from jinja2 import Environment, FileSystemLoader
from netmiko import Netmiko

# =====================
# Setup Logger
# =====================
logging.basicConfig(
    filename='network_automation.log',
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
# Setup Jinja2
# =====================
try:
    env = Environment(
        loader=FileSystemLoader('.'),
        trim_blocks=True,
        autoescape=True
    )
    template = env.get_template('lab_config_template.j2')
    logger.info("Successfully loaded lab_config_template.j2")
except Exception as e:
    logger.error(f"Failed to load Jinja2 template: {e}")
    exit()

# =====================
# Loop through devices
# =====================
for host in hosts["hosts"]:

    logger.info("=" * 60)
    logger.info(f"Connecting to {host['hostname']} ({host['name']})")
    logger.info("=" * 60)

    try:
        config = template.render(host=host)
        logger.info(f"Config generated for {host['hostname']} successfully")
        logger.debug(f"Generated config for {host['hostname']}:\n{config}")
    except Exception as e:
        logger.error(f"Failed to render template for {host['hostname']}: {e}")
        continue

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

        output = net_connect.send_config_set(config.split("\n"))
        logger.info(f"Config pushed to {host['hostname']} successfully")
        logger.debug(f"Device output from {host['hostname']}:\n{output}")

        net_connect.disconnect()
        logger.info(f"Disconnected from {host['hostname']} successfully")

    except Exception as e:
        logger.error(f"Failed to connect to {host['hostname']}: {e}")
        continue

logger.info("Script completed successfully")
