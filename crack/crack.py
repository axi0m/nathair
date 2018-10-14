# author: axi0m
# purpose: rudimentary password cracker
# usage: crack.py --passfile 'C:\password_dump.txt' --hashtype 'md5' --hashfile 'C:\captured_hashes.txt'
# changelog: 02/26/18 - initial creation
# 05/28/18 - migrated to hashlib module and updated to PEP8 format
# https://docs.python.org/3/library/hashlib.html
# 10/10/18 - added click as import to handle arguments better than argparse
# 10/14/18 - added try/catch for exception handling, added more comments
'''

To do:
Add logging and be more verbose in the exception/error handling
Using `map` may be a better way than with for handling files

'''

import hashlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--passfile', nargs='?', default='F:\Password_Dump.txt', help="Password dump file", action="store", dest='passfile')
parser.add_argument('--hashtype', nargs='?', default='md5', help="The hash algorithm to use", action="store", dest='hashtype')
parser.add_argument('--hashfile', nargs='?', default='F:\Documents\Python\violent_python\crack\passwords.txt', action="store", dest='hashfile', help="The hashed password list to crack")

args = parser.parse_args()

# Convert all our arguments from argument parser to cleaner variable names
passfile = args.passfile
hashtype = args.hashtype
hashfile = args.hashfile

def test_pass(hashtype, hashPass):
    # We use `with` to handle file operations and close the object
    with open(passfile, 'r') as dictFile:
        for word in dictFile:
            # Strip the new line character
            word = word.strip('\n')
            # Wrap a try/catch to help with error handling
            #count = count+1
            try:
                # If we create a new instance of the class I can dynamically update the hashtype as a passed variable
                # https://pymotw.com/2/hashlib/ <--- See that for details
                digest = hashlib.new(hashtype)
            except:
                print("[!] Error encountered!\n")
            finally:
                # I removed the string = string.update format here as it isn't necessary using the native .update method
                digest.update(word.encode('utf-8'))
            #print("[*] Processed hash " + hashPass + "\n")
            if (digest.hexdigest() == hashPass):
                print("[+] Found Password: " + word + "\n")
                return
        print("[-] Password Not Found.\n")
    return


def main(hashfile, hashtype):
    print("[*] Selected Hash Algorithm: " + hashtype + "\n")
    hashFile = open(hashfile)
    for line in hashFile.readlines():
        if ":" in line:
            user = line.split(':')[0]
            hashPass = line.split(':')[1].strip(" ")
            print("[*] Cracking password for: " + user)
            test_pass(hashtype, hashPass)

if __name__ == "__main__":
    main(hashfile, hashtype)