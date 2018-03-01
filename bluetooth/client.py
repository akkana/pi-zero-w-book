#!/usr/bin/env python

# From inquiry.py in bluezutils sample scripts
# and rfcomm-client.py in the python-bluez examples.

import bluetooth
import sys

uuid = "5f2f7e70-f863-451a-9619-9fce58e2e87e"

print("Searching for bluetooth devices...")

nearby_devices = bluetooth.discover_devices(lookup_names = True)
if not nearby_devices:
    print("Couldn't see any Bluetooth devices")
    sys.exit(1)

print("Found %d devices" % len(nearby_devices))
service_matches = None
for addr, name in nearby_devices:
    print("  %s - %s" % (addr, name))
    service_matches = bluetooth.find_service(uuid = uuid, address = addr)

if not service_matches:
    print("Couldn't find any PiBadgeServer services")
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("Connecting to \"%s\" on %s" % (name, host))

# Create the client socket
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((host, port))

print("Connected. Type stuff.")
while True:
    data = raw_input()
    if len(data) == 0: break
    sock.send(data)

sock.close()
