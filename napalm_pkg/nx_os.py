import json
import napalm


driver = napalm.get_network_driver('nxos')

device = driver(hostname='10.10.20.58', username='admin',
                password='Cisco123', optional_args={'transport': 'https'})

device.open()

print "get facts: ", json.dumps(device.get_facts())