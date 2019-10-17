# author: axi0m
# purpose: rudimentary password cracker
# usage: crack.py --passfile 'C:\password_dump.txt' --hashtype 'md5' --hashfile 'C:\captured_hashes.txt'
# changelog: 02/26/18 - initial creation
# 05/28/18 - migrated to hashlib module and updated to PEP8 format
# https://docs.python.org/3/library/hashlib.html
# 10/10/18 - added click as import to handle arguments better than argparse
# 10/14/18 - added try/catch for exception handling, added more comments
# 10/17/19 - replaced default file paths, added more exception handling, cleaned up code
'''

TODO: Add logging and be more verbose in the exception/error handling
TODO: Using `map` may be a better way than with for handling files

'''

import hashlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--passfile', nargs='?', default='passwords_to_crack.txt', help="Password dump file", action="store", dest='passfile')
parser.add_argument('--hashtype', nargs='?', default='md5', help="The hash algorithm to use", action="store", dest='hashtype')
parser.add_argument('--hashfile', nargs='?', default='hashed_passwords.txt', action="store", dest='hashfile', help="The hashed password list to crack")

args = parser.parse_args()

# Convert all our arguments from argument parser to cleaner variable names
passfile = args.passfile
hashtype = args.hashtype
hashfile = args.hashfile

def test_pass(hashtype, hashPass):
    ''' Test if we hash of the password matches our password hash file '''
    with open(passfile, 'r') as dictFile:
        for word in dictFile:
            word = word.strip('\n')
            try:
                # TODO: If we create a new instance of the class I can dynamically update the hashtype as a passed variable
                # TODO: https://pymotw.com/2/hashlib/ <--- See that for details
                digest = hashlib.new(hashtype)
                digest.update(word.encode('utf-8'))

            except KeyboardInterrupt as keybd_err:
                print(f"[!] ERROR Keyboard interrupt handled: {keybd_err}")

            except SystemExit as sys_exit:
                print(f"[!] ERROR System exit: {sys_exit}")

            except Exception as generic_err:
                print(f"[!] ERROR Generic exception encountered: {generic_err}")
            
            if (digest.hexdigest() == hashPass):
                return print(f"[+] DEBUG Found Password: {word}")
            else:
                return print(f"[-] DEBUG Password Not Found.")


def main(hashfile, hashtype):
    ''' Accept file of hashes and given hash type '''
    print(f"[*] DEBUG Selected hash algorithm: {hashtype}")
    with open(hashfile) as hashFile:
        for line in hashFile.readlines():
                if ":" in line:
                    user = line.split(':')[0]
                    hashPass = line.split(':')[1].strip(" ")
                    print(f"[*] DEBUG Cracking password for: {user}")
                    test_pass(hashtype, hashPass)

if __name__ == "__main__":
    main(hashfile, hashtype)