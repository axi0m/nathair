# author: axi0m
# purpose: rudimentary zip cracker
# usage: crack_zip.py --zip --passfile
# changelog: 10/12/18 - initial creation
'''

To do:

'''

import zipfile
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--zipfile', nargs='?', default='F:\Archives\Brrcon2017.zip', action="store", dest='zipfile', help="The zip file to crack.")

args = parser.parse_args()

file = args.zipfile
passwd='F:\Password_Dump.txt'

def test_pass(file, passwd):
    zFile = zipfile.ZipFile(file)
    zFile.extractall(pwd=passwd)

def main(file, passwd):
    test_pass(file, passwd)

if __name__ == "__main__":
    main(file, passwd)