#!/bin/sh

# Create GPIO 14:
echo 14 > /sys/class/gpio/export
# That may give an I/O error if we've already created GPIO14.
# But you can ignore the error and proceed.

# Specify we will use GPIO 14 for output:
echo out > /sys/class/gpio/gpio14/direction

# Blink the light, once per second.
while true; do
    echo 1 > /sys/class/gpio/gpio14/value
    sleep 1
    echo 0 > /sys/class/gpio/gpio14/value
    sleep 1
done
