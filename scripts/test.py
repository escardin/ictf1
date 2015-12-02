from setflag import set_flag
from getflag import get_flag
from exploit import exploit
from benign import benign

flag = 'test'
ip = 'localhost'
port = '9800'
benign(ip, port)
resp = set_flag(ip, port, flag)
legit_flag = get_flag(ip, port, resp['FLAG_ID'], resp['TOKEN'])['FLAG']
if flag != legit_flag:
    raise Exception('Legit flag is wrong! flag: ' + flag + ' legit: ' + legit_flag)
exploit_flag = exploit(ip, port, resp['FLAG_ID'])['FLAG']
if flag != exploit_flag:
    raise Exception('Exploit flag is wrong! flag: ' + flag + ' exploit: ' + exploit_flag)
