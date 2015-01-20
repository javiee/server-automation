#!/usr/bin/env python
import pyudev   

context = pyudev.Context()

for device in context.list_devices(MAJOR=8):
	if (device.device_type == 'disk'):
		print "{}".format(device.device_node)


