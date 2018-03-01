#!/usr/bin/env python

# A Bluetooth server that lets nearby bluetooth-enabled devices
# discover and communicate with each other.

import bluetooth
import socket     # for gethostname() (eyeroll)
import sys

# UUID for the SwarmServer Bluetooth service
uuid = "5f2f7e70-f863-451a-9619-9fce58e2e87e"

def find_nearby_devices():
    '''Find all nearby Bluetooth devices, whether Swarm-enabled or not.'''
    print("Searching for bluetooth devices...")

    nearby_devices = bluetooth.discover_devices(lookup_names = True)
    if not nearby_devices:
        print("Couldn't see any Bluetooth devices")
        sys.exit(1)

    print("Found %d devices" % len(nearby_devices))
    for addr, name in nearby_devices:
        print("  %s - %s" % (addr, name))
        # service_matches = bluetooth.find_service(uuid = uuid, address = addr)
    return nearby_devices

def find_swarm_servers():
    '''Find all nearby Swarm servers.
    '''
    return bluetooth.find_service(uuid=uuid, address=None)

def connect_to_server(server):
    host = server["host"]

    print("Connecting to \"%s\" on %s %s" % (server['name'],
                                             server['provider'],
                                             server['host']))

    # Create the client socket
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((host, server["port"]))
    return sock

def start_server():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "5f2f7e70-f863-451a-9619-9fce58e2e87e"

    bluetooth.advertise_service(server_sock,
                                "SwarmServer",
                                service_id = uuid,
                                service_classes = [
                                    uuid, bluetooth.SERIAL_PORT_CLASS
                                ],
                                profiles = [ bluetooth.SERIAL_PORT_PROFILE ],
                                provider=socket.gethostname(),
                                description="Find other Swarm devices",
                                # protocols = [ bluetooth.OBEX_UUID ]
                               )

    print "Waiting for connection on RFCOMM channel %d" % port

    client_sock, client_info = server_sock.accept()
    print "Accepted connection from ", client_info

    try:
        while True:
            data = client_sock.recv(1024)
            if len(data) == 0: break
            print("received '%s'" % data)
    except IOError:
        pass

    print("Disconnected")

    client_sock.close()
    server_sock.close()

def print_server(server):
    print("%s" % (server['host']))
    for key in ('provider', 'name', 'description', 'protocol', 'port'):
        if key in server:
            print("    %s: %s" % (key, server[key]))

if __name__ == '__main__':
    # If -s, run a server:
    if len(sys.argv) > 1 and sys.argv[1] == '-s':
        start_server()
        sys.exit(0)

    # Otherwise discover servers and connect to the first one, if any.
    print("Searching for Swarm servers ...")
    servers = find_swarm_servers()
    if not servers:
        print("Couldn't find any SwarmServer services")
        sys.exit(0)

    print("Found %d server(s)" % len(servers))
    for server in servers:
        # Since it's not like python-bluetooth has any documentation ...
        # servers returned from bluetooth.find_service will have:
        # protocol, name, service-id, profiles, service-classes,
        # host (MAC addr), provider, port, description.
        print_server(server)

    # Connect to the first one.
    sock = connect_to_server(servers[0])

    print("Connected. Type stuff.")
    while True:
        data = raw_input()
        if len(data) == 0: break
        sock.send(data)

    sock.close()

