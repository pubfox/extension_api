#!/usr/bin/python

from extension_api import instance_device
from instance_device import Devices

net_dev = Devices (dev = "vnet0", netspeed = "1")
print net_dev.netspeed
print net_dev
aaa = net_dev.normal_return()
