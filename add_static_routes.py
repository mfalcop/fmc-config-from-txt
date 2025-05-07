from fireREST import FMC
from networking import ip_to_cidr

FMC_BASE_URL = "https://10.122.109.62"
FMC_USERNAME = "api"
FMC_PASSWORD = "CXlabs.123"
management_center = {
    "ip_address": "10.122.109.62",
    "username": "api",
    "password": "CXlabs.123",
    "domain": "Global"
}
domain_uuid = 'e276abec-e0f2-11e3-8169-6d9ed49b625f'
device_uuid = '84cbc758-254b-11f0-8ba9-d57f7495d4f5'

def create_static_route(fmc, interface, network, gateway, distance):
    print("Creating static route for interface:", interface)

    data = {
    "interfaceName": interface,
    "selectedNetworks": [
        {
            "id": network
        }
    ],
    "gateway": {
        "object": {
            "id": gateway
        }
    },
    "metricValue": distance,
    }
    try:
        route = fmc.device.devicerecord.routing.ipv4staticroute.create(container_uuid=device_uuid, data=data)
        print("Static route created successfully:", route)

    except Exception as e:
        print("Error creating static route:", e)
        return

def main():
    print("Getting access to the FMC")
    fmc = FMC(hostname=management_center['ip_address'], username=management_center['username'],
              password=management_center['password'], domain=management_center['domain'])
    print("Access to the FMC established")
    route = fmc.device.devicerecord.routing.ipv4staticroute.get(container_uuid=device_uuid)
    
    # Open file with routes
    with open('static_routes_config.txt', 'r') as file:
        # Read the entire file content into a string
        lines = file.readlines()

    for index, line in enumerate(lines):
        print("getting route", index)
        parsed_line = line.split()
        cidr = ip_to_cidr(parsed_line[1], parsed_line[2])
        split = cidr.split('/')
        # Check if the CIDR is a host or network
        # If it is a host (e.g., /32), create a host object, otherwise create a network object
        
        


        try:
            if "32" in split[1]:
                net_objects = fmc.object.host.get(name_or_value=split[0])
                if not net_objects:
                    #print("Creating new host object for:", split[0])
                    # Create a new host object
                    data = {'name': "Host-{}".format(split[0]), 'value': split[0]}
                    net_objects = fmc.object.host.create(data)
                    print("Created host object:", split[0])
                    network = net_objects
                    
                else:
                    print("Host object already exists:", net_objects[0]['name'])
                    network = net_objects[0]
              
            else:
                net_objects = fmc.object.network.get(name_or_value=cidr)
                if not net_objects:
                    #print("Creating new network object for:", split[0])
                    # Create a new host object
                    data = {'name': "Network-{}".format(split[0]), 'value': cidr}
                    net_objects = fmc.object.network.create(data)
                    print("Created network object:", cidr)
                    network = net_objects
                else:
                    print("Network object already exists:", net_objects[0]['name'])
                    network = net_objects[0]
        except Exception as e:
            print("Error creating network object: ", split[0], e)

        # Check if the gateway exists, if not create it
        try:
            
            gateway = fmc.object.host.get(name_or_value=parsed_line[4])
            if not gateway:
                #print("Creating new gateway host object for:", parsed_line[4])
                # Create a new host object for the gateway
                data = {'name': "Host-{}".format(parsed_line[4]), 'value': parsed_line[4]}
                gateway = fmc.object.host.create(data)
                print("Created gateway host object:", parsed_line[4])
            else:
                print("Gateway host object already exists:", gateway[0]['name'])
                gateway = gateway[0]
        except Exception as e:
            print("Error creating network object: "+parsed_line[4], e)
        
        ifc =  parsed_line[0]
        dis = parsed_line[4]
        # Create the static route
        create_static_route(fmc, ifc, network['id'], gateway['id'], dis)
        #print("Static route created: ", line)


if __name__ == "__main__":
    main()