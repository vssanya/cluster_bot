import re
from pysnmp.hlapi import *

temp_re = re.compile(r"^.+ = (?P<temp>[0-9]+)$")

def temp(id):
    return 20
    errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                CommunityData('public', mpModel=0),
                UdpTransportTarget(('10.11.0.101', 161)),
                ContextData(),
                ObjectType(ObjectIdentity('1.3.6.1.4.1.318.1.1.10.4.2.3.1.5.0.{}'.format(id))))
                )

    if not errorIndication and not errorStatus:
        return int(temp_re.search(varBinds[0].prettyPrint()).groupdict()['temp'])
    else:
        return 0
