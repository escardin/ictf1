from set_flag import set_flag
from get_flag import get_flag
from exploit import exploit
from benign import benign

flag = 'test'
resp = set_flag('192.168.5.22', '8080', flag)
legit_flag = get_flag('192.168.5.22', '8080', resp['FLAG_ID'], resp['TOKEN'])['FLAG']
if flag != legit_flag:
    raise Exception('Legit flag is wrong! flag: '+flag+' legit: '+legit_flag)
exploit_flag = exploit('192.168.5.22', '8080', resp['FLAG_ID'])['FLAG']
if flag != exploit_flag:
    raise Exception('Exploit flag is wrong! flag: '+flag+' exploit: '+exploit_flag)
benign('192.168.5.22', '8080')
