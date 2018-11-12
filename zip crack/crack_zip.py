# author: axi0m
# purpose: rudimentary zip cracker
# usage: crack_zip.py --zip --passfile
# changelog: 10/12/18 - initial creation
# 10/25/2018 - kddiens - adding loop for the password database file
'''

To do:

'''

import zipfile
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file', nargs='?', default='F:\Archives\Brrcon2017.zip', action="store", dest='file', help="The zip file to crack.")
parser.add_argument('--pwdfile', nargs='?', default='F:\Password_Dump.txt', action="store", dest="pwdfile", help="The reference password file.")

args = parser.parse_args()

zfile = args.file
passfile = args.pwdfile

def test_pass(zfile, passfile):
    with open(passfile, 'r') as dictFile:
        for word in dictFile:
            # Strip the new line character
            word = word.strip('\n')
            # Wrap a try/catch to help with error handling
            try:
                zfile.extractall(pwd=word)
                print("[+] Password found: %s\n", word)
            except Exception:
                pass
                #print("Error encountered during extract!")

def main(zfile, passfile):
    test_pass(zfile, passfile)

if __name__ == "__main__":
    main(zfile, passfile)