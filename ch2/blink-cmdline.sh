#!/bin/sh

# Blink an LED from the commandline using raspi-gpio.

while true; do
    # Set GPIO 14 to driving high:
    raspi-gpio set 14 op dh
    sleep 1
    # Set GPIO 14 to driving low:
    raspi-gpio set 14 op dl
    sleep 1
done

