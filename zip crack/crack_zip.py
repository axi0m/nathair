# author: axi0m
# purpose: rudimentary zip cracker
# usage: crack_zip.py --zip --passfile
# changelog: 10/12/18 - initial creation
# 10/25/2018 - kddiens - adding loop for the password database file
# 11/12/2018 - kddiens - added threading, moved main logic to main function
'''

To do:
1. Add a lot more robust exception handling
2. Add minimal test cases
3. Add logging
4. Add counter/progress tracker
4. Examine if adding eventing or threading or map would improve performance of extract attempts
'''

import zipfile
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file', nargs='?', default='F:\Sample.zip', action="store", dest='file', help="The zip file to crack.")
parser.add_argument('--pwdfile', nargs='?', default='F:\password_test.txt', action="store", dest="pwdfile", help="The reference password file.")

args = parser.parse_args()

zfile = args.file
passfile = args.pwdfile

def extractfile(zfile, password):
    # Wrap a try/catch to help with error handling
    try:
        zfile.extractall(pwd=password.encode('utf=8'))
        print("[+] Password found: {}".format(password))
        exit(0)
    except Exception as ex:
        print(ex)
        return

def main(zfile, passfile):
    zFile = zipfile.ZipFile(zfile)
    with open(passfile, 'r') as dictFile:
        for word in dictFile:
        # Strip the new line character
            word = word.strip('\n')
            extractfile(zFile, word)

if __name__ == "__main__":
    main(zfile, passfile)