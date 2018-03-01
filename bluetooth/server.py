#!/usr/bin/env python

# From rfcomm-server.py in the python-bluez examples
# auth: Albert Huang <albert@csail.mit.edu>

import bluetooth

import sys

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "5f2f7e70-f863-451a-9619-9fce58e2e87e"

bluetooth.advertise_service(server_sock,
                            "PiServer",
                            service_id = uuid,
                            service_classes = [ uuid,
                                                bluetooth.SERIAL_PORT_CLASS ],
                            profiles = [ bluetooth.SERIAL_PORT_PROFILE ],
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
