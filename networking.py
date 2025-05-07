import ipaddress

# Define a list of IP addresses and subnet masks
ip_subnet_data = [
    {"ip": "192.168.1.0", "mask": "255.255.255.0"},
    {"ip": "10.0.0.0", "mask": "255.0.0.0"},
    {"ip": "172.16.0.0", "mask": "255.240.0.0"},
]

# Function to convert IP and subnet mask to CIDR notation
def ip_to_cidr(ip, mask):
    network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    return str(network)

# Iterate through the list and convert to CIDR notation
# for data in ip_subnet_data:
#     ip = data["ip"]
#     mask = data["mask"]
#     cidr = ip_to_cidr(ip, mask)
#     print(f"IP: {ip}, Mask: {mask} => CIDR: {cidr}")