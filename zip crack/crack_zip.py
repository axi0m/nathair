# author: axi0m
# purpose: rudimentary zip cracker
# usage: crack_zip.py --zip --passfile

from zipfile import ZipFile
from zipfile import BadZipFile
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--file", nargs="?", action="store", dest="file", help="The zip file to crack."
)
parser.add_argument(
    "--pwdfile",
    nargs="?",
    action="store",
    dest="pwdfile",
    help="The reference password file.",
)

args = parser.parse_args()

zfile = args.file
pfile = args.pwdfile


def extractfile(zf, word):

    try:
        zf.extractall(pwd=word.encode("utf-8"))
        print("[+] Password found: {}".format(word))

    except RuntimeError:
        pass  # To Do

    except Exception as err:
        return err


def main(zfile, pfile):

    try:
        with ZipFile(zfile) as zf:
            with open(pfile, "r") as dictFile:
                for word in dictFile:
                    word = word.strip("\n")
                    extractfile(zf, word)

    except BadZipFile as err:
        print("[!] Bad zip file encountered: {}".format(err))


if __name__ == "__main__":
    main(zfile, pfile)
