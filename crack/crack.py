# author: axi0m
# purpose: rudimentary password cracker
# usage: crack.py
# changelog: 02/26/18 - initial creation
# 05/28/18 - migrated to hashlib module and updated to PEP8 format
# https://docs.python.org/3/library/hashlib.html

'''

To do:
Add checking for multiple hash types (sha256, sha512, etc)
Add logging and be more verbose in the exception/error handling
Using `map` may be a better way than with for handling files

'''

import hashlib

def test_pass(cryptPass):
    # below code was in example when using crypt module which does not exist anymore
    # salt = cryptPass[0:2]
    with open('F:\Password_Dump.txt', 'r') as dictFile:
        for word in dictFile:
            word = word.strip('\n')
            digest = hashlib.md5(word.encode('utf-8'))
            if (digest.hexdigest() == cryptPass):
                print("[+] Found Password: " + word + "\n")
                return
        print("[-] Password Not Found.\n")
    return


def main():
    passFile = open('passwords.txt')
    for line in passFile.readlines():
        if ":" in line:
            user = line.split(':')[0]
            cryptPass = line.split(':')[1].strip(" ")
            print("[*] Cracking password for: " + user)
            test_pass(cryptPass)


if __name__ == "__main__":
    main()