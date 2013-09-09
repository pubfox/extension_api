# Create your views here.
from django.http import HttpResponse
from extension_api.instance_device import Devices

def netspeed (request, ins_id, speed):
	netdev = Devices ()
	if speed <= 0:
		ret = netdev.delNetspeed(ins_id)
	else: ret = netdev.strictNetspeed(ins_id, speed)
	if ret == -1: return HttpResponse("nok")
	return HttpResponse ("ok")