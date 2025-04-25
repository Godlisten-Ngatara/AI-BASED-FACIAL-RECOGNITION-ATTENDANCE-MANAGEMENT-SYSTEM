import re
import netifaces
from typing import List

from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery

def discover(scope = None) -> List:

    if (scope == None):
        ips = list()
        for iface in netifaces.interfaces():
            if(netifaces.AF_INET in netifaces.ifaddresses(iface)):
                ips.append(netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr'])
        scope = ['.'.join(ip.split('.')[:2]) for ip in ips]

    wsd = WSDiscovery()
    wsd.start()
    ret = wsd.searchServices()
    wsd.stop()

    onvif_services = [s for s in ret if str(s.getTypes()).find('onvif') >= 0]

    urls = [ip for s in onvif_services for ip in s.getXAddrs()]

    ips = [ip for url in urls for ip in re.findall(r'\d+\.\d+\.\d+\.\d+', url)]

    lst = [ip for ip in ips if any(ip.startswith(sp) for sp in scope)]
    return sorted(lst)