#!/usr/bin/env python
from subprocess import Popen, PIPE
from getpass import getpass

def install_package(p):
    print('Enter root password to install %s:' % p)
    Popen(['sudo', 'zypper', 'in', '-y', p], stdout=PIPE).wait()

# Check if we have python2-python-pam
if Popen(['zypper', 'se', 'python2-python-pam'], stdout=PIPE, stderr=PIPE).wait() == 0:
    try:
        import pam
    except ImportError:
        install_package('python2-python-pam')
        import pam
    p = pam.pam()
    p.authenticate(raw_input('Username: '), getpass())
    print('{} {}'.format(p.code, p.reason))
    exit(0)

# Check if we have python-pam
try:
    import PAM
except ImportError:
    install_package('python-pam')
    import PAM

def pam_conv(auth, query_list):
    resp = []
    for (query, type) in query_list:
        # Never echo
        if type == PAM.PAM_PROMPT_ECHO_ON or PAM.PAM_PROMPT_ECHO_OFF:
            resp.append((getpass(query), 0))
        else:
            print(query)
            resp.append(('', 0))
    return resp

p = PAM.pam()
p.start('passwd')
p.set_item(PAM.PAM_USER, raw_input('Username: '))
p.set_item(PAM.PAM_CONV, pam_conv)
try:
    p.authenticate()
except:
    print('Authentication failed')
else:
    print('Authentication succeeded')
try:
    p.acct_mgmt()
except:
    print('User is not allowed')
else:
    print('User is allowed')
