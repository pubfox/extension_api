import os
import subprocess
import re
import libvirt


class Devices():
		def __init__(self, tenant = "admin"):
			self.tenant = tenant
			self.macdict = {}
			fp = subprocess.Popen ("ifconfig", shell = True, stdout = subprocess.PIPE)
			for line in fp.stdout.readlines():
				if re.search ("HWaddr", line) and re.match ("vnet", line):
					device = line.split()[0]
					mac = line.split()[4]
					self.macdict [mac] = device
		
		def getInsDevice(self, ins_id):
			conn = libvirt.openReadOnly ("qemu:///system")
			try:
				dom = conn.lookupByUUIDString (ins_id)
			except libvirt.libvirtError, e:
				return -1
			self.xml = dom.XMLDesc(0)
			for line in self.xml.split('\n'):
				if re.search ("mac address", line): imac = line.split('=')[1].split('\'')[1]
			for mac, dev in self.macdict.items():
				if mac.split(':')[-5:] == imac.split(':')[-5:]:
					return self.macdict[mac]
			return None
		
		def strictNetspeed (self, ins_id, netspeed):
			self.dev = self.getInsDevice (ins_id)
			if self.dev == -1: return -1
			cmd = "tc -s qdisc del dev " + str(self.dev) + " root"
			os.system (cmd)
			netspeed = int(netspeed)
			if netspeed == 0:
				netspeed = 0.00001
			else:
				netspeed = netspeed * 1.5
			cmd = "tc -s qdisc add dev " + str(self.dev) + " root tbf rate " + str(netspeed) + "Mbit latency 50ms burst 10000 mpu 64 mtu 150000"
			os.system (cmd)
			#self.normal_return()
		
		def delNetspeed (self, ins_id):
			self.dev = self.getInsDevice (ins_id)
			cmd = "tc -s qdisc del dev " + self.dev + " root"
			os.system (cmd)

		def normal_return(self):
			return "ok"
		
		def error_return(self):
			return "nok"
