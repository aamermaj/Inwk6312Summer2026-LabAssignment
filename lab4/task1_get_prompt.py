from netmiko import Netmiko

device = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.101", 
    "username": "student",
    "password": "Meilab123",
    "port": "22",
}

net_connect = Netmiko(**device)

print(net_connect.find_prompt())


